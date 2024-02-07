from enum import Enum
import typer
from typing_extensions import Annotated
from typing import Optional
from pathlib import Path

import json
import logging 
logger = logging.getLogger()
logger.setLevel(logging.INFO)

from rich.progress import track
from rich import print 
from rich.console import Console

# for typer
from .dataclasses_cli import Autoencoder, Optimizer, Loss, Activation, Preprocessing

console=Console()
app = typer.Typer(rich_markup_mode="rich",
    help="Create FCGRs, Train an Autoencoder, and extract the Encoder from it to map FCGRs to the embedding space.")

@app.command("train-autoencoder", help="Train an autoencoder.")
def train(
        outdir: Annotated[Path, typer.Option(help="directory to save experiment results")],
        datadir: Annotated[Path, typer.Option(help="directory where FCGR with numpy files are stored. If None, training_list will be used")] = None,
        training_list: Annotated[Path, typer.Option(help=".txt file with paths to FCGR to be used for training the autoencoder. If None, datadir will be used")] = None,
        autoencoder: Annotated[Autoencoder, typer.Option(help="name of autoencoder to use for training")] = Autoencoder.AutoencoderFCGR.value,
        latent_dim: Annotated[int, typer.Option(min=2, help="number of dimension embedding space")] = 100, 
        kmer: Annotated[int, typer.Option(min=1)] = 6,
        hidden_activation: Annotated[Activation,typer.Option(help="activation function for hidden layers")]=Activation.Relu.value,
        output_activation: Annotated[Activation,typer.Option(help="activation function output layer")]=Activation.Softmax.value,
        batch_normalization: Annotated[bool, typer.Option("--batch-normalization/ ","-bn/ ", help="If set, batch normalization will be applied after each ConvFCGR and DeConvFCGR")]=False,
        preprocessing: Annotated[Preprocessing, typer.Option(help="preprocessing")]=Preprocessing.Distribution.value,
        epochs: Annotated[int, typer.Option(min=1)] = 50,
        batch_size: Annotated[int, typer.Option(min=1)] = 64,
        loss: Annotated[Loss, typer.Option(help="loss function (keras option with default params)")] = Loss.CategoricalCrossEntropy.value,
        optimizer: Annotated[Optimizer, typer.Option(help="optimizer to train the autoencoder (keras option with default params)")] = Optimizer.Adam.value,
        patiente_early_stopping: Annotated[int, typer.Option()] = 20,
        patiente_learning_rate: Annotated[int, typer.Option()] = 10,
        train_size: Annotated[float, typer.Option(min=0.01, max=0.99)] = 0.8,
        seed: Annotated[int, typer.Option(help= "to reproduce split of dataset")] = 42,
        ) -> None:
    print(f"Training neural network of type: {autoencoder.value}")

    from collections import Counter
    import tensorflow as tf
    from .dnn.loaders.VARdataloader import DataLoaderVAR as DataLoader
    from .dnn.models import (
        DenseAutoencoder,
        CNNAutoencoder,
        CNNAutoencoderBN, 
        CNNAutoencoderCAE,
        CNNAutoencoderCAEBN,
        CNNAutoencoderCAEBNLeakyRelu,
        CNNAutoencoderCAEBNL2Emb,
        AutoencoderFCGR
        )
    from .dnn.callbacks import CSVTimeHistory
    from .dnn.utils.split_data import TrainValTestSplit

    assert any([datadir is not None, training_list is not None]), "Missing INFO: at least one of --datadir or --training-list must be provided."
    
    KMER=kmer

    # parameters train
    LATENT_DIM=latent_dim
    EPOCHS=epochs
    BATCH_SIZE=batch_size
    ARCHITECTURE=autoencoder
    PATIENTE_EARLY_STOPPING=patiente_early_stopping
    PATIENTE_LEARNING_RATE=patiente_learning_rate
    TRAIN_SIZE=train_size
    SEED=seed

    # folder where to save training results
    PATH_TRAIN=Path(outdir)
    PATH_TRAIN.mkdir(exist_ok=True, parents=True)

    # preprocessing of each FCGR to feed the model 
    if preprocessing == "distribution":
        # sum = 1
        preprocessing = lambda x: x / x.sum().sum()    
    else: 
        # scale [0,1]
        preprocessing = lambda x: x / x.max() 

    # ------ data split ------
    if datadir is not None:
        # From a directory with .npy files
        #FIXME: this only works for the bacterial dataset in its current form

        # parameters dataset
        PATH_FCGR=Path(datadir)

        ## Create train-val-test datasets 
        label_from_path=lambda path: Path(path).parent.stem.split("__")[0]

        # paths to fcgr 
        list_npy = [p for p in Path(PATH_FCGR).rglob('*/*.npy')] # if "dustbin" not in str(p) and "__01" in str(p)]
        labels = [label_from_path(path) for path in list_npy]#[:1000]
        
        tvt_split = TrainValTestSplit(id_labels=list_npy, labels=labels, seed=SEED)
        tvt_split(train_size=TRAIN_SIZE, balanced_on=labels)# split datasets
        list_train = tvt_split.datasets["id_labels"]["train"]
        list_val   = tvt_split.datasets["id_labels"]["val"]
        list_test  = tvt_split.datasets["id_labels"]["test"]

        logging.info(f"training on {len(list_train)}")
        logging.info(f"validating on {len(list_val)}")
        logging.info(f"Testing on {len(list_test)}")

        with open(PATH_TRAIN.joinpath("summary-split.json"),"w") as fp:
            json.dump(tvt_split.get_summary_labels(), fp)

        # save split
        with open(PATH_TRAIN.joinpath("split-train-val-test.json"),"w") as fp:
            json.dump(tvt_split.datasets, fp, indent=4)
    else:
        # From training list
        list_paths = []
        with open(training_list, "r") as fp:
            for line in fp.readlines():
                path = line.replace("\n","").strip().split("\t")[0] # first column of the input file 
                if path.endswith(".npy"): 
                    list_paths.append(path)

        N_paths = len(list_paths)
        pos_cut = int(N_paths*train_size)
        list_train = list_paths[:pos_cut]
        list_val   = list_paths[pos_cut:]

    # ------ training -----
        
    # dataset train
    ds_train = DataLoader(
        list_paths=list_train,
        batch_size=BATCH_SIZE,
        shuffle=True,
        preprocessing=preprocessing
    )

    # dataset validation
    ds_val = DataLoader(
        list_paths=list_val,
        batch_size=BATCH_SIZE,
        shuffle=False,
        preprocessing=preprocessing
    )

    # - Callbacks: actions that are triggered at the end of each epoch
    # checkpoint: save best weights
    Path(f"{PATH_TRAIN}/checkpoints").mkdir(exist_ok=True, parents=True)
    cb_checkpoint = tf.keras.callbacks.ModelCheckpoint(
        filepath=f'{PATH_TRAIN}/checkpoints/weights-{ARCHITECTURE}.keras',
        monitor='val_loss',
        mode='min',
        save_best_only=True,
        verbose=1
    )

    # reduce learning rate
    cb_reducelr = tf.keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        mode='min',
        factor=0.1,
        patience=PATIENTE_LEARNING_RATE,
        verbose=1,
        min_lr=0.00001
    )

    # stop training if
    cb_earlystop = tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',
        mode='min',
        min_delta=0.001,
        patience=PATIENTE_EARLY_STOPPING,
        verbose=1
    )

    # save history of training
    cb_csvlogger = tf.keras.callbacks.CSVLogger(
        filename=f'{PATH_TRAIN}/training_log.csv',
        separator='\t',
        append=False
    )

    # save time by epoch
    cb_csvtime = CSVTimeHistory(
        filename=f'{PATH_TRAIN}/time_log.csv',
        separator='\t',
        append=False
    )
    # print(autoencoder.model.summary())
    # Load and train model
    autoencoder=eval(f"""{ARCHITECTURE}(latent_dim = {LATENT_DIM}, 
                output_activation='{output_activation}', 
                hidden_activation='{hidden_activation}', 
                kmer={kmer}, 
                batch_normalization={batch_normalization},
                )""")
    
    if optimizer.value=="ranger":
        import tensorflow_addons as tfa
        
        radam = tfa.optimizers.RectifiedAdam()
        ranger = tfa.optimizers.Lookahead(radam, sync_period=6, slow_step_size=0.5)
        optimizer = ranger
    else:
        optimizer=optimizer.value
    autoencoder.compile(optimizer=optimizer, loss=loss.value)
    autoencoder.fit(
        ds_train, 
        validation_data=ds_val, 
        epochs=EPOCHS,
        callbacks=[
            cb_checkpoint,
            cb_reducelr,
            cb_earlystop,
            cb_csvlogger,
            cb_csvtime
            ]
    )

