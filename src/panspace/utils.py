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
    Ranger="ranger"
    
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


import re
import statistics
from pathlib import Path
from datetime import datetime
from collections import namedtuple,defaultdict

MESSAGES_USRBINTIME = [
    "User time (seconds)",
    "System time (seconds)",
    "Elapsed (wall clock) time (h:mm:ss or m:ss)",
    "Maximum resident set size (kbytes)"
]

class LogInfo:
    def __init__(self,):
        self.messages = MESSAGES_USRBINTIME
    
    def __call__(self, path_log: str) -> None:
        lines = self.load_lines(path_log)
        info  = self.usrbintime_info(lines)
        return info

    def load_lines(self,path_log):
        
        lines = []
        
        with open(path_log) as fp:
            
            for line in fp.readlines():
                for l in line.split(":"):
                    if any([message in l for message in self.messages]):
                        lines.append(line)
        return lines
    
    def usrbintime_info(self, lines):
        usrbintime = dict()
        for line in lines:
            # print(line)
            # if any([message in line for message in MESSAGES_USRBINTIME]):
            feat, value = line.replace("\t","").replace("\n","").split(": ")
            feat = feat.strip()
            value = value.strip()
            if "m:ss" in feat:
                try: 
                    # m:s
                    minutes, seconds = value.split(":")
                    value = int(minutes)*60 + float(seconds)
                except: 
                    # h:m:s
                    hours, minutes, seconds = value.split(":")
                    value = int(hours)*3600 + int(minutes)*60 + float(seconds)
                
                feat = feat + " (seconds)"

            usrbintime[feat] = float(value)

        return usrbintime

    def summarize_directory(self, dir_logs: str, pattern: str = "*.log") -> dict:
        "aggregate usrbintime info (mean, std, min, max, sum) across all .log files in a directory"
        per_feat = defaultdict(list)

        for path_log in sorted(Path(dir_logs).glob(pattern)):
            info = self(str(path_log))
            for feat, value in info.items():
                per_feat[feat].append(value)

        summary = dict()
        for feat, values in per_feat.items():
            summary[feat] = {
                "count": len(values),
                "mean": statistics.mean(values),
                "std": statistics.stdev(values) if len(values) > 1 else 0.0,
                "min": min(values),
                "max": max(values),
                "sum": sum(values),
            }
        return summary
