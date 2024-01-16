"dataclasses to use with Typer for CLI options commands"
from enum import Enum 

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