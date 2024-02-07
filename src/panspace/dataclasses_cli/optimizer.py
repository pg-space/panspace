from enum import Enum

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
    Ranger="ranger"