from enum import Enum 

class Loss(str, Enum):
    BinaryCrossEntropy="binary_crossentropy"
    MSE="mean_squared_error"
    CategoricalCrossEntropy="categorical_crossentropy"

