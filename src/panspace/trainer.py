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
# from .dataclasses_cli import 
from .dataclasses_cli import (
    Autoencoder,
    ModelMetricLearning, 
    Optimizer, 
    LossAutoencoder,
    LossMetricLearning, 
    LossOneShot,
    Activation, 
    Preprocessing,
)

console=Console()
app = typer.Typer(rich_markup_mode="rich",
    help="Train Autoencoder/Metric Learning. Utilities.")

@app.command("autoencoder", help="Train an autoencoder.")
def train_autoencoder(
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
        loss: Annotated[LossAutoencoder, typer.Option(help="loss function (keras option with default params)")] = LossAutoencoder.CategoricalCrossEntropy.value,
        optimizer: Annotated[Optimizer, typer.Option(help="optimizer to train the autoencoder (keras option with default params)")] = Optimizer.Adam.value,
        patiente_early_stopping: Annotated[int, typer.Option()] = 20,
        patiente_learning_rate: Annotated[int, typer.Option()] = 10,
        train_size: Annotated[float, typer.Option(min=0.01, max=0.99)] = 0.8,
        seed: Annotated[int, typer.Option(help= "to reproduce split of dataset")] = 42,
        ) -> None:
    print(f"Training neural network of type: {autoencoder.value}")

    from collections import Counter
    import tensorflow as tf
    from .dnn.loaders import DataLoaderAutoencoder as DataLoader
    from .dnn.models import AutoencoderFCGR
    from .dnn.callbacks import CSVTimeHistory
    from .dnn.utils.split_data import TrainValTestSplit

    print(tf.config.list_physical_devices('GPU'))
    # tf.debugging.set_log_device_placement(True)


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
        preprocessing=preprocessing,
        inference_mode = False,
        reshape = True,
        kmer_size=KMER,
    )

    # dataset validation
    ds_val = DataLoader(
        list_paths=list_val,
        batch_size=BATCH_SIZE,
        shuffle=False,
        preprocessing=preprocessing,
        inference_mode = False,
        reshape = True,
        kmer_size=KMER,
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
            ],
        workers=8, use_multiprocessing=True, max_queue_size=256
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

@app.command("split-data-cross-validation", help="Split a list of files in either train, validation and test, or in sets for k-fold validation.")
def split_dataset_cross_validation(
            datadir: Annotated[Path, typer.Option("--datadir","-d", help="path to folder with .npy files.")],
            outdir: Annotated[Path, typer.Option("--outdir","-o", mode="w", help="directory to save split results.")],
            kfold: Annotated[int, typer.Option("--kfold","-k", help="If provided, the .npy files in datadir will be split in k-folds for cross-validation.", min=1)] = 5,
            path_labels: Annotated[Path, typer.Option("--labels", mode="r", help=".txt file where the first column is the sampleid and second column is the label (tab separated)")] = None,
            seed: Annotated[int, typer.Option("--seed", "-s", help= "to reproduce split of dataset")] = 42,
            ):
    
    from pathlib import Path
    from .dnn.utils.split_data_cross_validation import CrossValidationSplit

    SEED = seed 

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
        
    if kfold > 1:
        print("Cross validation")
        split_cv = CrossValidationSplit(kfolds=kfold)
        paths_by_partition = split_cv(list_paths)
        print(len(list_paths))
        
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

