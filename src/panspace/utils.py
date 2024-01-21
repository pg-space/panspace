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
    AutoencoderFCGR="AutoencoderFCGR"

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

class Loss(str, Enum):
    BinaryCrossEntropy="binary_crossentropy"
    MSE="mean_squared_error"
    CategoricalCrossEntropy="categorical_crossentropy"

class Activation(str,Enum):
    Sigmoid="sigmoid"
    Softmax="softmax"
    Relu="relu"
    LeakyRelu="leakyrealu"

class Preprocessing(str,Enum):
    Distribution="distribution"
    ScaleZeroOne="scale_zero_one"