from enum import Enum

class ModelMetricLearning(str, Enum):
    CNNFCGR="CNNFCGR",
    CNNFCGR_Dropout="CNNFCGR_Dropout",
    ResNet50="ResNet50",
    CNNFCGR_Levels="CNNFCGR_Levels",
