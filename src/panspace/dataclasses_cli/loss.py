from enum import Enum 

class LossAutoencoder(str, Enum):
    BinaryCrossEntropy="binary_crossentropy"
    MSE="mean_squared_error"
    CategoricalCrossEntropy="categorical_crossentropy"

class LossMetricLearning(str,Enum):
    Contrastive="contrastive_loss"
    TripletSemiHard="triplet_semihard_loss"
    TripletHard="triplet_hard_loss"