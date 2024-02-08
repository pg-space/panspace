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
from panspace.dataclasses_cli import (
    ModelMetricLearning, 
    Optimizer, 
    LossMetricLearning, 
    Activation, 
    Preprocessing,
)

from pathlib import Path

def train_metric_learning(
        outdir: Annotated[Path, typer.Option(help="directory to save experiment results")],
        training_list: Annotated[Path, typer.Option(help=".txt file with paths to FCGR in the first column and labels in the second column (tab separated)")] = None,
        architecture: Annotated[ModelMetricLearning, typer.Option(help="name of the model to be used for training")] = ModelMetricLearning.CNNFCGR.value,
        latent_dim: Annotated[int, typer.Option(min=2, help="number of dimension embedding space")] = 100, 
        kmer: Annotated[int, typer.Option(min=1)] = 6,
        hidden_activation: Annotated[Activation,typer.Option(help="activation function for hidden layers")]=Activation.Relu.value,
        batch_normalization: Annotated[bool, typer.Option("--batch-normalization/ ","-bn/ ", help="If set, batch normalization will be applied after each ConvFCGR and DeConvFCGR")]=False,
        preprocessing: Annotated[Preprocessing, typer.Option(help="preprocessing")]=Preprocessing.Distribution.value,
        epochs: Annotated[int, typer.Option(min=1)] = 2,
        batch_size: Annotated[int, typer.Option(min=1)] = 64,
        loss: Annotated[LossMetricLearning, typer.Option(help="loss function")] = LossMetricLearning.Contrastive.value,
        optimizer: Annotated[Optimizer, typer.Option(help="optimizer to train the autoencoder (keras option with default params)")] = Optimizer.Adam.value,
        patiente_early_stopping: Annotated[int, typer.Option()] = 20,
        patiente_learning_rate: Annotated[int, typer.Option()] = 10,
        train_size: Annotated[float, typer.Option(min=0.01, max=0.99)] = 0.8,
        seed: Annotated[int, typer.Option(help= "to reproduce split of dataset")] = 42,
        ) -> None:
    print(f"Training neural network of type: {model.value}")

    # assert any([datadir is not None, training_list is not None]), "Missing INFO: at least one of --datadir or --training-list must be provided."
    import tensorflow as tf
    import tensorflow_addons as tfa
    from panspace.dnn.loaders import DataLoaderMetricLearning as DataLoader
    from panspace.dnn.callbacks import CSVTimeHistory
    from panspace.dnn.models.metric_learning import CNNFCGR

    KMER=kmer

    # parameters train
    LATENT_DIM=latent_dim
    EPOCHS=epochs
    BATCH_SIZE=batch_size
    ARCHITECTURE=architecture
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

    # From training list
    list_paths = []
    list_labels = []
    with open(training_list, "r") as fp:
        for line in fp.readlines():
            path, label = line.replace("\n","").strip().split("\t") # first column of the input file 
            if path.endswith(".npy"): 
                list_paths.append(path)
                list_labels.append(label)

    N_paths = len(list_paths)
    pos_cut = int(N_paths*train_size)
    list_train = list_paths[:pos_cut]
    labels_train = list_labels[:pos_cut]
    list_val   = list_paths[pos_cut:]
    labels_val = list_labels[pos_cut:]

    # ------ training -----
        
    # dataset train
    ds_train = DataLoader(
        list_paths=list_train,
        list_labels=labels_train,
        batch_size=BATCH_SIZE,
        shuffle=True,
        preprocessing=preprocessing
    )

    # dataset validation
    ds_val = DataLoader(
        list_paths=list_val,
        list_labels=labels_val,
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
   
    # ---- optimizer ----
    if optimizer.value=="ranger":
        
        radam = tfa.optimizers.RectifiedAdam()
        ranger = tfa.optimizers.Lookahead(radam, sync_period=6, slow_step_size=0.5)
        optimizer = ranger
    else:
        optimizer=optimizer.value

    # ---- loss function ----
    if loss.value == "triplet_hard":
        loss = tfa.losses.TripletHard()    
    elif loss.value == "triplet_semihard_loss": 
        loss = tfa.losses.TripletSemiHardLoss()
    else:
        loss = tfa.losses.ContrastiveLoss()
    

    # Load and train model
    model=eval(f"""{ARCHITECTURE}(latent_dim = {LATENT_DIM}, 
                hidden_activation='{hidden_activation}', 
                kmer={kmer}, 
                batch_normalization={batch_normalization},
                )""")    
    
    model.compile(optimizer=optimizer, loss=loss)
    
    model.fit(
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