@app.command("split-autoencoder",help="Save Encoder and Decoder as separated models.",)
def split_autoencoder(
        path_checkpoint: Annotated[Path, typer.Option("--path-checkpoint","-c", help="path to .keras model with trained weights.")],
        dirsave: Annotated[Path, typer.Option("--dirsave","-ds", help="directory to save encoder and decoder.")],
        encoder_only: Annotated[bool, typer.Option("--encoder-only/ ","-e/ ", help="store only the encoder, decoder will be discarded.")] = False,
        tflite: Annotated[bool, typer.Option("--tflite/ ","-t/ ", help="save models in .tflite format instead of .keras format.")] = False,
        ) -> None:
    from pathlib import Path
    import tensorflow as tf
    
    console.print(":dna: loading autoencoder")
    autoencoder = tf.keras.models.load_model(path_checkpoint)

    # get Encoder and/or Decoder as separate models
    console.print(":scissors: getting encoder...")
    encoder = tf.keras.models.Model(autoencoder.input,autoencoder.get_layer("output_encoder").output)
    if encoder_only is False:
        console.print(":scissors: getting encoder...")
        decoder = tf.keras.models.Model(autoencoder.get_layer("input_decoder").input, autoencoder.output)

    # save Encoder and/or Decoder
    path_save_models = Path(dirsave)
    path_save_models.mkdir(exist_ok=True, parents=True)
    
    name_models = ["encoder"] if encoder_only else ["encoder","decoder"]

    for name_model in name_models:
        
        if tflite:
            console.print(f":floppy_disk: saving {name_model} in .tflite")
            # Convert the models in .tflite format
            converter = tf.lite.TFLiteConverter.from_keras_model(eval(f"{name_model}"))
            tflite    = converter.convert()

            # Save the model
            with open(path_save_models.joinpath(f"{name_model}.tflite"), "wb") as f:
                f.write(tflite)
        else:    
            console.print(f":floppy_disk: saving {name_model} in .keras")
            # Save as .keras models
            model = eval(f"{name_model}")
            model.save(path_save_models.joinpath(f"{name_model}.keras"))

