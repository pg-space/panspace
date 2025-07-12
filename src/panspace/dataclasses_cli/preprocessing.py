from enum import Enum

class Preprocessing(str,Enum):
    Distribution="distribution"
    ScaleZeroOne="scale_zero_one"
    Clip="clip"
    Clip_ScaleZeroOne="clip_scale_zero_one"