# @app.command("split-data")
def split_dataset(
            datadir: Annotated[Path, typer.Option("--datadir","-d", help="path to folder with .npy files.")],
            outdir: Annotated[Path, typer.Option("--outdir","-o", mode="w", help="directory to save split results.")],
            train_size: Annotated[float, typer.Option(min=0.01, max=0.99)] = 0.8,
            path_labels: Annotated[Path, typer.Option("--labels", mode="r", help=".txt file where the first column is the prefix of the filename (eg. path/to/<prefix>.fa) and second column is the label (tab separated)")] = None,
            seed: Annotated[int, typer.Option("--seed", "-s", help= "to reproduce split of dataset")] = 42,
        ):

    from .dnn.utils.split_data import TrainValTestSplit

    list_paths = [str(p) for p in Path(datadir).rglob("*.npy")]

    outdir=Path(outdir)
    outdir.mkdir(exist_ok=True, parents=True)

    # labels
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

    labels = [labels_by_sampleid.get(Path(p).stem, "unknown") for p in list_paths]
    print(set(labels))
    tvt_split = TrainValTestSplit(id_labels=list_paths, labels=labels, seed=seed)
    tvt_split(train_size=train_size, balanced_on=labels) # split datasets
    list_train = tvt_split.datasets["id_labels"]["train"]
    list_val   = tvt_split.datasets["id_labels"]["val"]
    list_test  = tvt_split.datasets["id_labels"]["test"]

    labels_train = tvt_split.datasets["labels"]["train"]
    labels_val   = tvt_split.datasets["labels"]["val"]
    labels_test  = tvt_split.datasets["labels"]["test"]

    # with open(outdir.joinpath("summary-split.json"),"w") as fp:
    #     json.dump(tvt_split.get_summary_labels(), fp)

    # # save split
    # with open(outdir.joinpath("split-train-val-test.json"),"w") as fp:
    #     json.dump(tvt_split.datasets, fp, indent=4)
    
    # txt train 
    with open(outdir.joinpath("train.txt"),"w") as fp:
        paths = list_train + list_val
        labels = labels_train + labels_val

        for path, label in zip(paths, labels):
            
            if path_labels:
                sample_id = Path(path).stem
                label = labels_by_sampleid.get(sample_id, "unknown")
                fp.write(f"{path}\t{label}\n") 
            else:
                fp.write(f"{path}\n")
    
    # txt test
    with open(outdir.joinpath("test.txt"),"w") as fp:
        
        for path, label in zip(list_test, labels_test):
            
            if path_labels:
                sample_id = Path(path).stem
                label = labels_by_sampleid.get(sample_id, "unknown")
                fp.write(f"{path}\t{label}\n") 
            else:
                fp.write(f"{path}\n")
    
    print("finished")

@app.command("split-dataset", help="split data intro train, validation and test sets")
def split_train_val_test(
        file_paths_label: Annotated[Path, typer.Option("--file-paths-labels","-f", 
                                                       help="tab separeted txt file with first column the npy path and second column the label")],
        outdir: Annotated[Path, typer.Option("--outdir","-o", mode="w", help="directory to save split results.")],
        train_size: Annotated[float, typer.Option(min=0.01, max=0.99, 
                                                  help="""percentage of data to be used for training. 
                                                  Validation and test will be of size (1-train_size)/2 each.""")] = 0.8,
        seed: Annotated[int, typer.Option("--seed", "-s", 
                                                    help= "to reproduce split of dataset")] = 42,
        min_labels_test: Annotated[int, typer.Option("--min-labels", 
                                                     help="""minimum number of labels of a species to be considered in the test set. 
                                                     If the number of species in the input dataset is less than this, then all data will be used in the training set only""")] = 10,
        ):

    import random
    import pandas as pd
    random.seed(seed)
    outdir = Path(outdir)
    outdir.mkdir(exist_ok=True, parents=True)

    df = pd.read_csv(file_paths_label, sep="\t", header=None, names=["path","label"])
    unique_labels = df["label"].unique()  
    unique_labels.sort()

    for specie in track(unique_labels, description=":dna: split dataset by species"):

        paths_specie = df.query(f"label == '{specie}'")["path"].tolist()
        paths_specie.sort()
        
        if len(paths_specie) > min_labels_test:
            random.shuffle(paths_specie)
            N = len(paths_specie)
            pos_train = int(0.8*N)
            pos_test = int(0.9*N)
            paths_train = paths_specie[:pos_train]
            paths_validation = paths_specie[pos_train:pos_test]
            paths_test = paths_specie[pos_test:]
            # break

            with open(outdir.joinpath("training_list.txt"),"a") as fp:
                for path in paths_train:
                    fp.write(f"{path}\t{specie}\n")

            with open(outdir.joinpath("validation_list.txt"),"a") as fp:
                for path in paths_validation:
                    fp.write(f"{path}\t{specie}\n")

            with open(outdir.joinpath("test_list.txt"),"a") as fp:
                for path in paths_test:
                    fp.write(f"{path}\t{specie}\n")

        # species with less than min_labels_test FCGRs will only be used for training
        else:
            with open(outdir.joinpath("training_list.txt"),"a") as fp:
                for path in paths_specie:
                    fp.write(f"{path}\t{specie}\n")

    print(f":dna: saved results in {outdir}")

