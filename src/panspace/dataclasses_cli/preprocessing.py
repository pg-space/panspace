from enum import Enum

class Preprocessing(str,Enum):
    Distribution="distribution"
    ScaleZeroOne="scale_zero_one"
    Clip="clip"
    # ScaleZeroOne_Clip="scale_zero_one_clip"
    Clip_ScaleZeroOne="clip_scale_zero_one"