@app.command("fcgr",help="Create the Frequency matrix of CGR (FCGR) from k-mer counts.")
def create_fcgr_kmc(path_kmer_counts: Annotated[Path, typer.Option("--path-kmer-counts","-pk",mode="r", help="path to .txt file with kmer counts.")],
                path_save: Annotated[Path, typer.Option("--path-save","-ps",mode="w", help="path to .npy file to store FCGR.")],
                kmer: Annotated[int, typer.Option("--kmer","-k",min=1)] = 6) -> None:

    from .fcgr.fcgr_from_kmc import FCGRKmc
    import numpy as np
    from pathlib import Path

    fcgr = FCGRKmc(kmer)
    m = fcgr(path_kmer_counts)
    Path(path_save).parent.mkdir(exist_ok=True, parents=True)
    np.save(path_save, m)

@app.command("fcgr-fasta",help="Create the Frequency matrix of CGR (FCGR) from a fasta file.")
def create_fcgr_fasta(path_fasta: Annotated[Path, typer.Option("--path-fasta","-pf",mode="r", help="path to .fa file with assembly.")],
                path_save: Annotated[Path, typer.Option("--path-save","-ps",mode="w", help="path to .npy file to store FCGR.")],
                kmer: Annotated[int, typer.Option("--kmer","-k",min=1)] = 6) -> None:

    # from .fcgr.fcgr_from_kmc import FCGRKmc
    from complexcgr import FCGR
    import numpy as np
    from pathlib import Path
    from Bio import SeqIO

    fcgr = FCGR(kmer)
    with open(path_fasta,"r") as fp:
        record = SeqIO.read(fp, format="fasta")
    
    m = fcgr(sequence=record.seq)

    Path(path_save).parent.mkdir(exist_ok=True, parents=True)
    np.save(path_save, m)

