from enum import Enum 

class Activation(str,Enum):
    Sigmoid="sigmoid"
    Softmax="softmax"
    Relu="relu"
    LeakyRelu="leakyrealu"