@app.command("metric-learning", help="Create embedding using labels in training with the triplet loss")
def train_metric_learning(
        training_list: Annotated[Path, typer.Option(help=".txt file with paths to FCGR in the first column and labels in the second column (tab separated)")],
        validation_list: Annotated[Path, typer.Option(help=".txt file with paths to FCGR in the first column and labels in the second column (tab separated)")],
        kmer: Annotated[int, typer.Option(min=6, help="kmer used to create the FCGR that will be used to train the model.")],
        outdir: Annotated[Path, typer.Option(help="directory to save experiment results")] = "output-training",
        architecture: Annotated[ModelMetricLearning, typer.Option(help="name of the model to be used for training")] = ModelMetricLearning.CNNFCGR.value,
        latent_dim: Annotated[int, typer.Option(min=2, help="number of dimension embedding space")] = 128, 
        hidden_activation: Annotated[Activation,typer.Option(help="activation function for hidden layers")]=Activation.Relu.value,
        batch_normalization: Annotated[bool, typer.Option("--batch-normalization/ ","-bn/ ", help="If set, batch normalization will be applied after each ConvFCGR")]=False,
        preprocessing: Annotated[Preprocessing, typer.Option(help="preprocessing")]=Preprocessing.ScaleZeroOne.value,
        epochs: Annotated[int, typer.Option(min=1)] = 2,
        batch_size: Annotated[int, typer.Option(min=1)] = 256,
        loss: Annotated[LossMetricLearning, typer.Option(help="loss function")] = LossMetricLearning.TripletSemiHard.value,
        margin: Annotated[float, typer.Option(help="margin")] = 1.0, 
        optimizer: Annotated[Optimizer, typer.Option(help="optimizer to train the autoencoder (keras option with default params)")] = Optimizer.Adam.value,
        patiente_early_stopping: Annotated[int, typer.Option()] = 20,
        patiente_learning_rate: Annotated[int, typer.Option()] = 10,
        num_classes_per_batch: Annotated[int, typer.Option(min=1)] = 16,
        path_weights: Annotated[Path, typer.Option(help="pretrained weights/model, eg: path/to/weights.keras")] = None,
        factor_batches: Annotated[int, typer.Option(help="Number of batches per epoch will be multiplied by this number")] = 1,
        weighted_loader: Annotated[bool, typer.Option("--weighted-loader", "-wl",help="If set, batches will be created weightening classes by representatitity, otherwise, random selection will be used.")]=False,
        ) -> None:
    
    """
    train a metric learning approach where batches are balanced by using 'num_classes_per_batch'
    """
    assert batch_size % num_classes_per_batch == 0, "--batch-size must be divisible by --num-classes-per-batch" 
    print(f"Training neural network of type: {architecture.value}")

    # assert any([datadir is not None, training_list is not None]), "Missing INFO: at least one of --datadir or --training-list must be provided."
    import tensorflow as tf
    import tensorflow_addons as tfa
    from .dnn.loaders import DataLoaderMetricLearning as DataLoaders
    from .dnn.loaders.generator_batches import generator_balanced_triplet_batches, generator_balanced_batches
    from .dnn.callbacks import CSVTimeHistory
    from .dnn.models import CNNFCGR, ResNet50
    from collections import defaultdict

    # parameters train
    ARCHITECTURE=architecture
    PATIENTE_EARLY_STOPPING=patiente_early_stopping
    PATIENTE_LEARNING_RATE=patiente_learning_rate

    # folder where to save training results
    PATH_TRAIN=Path(outdir)
    PATH_TRAIN.mkdir(exist_ok=True, parents=True)

    # preprocessing of each FCGR to feed the model 
    if preprocessing == "distribution":
        # sum = 1
        preprocessing = lambda x,y: ( x / tf.math.reduce_sum(x), y )   
    else: 
        # scale [0,1]
        preprocessing = lambda x,y: ( x / tf.math.reduce_max(x), y )

    # ------ data split: training + validation ------

    # From training list
    data_dict_train = defaultdict(list)
    with open(training_list, "r") as fp:
        for line in fp.readlines():
            path, label = line.replace("\n","").strip().split("\t") # first column of the input file 
            data_dict_train[label].append(path)

    # From validation list
    data_dict_validation = defaultdict(list)
    with open(validation_list, "r") as fp:
        for line in fp.readlines():
            path, label = line.replace("\n","").strip().split("\t") # first column of the input file 
            data_dict_validation[label].append(path)

    batches_per_epoch_train = int( sum([len(_) for _ in data_dict_train.values()]) / batch_size)*factor_batches
    batches_per_epoch_validation = int( sum([len(_) for _ in data_dict_validation.values()]) / batch_size)*factor_batches

    generator_train = generator_balanced_batches(data_dict_train, batch_size, num_classes_per_batch, weights=weighted_loader)
    ds_train = tf.data.Dataset.from_generator(
                generator_train,
                output_signature=(tf.TensorSpec((batch_size,2**kmer, 2**kmer, 1), dtype=tf.float32), tf.TensorSpec((batch_size,), dtype=tf.int8)
            ))  

    generator_validation = generator_balanced_batches(data_dict_validation, batch_size, num_classes_per_batch, weights=weighted_loader)
    ds_validation = tf.data.Dataset.from_generator(
                generator_validation,
                output_signature=(tf.TensorSpec((batch_size,2**kmer, 2**kmer, 1), dtype=tf.float32), tf.TensorSpec((batch_size,), dtype=tf.int8)
            ))  

    ds_train = ds_train.prefetch(tf.data.AUTOTUNE)
    ds_validation = ds_validation.prefetch(tf.data.AUTOTUNE)

    ds_train.map(preprocessing, num_parallel_calls=tf.data.AUTOTUNE)
    ds_validation.map(preprocessing, num_parallel_calls=tf.data.AUTOTUNE)

    # - Callbacks: actions that are triggered at the end of each epoch
    # checkpoint: save best weights
    Path(f"{PATH_TRAIN}/checkpoints").mkdir(exist_ok=True, parents=True)
    # TODO: save only weights
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
        min_lr=0.000001
    )

    # stop training if
    cb_earlystop = tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',
        mode='auto',
        # min_delta=0.001,
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
   
    # ---- optimizer ----
    if optimizer.value=="ranger":
        radam = tfa.optimizers.RectifiedAdam()
        ranger = tfa.optimizers.Lookahead(radam, sync_period=6, slow_step_size=0.5)
        optimizer = ranger
    else:
        optimizer=optimizer.value

    # ---- loss function ----
    if loss.value == "triplet_hard_loss":
        print("loss function: triplet hard")
        loss = tfa.losses.TripletHardLoss(margin=margin, distance_metric="L2", soft=False)    
    elif loss.value == "triplet_semihard_loss":
        print("loss function: triplet semihard")
        loss = tfa.losses.TripletSemiHardLoss(margin=margin, distance_metric="L2")
    else:
        raise("undefined loss function")
        # loss = tfa.losses.ContrastiveLoss(margin=margin, )

    # Load and train model
    if ARCHITECTURE == "CNNFCGR":
        model=eval(f"""{ARCHITECTURE}(latent_dim = {latent_dim}, 
                    hidden_activation='{hidden_activation}', 
                    kmer={kmer}, 
                    batch_normalization={batch_normalization},
                    )""")    
    elif ARCHITECTURE == "ResNet50":
        model=eval(f"""{ARCHITECTURE}(latent_dim = {latent_dim}, 
                    hidden_activation='{hidden_activation}', 
                    kmer={kmer},
                    )""")
    else:
        raise Exception("Model not found")
    
    # TODO: load pre-trained weights
    if path_weights is not None:
        print(f"Using pretrained weights from {path_weights}")
        model.load_weights(path_weights)
        # model = tf.keras.models.load_model(path_weights)

    model.compile(optimizer=optimizer, loss=loss,) # metrics=[tfa.metrics.CosineSimilarity(axis=-1)])
    
    model.fit(
        ds_train, 
        steps_per_epoch=batches_per_epoch_train,
        epochs=epochs,
        validation_data=ds_validation, 
        validation_steps=batches_per_epoch_validation,
        callbacks=[
            cb_checkpoint,
            cb_reducelr,
            cb_earlystop,
            cb_csvlogger,
            cb_csvtime
            ],
        workers=8, use_multiprocessing=True, max_queue_size=256
    )