@app.command("split-data", help="Split a list of files in either train, validation and test, or in sets for k-fold validation.")
def split_data(datadir: Annotated[Path, typer.Option("--datadir","-d", help="path to folder with .npy files.")],
               outdir: Annotated[Path, typer.Option("--outdir","-o", mode="w", help="directory to save split results.")],
               kfold: Annotated[int, typer.Option("--kfold","-k", help="If provided, the .npy files in datadir will be split in k-folds for cross-validation.", min=1)] = None,
               path_labels: Annotated[Path, typer.Option("--labels", mode="r", help=".txt file where the first column is the sample_id (eg. path/to/<sample_id>.fa) and second column is the label (tab separated)")] = None
               ):
    
    from pathlib import Path
    from .dnn.utils.split_data import TrainValTestSplit
    from .dnn.utils.split_data_cross_validation import CrossValidationSplit

    list_paths = [str(p) for p in Path(datadir).rglob("*.npy")]

    outdir=Path(outdir)
    outdir.mkdir(exist_ok=True, parents=True)

    # load labels
    if path_labels: 
        labels_by_sampleid = dict()
        with open(path_labels, "r") as fp:
            for line in fp.readlines():
                try:
                    # TODO: any better way to standarize the label? could change for other experiments
                    sample_id, label = line.replace("\n","").strip().split("\t")
                    sample_id = sample_id.strip()
                    label = "_".join(label.lower().strip().split(" "))
                    labels_by_sampleid[sample_id] = label
                except:
                    continue #to avoid failing when lines are empty or no valid info
        # del labels_by_sampleid
        
    if kfold:
        split_cv = CrossValidationSplit(kfolds=kfold)
        paths_by_partition = split_cv(list_paths)
        
        ids_partition = set(paths_by_partition.keys())
        for id_partition, paths_partition in paths_by_partition.items():
            # for test consider 1 fold  
            list_test  = paths_partition
            
            # for train consider the remaining (k-1) folds
            list_train = []
            id_partitions_train = set(ids_partition) - set([id_partition])

            for id_partition_train in id_partitions_train:
                list_train.extend(
                    paths_by_partition[id_partition_train]
                )

            path_train = outdir.joinpath(f"train_{id_partition+1}-fold.txt")
            print(path_train)
            with open(path_train, "w") as fp:
                for path in list_train:
                    if path_labels:
                        sample_id = Path(path).stem
                        label = labels_by_sampleid.get(sample_id, "unknown")
                        fp.write(f"{path}\t{label}\n")
                    else:
                        fp.write(f"{path}\n")

            path_test=outdir.joinpath(f"test_{id_partition+1}-fold.txt")
            print(path_test)
            with open(path_test, "w") as fp:
                for path in list_test:
                    if path_labels:
                        sample_id = Path(path).stem
                        label = labels_by_sampleid.get(sample_id, "unknown")
                        fp.write(f"{path}\t{label}\n") 
                    else:
                        fp.write(f"{path}\n")

    print("finished")