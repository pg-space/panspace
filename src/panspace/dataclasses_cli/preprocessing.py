from enum import Enum

class Preprocessing(str,Enum):
    Distribution="distribution"
    ScaleZeroOne="scale_zero_one"