@app.command("one-shot", help="train one-shot model with contrastive loss")
def train_contrastive_model(
        training_list: Annotated[Path, typer.Option(help=".txt file with paths to FCGR in the first column and labels in the second column (tab separated)")],
        validation_list: Annotated[Path, typer.Option(help=".txt file with paths to FCGR in the first column and labels in the second column (tab separated)")],
        kmer: Annotated[int, typer.Option(min=6, help="kmer used to create the FCGR that will be used to train the model.")],
        outdir: Annotated[Path, typer.Option(help="directory to save experiment results")] = "output-training",
        latent_dim: Annotated[int, typer.Option(min=2, help="number of dimension embedding space")] = 128, 
        hidden_activation: Annotated[Activation,typer.Option(help="activation function for hidden layers")]=Activation.Relu.value,
        batch_normalization: Annotated[bool, typer.Option("--batch-normalization/ ","-bn/ ", help="If set, batch normalization will be applied after each ConvFCGR")]=False,
        preprocessing: Annotated[Preprocessing, typer.Option(help="preprocessing")]=Preprocessing.ScaleZeroOne.value,
        epochs: Annotated[int, typer.Option(min=1)] = 2,
        batch_size: Annotated[int, typer.Option(min=1)] = 256,
        # loss: Annotated[LossMetricLearning, typer.Option(help="loss function")] = LossOneShot.Contrastive.value,
        margin: Annotated[float, typer.Option(help="margin for contrastive loss")] = 1.0,
        optimizer: Annotated[Optimizer, typer.Option(help="optimizer to train the autoencoder (keras option with default params)")] = Optimizer.Adam.value,
        patiente_early_stopping: Annotated[int, typer.Option()] = 20,
        patiente_learning_rate: Annotated[int, typer.Option()] = 10,
        path_weights: Annotated[Path, typer.Option(help="pretrained of backbone model trained with triplet loss, eg: path/to/weights.keras")] = None,
        factor_batches: Annotated[int, typer.Option(help="Number of batches per epoch will be multiplied by this number")] = 1,
):

    import tensorflow as tf
    import tensorflow.keras.backend as K
    import tensorflow_addons as tfa
    from .dnn.loaders.generator_batches import (
        generator_one_shot, 
        generator_one_shot_genus, 
        generator_one_shot_genus_mix,
        )
    from .dnn.callbacks import CSVTimeHistory
    from .dnn.models import CNNFCGR
    from .dnn.models.custom_layers.euclidean_distance import EuclideanDistance

    from collections import defaultdict

    # parameters train
    PATIENTE_EARLY_STOPPING=patiente_early_stopping
    PATIENTE_LEARNING_RATE=patiente_learning_rate

    # folder where to save training results
    PATH_TRAIN=Path(outdir)
    PATH_TRAIN.mkdir(exist_ok=True, parents=True)

    # ------- Dataset -------
    # 
    # preprocessing of each FCGR to feed the model 
    if preprocessing == "distribution":
        # sum = 1
        fn_preprocessing = lambda x,y: ( x[0] / tf.math.reduce_sum(x[0]) , x[1] / tf.math.reduce_sum(x[1]) , y)  
    else: 
        # scale [0,1]
        fn_preprocessing = lambda x,y: ( x[0] / tf.math.reduce_max(x[0]) , x[1] / tf.math.reduce_max(x[1]) , y)  

    # From training list
    data_dict_train = defaultdict(list)
    with open(training_list, "r") as fp:
        for line in fp.readlines():
            path, label = line.replace("\n","").strip().split("\t") # first column of the input file 
            data_dict_train[label].append(path)

    # From validation list
    data_dict_validation = defaultdict(list)
    with open(validation_list, "r") as fp:
        for line in fp.readlines():
            path, label = line.replace("\n","").strip().split("\t") # first column of the input file 
            data_dict_validation[label].append(path)

    batches_per_epoch_train = int( sum([len(_) for _ in data_dict_train.values()]) / batch_size)*factor_batches
    batches_per_epoch_validation = int( sum([len(_) for _ in data_dict_validation.values()]) / batch_size)*factor_batches

    generator_train = generator_one_shot(data_dict_train, batch_size, weights=False)
    ds_train = tf.data.Dataset.from_generator(
                generator_train,
                output_signature=(
                                    (tf.TensorSpec((batch_size,2**kmer, 2**kmer, 1), dtype=tf.float32), tf.TensorSpec((batch_size,2**kmer, 2**kmer, 1), dtype=tf.float32)), 
                                    tf.TensorSpec((batch_size,), dtype=tf.float32)
                                )
            )  

    generator_validation = generator_one_shot(data_dict_validation, batch_size, weights=False)
    ds_validation = tf.data.Dataset.from_generator(
                generator_validation,
                output_signature=(
                                    (tf.TensorSpec((batch_size,2**kmer, 2**kmer, 1), dtype=tf.float32), tf.TensorSpec((batch_size,2**kmer, 2**kmer, 1), dtype=tf.float32)), 
                                    tf.TensorSpec((batch_size,), dtype=tf.float32)
                                )
            )  

    ds_train = ds_train.prefetch(tf.data.AUTOTUNE)
    ds_validation = ds_validation.prefetch(tf.data.AUTOTUNE)

    # # apply preprocessing
    ds_train.map(fn_preprocessing, num_parallel_calls=tf.data.AUTOTUNE)
    ds_validation.map(fn_preprocessing, num_parallel_calls=tf.data.AUTOTUNE)

    # ----- Model ------
    # 
    # Load embedding model
    embedding_model=CNNFCGR(
                latent_dim=latent_dim, 
                hidden_activation=hidden_activation, 
                kmer=kmer, 
                batch_normalization=batch_normalization,
                )

    if path_weights is not None:
        print(f"Using pretrained weights from {path_weights}")
        embedding_model.load_weights(path_weights)


    # one_shot model
    rows = 2**kmer
    cols = rows
    input_1 = tf.keras.layers.Input(shape=(rows,cols,1), name="input_1")
    input_2 = tf.keras.layers.Input(shape=(rows,cols,1), name="input_2")

    tower_1 = embedding_model(input_1)
    tower_2 = embedding_model(input_2)

    emb_1 = tf.keras.layers.Identity(False, name="output_1")(tower_1)
    emb_2 = tf.keras.layers.Identity(False, name="output_2")(tower_2)
    
    edist = EuclideanDistance()([emb_1, emb_2])

    normal_layer = tf.keras.layers.BatchNormalization()(edist)
    output_layer = tf.keras.layers.Dense(1, activation="sigmoid")(normal_layer)

    one_shot_model = tf.keras.models.Model(inputs=[input_1, input_2], outputs=output_layer)

    # ------ Callbacks ------
    # actions that are triggered at the end of each epoch

    # checkpoint: save best weights
    Path(f"{PATH_TRAIN}/checkpoints").mkdir(exist_ok=True, parents=True)
    # TODO: save only weights
    cb_checkpoint = tf.keras.callbacks.ModelCheckpoint(
        filepath=f'{PATH_TRAIN}/checkpoints/weights-one-shot.keras',
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
        min_lr=0.000001
    )

    # stop training if
    cb_earlystop = tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',
        mode='auto',
        # min_delta=0.001,
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
   
    # ---- optimizer ----
    if optimizer.value=="ranger":
        radam = tfa.optimizers.RectifiedAdam()
        ranger = tfa.optimizers.Lookahead(radam, sync_period=6, slow_step_size=0.5)
        optimizer = ranger
    else:
        optimizer=optimizer.value

    loss = tfa.losses.ContrastiveLoss(margin=margin,)

    one_shot_model.compile(optimizer=optimizer, loss=loss,)
    
    one_shot_model.fit(
        ds_train, 
        steps_per_epoch=batches_per_epoch_train,
        epochs=epochs,
        validation_data=ds_validation, 
        validation_steps=batches_per_epoch_validation,
        callbacks=[
            cb_checkpoint,
            cb_reducelr,
            cb_earlystop,
            cb_csvlogger,
            cb_csvtime
            ],
        workers=8, use_multiprocessing=True, max_queue_size=256
    )

@app.command("extract-backbone-one-shot", help="get embedding model from siamese network trained with contrastive loss")
def extract_backbone_one_shot_model(
            path_model: Annotated[Path, typer.Option(help="trained siamese network with contrastive loss, eg: path/to/checkpoint.keras")],
            path_save: Annotated[Path, typer.Option(help="path to save backbone model to output embeddings, eg: path/to/model.keras")]
            ):
    
    import tensorflow as tf 
    from .dnn.models.custom_layers.euclidean_distance import EuclideanDistance

    print(f"Loading siamese network from {path_model}")

    siamese = tf.keras.models.load_model(path_model, custom_objects={"EuclideanDistance": EuclideanDistance})    
    embedding_input = siamese.get_layer("input_1").input
    embedding_output = siamese.get_layer("output_1").output

    embedding_extractor = tf.keras.models.Model(inputs=embedding_input, outputs=embedding_output)

    print(f"Saving embedding model to {path_save}")
    embedding_extractor.save(path_save)