import yaml
import json
import tensorflow as tf
import numpy as np
from pathlib import Path

from dnn.loaders.VARdataloader import DataLoaderVAR as DataLoader
from dnn.models import (
    DenseAutoencoder,
    CNNAutoencoder,
    CNNAutoencoderBN, 
    CNNAutoencoderCAE,
    CNNAutoencoderCAEBN,
    CNNAutoencoderCAEBNLeakyRelu,
    CNNAutoencoderCAEBNL2Emb,
    )
from dnn.callbacks import CSVTimeHistory
from dnn.utils.split_data import TrainValTestSplit

## Params
with open("params.yaml") as fp:
    params = yaml.load(fp, Loader=yaml.FullLoader)
OUTDIR=params["outdir"]

# parameters train
LATENT_DIM=params['train']['latent_dim']
EPOCHS=params['train']['epochs']
BATCH_SIZE=params['train']['batch_size']
ARCHITECTURE=params['train']['architecture']
PATIENTE_EARLY_STOPPING=params['train']['patiente_early_stopping']
PATIENTE_LEARNING_RATE=params['train']['patiente_learning_rate']
TRAIN_SIZE=params['train']['train_size']
SEED=params['seed']

# folder where to save training results
PATH_TRAIN = Path(f"{OUTDIR}/train/")
PATH_TRAIN.mkdir(exist_ok=True, parents=True)

# preprocessing of each FCGR to feed the model 
preprocessing = lambda x: x / x.max() 

# parameters dataset
PATH_FCGR=Path(params['outdir']).joinpath("fcgr")

## Create train-val-test datasets
label_from_path=lambda path: Path(path).parent.stem.split("__")[0]

# paths to fcgr 
list_npy = list(Path(PATH_FCGR).rglob('*.npy'))
labels = [label_from_path(path) for path in list_npy]
tvt_split = TrainValTestSplit(id_labels=list_npy, labels=labels, seed=SEED)
tvt_split(train_size=TRAIN_SIZE, balanced_on=labels)# split datasets
list_train = tvt_split.datasets["id_labels"]["train"]
list_val   = tvt_split.datasets["id_labels"]["val"]
list_test   = tvt_split.datasets["id_labels"]["test"]


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
Path(f"{OUTDIR}/train/checkpoints").mkdir(exist_ok=True, parents=True)
cb_checkpoint = tf.keras.callbacks.ModelCheckpoint(
    # filepath='../data/train/checkpoints/weights-{epoch:02d}-{val_loss:.3f}.hdf5',
    filepath=f'{OUTDIR}/train/checkpoints/weights-{ARCHITECTURE}.hdf5',
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
    filename=f'{OUTDIR}/train/training_log.csv',
    separator='\t',
    append=False
)

# save time by epoch
cb_csvtime = CSVTimeHistory(
    filename=f'{OUTDIR}/train/time_log.csv',
    separator='\t',
    append=False
)

# Load and train model
autoencoder=eval(f"{ARCHITECTURE}(LATENT_DIM)")
autoencoder.compile(optimizer='adam', loss="binary_crossentropy")
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

# Encoder-Decoder
encoder = tf.keras.models.Model(autoencoder.input,autoencoder.get_layer("output_encoder").output)
decoder = tf.keras.models.Model(autoencoder.get_layer("input_decoder").input, autoencoder.output)

# save encoder and decoder
path_save_models = Path(f"{OUTDIR}/models")
encoder.save(path_save_models.joinpath("encoder"))
decoder.save(path_save_models.joinpath("decoder"))

# compute embeddings
trainval_data = DataLoader(
    list_paths=list_train + list_val,
    batch_size=10,
    shuffle=False,
    preprocessing=preprocessing,
    inference_mode=True
)

# embeddings train+val
embeddings = []
for data in iter(trainval_data):
    encoded_imgs = encoder(data).numpy()
    embeddings.append(encoded_imgs)

all_emb = np.concatenate(embeddings, axis=0)
assert len(all_emb) == len(list_train+list_val), "embeddings and ids does not match"
# save embeddings
path_emb = Path(f"{OUTDIR}/faiss-embeddings")
path_emb.mkdir(exist_ok=True, parents=True)
np.save(file=path_emb.joinpath("embeddings.npy"), arr=all_emb)
with open(path_emb.joinpath("id_embeddings.json"), "w") as fp:
    json.dump({j: str(p) for j,p in enumerate(list_train+list_val)}, fp, indent=4)

# embeddings test set
test_data = DataLoader(
    list_paths=list_test,
    batch_size=10,
    shuffle=False,
    preprocessing=preprocessing,
    inference_mode=True
)

embeddings = []
for data in iter(test_data):
    encoded_imgs = encoder(data).numpy()
    embeddings.append(encoded_imgs)

all_emb = np.concatenate(embeddings, axis=0)
assert len(all_emb) == len(list_test), "embeddings and ids does not match"
# save embeddings
path_emb = Path(f"{OUTDIR}/faiss-embeddings")
path_emb.mkdir(exist_ok=True, parents=True)
np.save(file=path_emb.joinpath("query_embeddings.npy"), arr=all_emb)
with open(path_emb.joinpath("query_embeddings.json"), "w") as fp:
    json.dump({j: str(p) for j,p in enumerate(list_test)}, fp, indent=4)