import tensorflow as tf
import time

class CSVTimeHistory(tf.keras.callbacks.Callback):
    def __init__(self, filename, separator=",", append=False): 
        self.filename=filename
        self.separator=separator
        self.append=append

    def on_train_begin(self, logs={}):
        self.times = []
        self.epoch = 1

        mode_writting = "w" if self.append is False else "a"
        with open(self.filename, mode_writting) as fp:
            fp.write("epoch" + self.separator + "secs" + "\n")

    def on_epoch_begin(self, batch, logs={}):
        self.epoch_time_start = time.time()

    def on_epoch_end(self, batch, logs={}):
        self.times.append(time.time() - self.epoch_time_start)
        self.write_time(self.epoch, self.times[-1])        
        self.epoch += 1
    
    def write_time(self,epoch,time):
        with open(self.filename,"a") as fp:
            fp.write(str(epoch) + self.separator + str(time) + "\n")