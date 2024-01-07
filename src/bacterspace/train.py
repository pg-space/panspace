from enum import Enum
import typer
from typing_extensions import Annotated
from typing import Optional

# import yaml
import json

import numpy as np
from pathlib import Path

import logging 
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = typer.Typer(rich_markup_mode="rich")

# For typer
class Autoencoder(str, Enum):
    DenseAutoencoder="DenseAutoencoder"
    CNNAutoencoder="CNNAutoencoder"
    CNNAutoencoderBN="CNNAutoencoderBN" 
    CNNAutoencoderCAE="CNNAutoencoderCAE"
    CNNAutoencoderCAEBN="CNNAutoencoderCAEBN"
    CNNAutoencoderCAEBNLeakyRelu="CNNAutoencoderCAEBNLeakyRelu"
    CNNAutoencoderCAEBNL2Emb="CNNAutoencoderCAEBNL2Emb"

class Optimizer(str, Enum):
    Adam="adam"
    SGD="SGD"
    RMSprop="rmsprop"
    AdamW="adamw"
    Adadelta="adadelta"
    Adagrad="adagrad"
    Adamax="adamax"
    Adafactor="adafactor"
    Nadam="nadam"
    
@app.command()
def train(
        datadir: Annotated[Path, typer.Option(help="directory where FCGR with numpy files are stored")],
        outdir: Annotated[Path, typer.Option(help="directory to save experiment results")],
        autoencoder: Annotated[Autoencoder, typer.Option(help="name of autoencoder to use for training")] = Autoencoder.CNNAutoencoderCAEBN.value,
        latent_dim: Annotated[int, typer.Option(min=2, help="number of dimension embedding space")] = 100, 
        kmer: Annotated[int, typer.Option(min=1)] = 6,
        epochs: Annotated[int, typer.Option(min=1)] = 50,
        batch_size: Annotated[int, typer.Option(min=1)] = 16,
        optimizer: Annotated[Optimizer, typer.Option(help="optimizer to train the autoencoder (keras option with default params)")] = Optimizer.Adam.value,
        patiente_early_stopping: Annotated[int, typer.Option()] = 20,
        patiente_learning_rate: Annotated[int, typer.Option()] = 10,
        train_size: Annotated[float, typer.Option(min=0.01, max=0.99)] = 0.8,
        seed: Annotated[int, typer.Option(help= "to reproduce split of dataset")] = 42,
        ):
    print(f"Training neural network of type: {autoencoder.value}")


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
        )
    from .dnn.callbacks import CSVTimeHistory
    from .dnn.utils.split_data import TrainValTestSplit

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
    preprocessing = lambda x: x / x.max() 

    # parameters dataset
    PATH_FCGR=Path(datadir) #Path(OUTDIR).joinpath(f"{KMER}mer/fcgr")

    ## Create train-val-test datasets
    label_from_path=lambda path: Path(path).parent.stem.split("__")[0]

    # paths to fcgr 
    list_npy = [p for p in Path(PATH_FCGR).rglob('*/*.npy') if "dustbin" not in str(p) and "__01" in str(p)]
    # print(len(list_npy))
    labels = [label_from_path(path) for path in list_npy]#[:1000]
    from collections import Counter; print(Counter(labels))
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
        # filepath='../data/train/checkpoints/weights-{epoch:02d}-{val_loss:.3f}.hdf5',
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

    # Load and train model
    autoencoder=eval(f"{ARCHITECTURE}(LATENT_DIM)")
    autoencoder.compile(optimizer=optimizer.value, loss="binary_crossentropy")
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