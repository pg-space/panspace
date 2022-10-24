"Load data to the model (Same as dataset.py but with keras)"
from typing import List, Union, Callable, Optional
from pathlib import Path
import numpy as np
import tensorflow as tf

class DataLoaderVAR(tf.keras.utils.Sequence):
    """Data Loader for keras from a list of paths to files""" 

    def __init__(self, 
                list_paths: List[Union[str, Path]], 
                batch_size: int = 8,
                shuffle: bool = True,      
                preprocessing: Optional[Callable] = None,
                inference_mode: bool = False
                ):
        self.list_paths = list_paths
        self.batch_size = batch_size 
        self.shuffle = shuffle
        self.preprocessing = preprocessing if callable(preprocessing) else lambda x: x
        self.inference_mode= inference_mode
        # initialize first batch
        self.on_epoch_end()

    def on_epoch_end(self,):
        """Updates indexes after each epoch (starting for the epoch '0')"""
        self.indexes = np.arange(len(self.list_paths))
        if self.shuffle == True:
            np.random.shuffle(self.indexes) # shuffle indexes in place

    def __len__(self):
        # Must be implemented
        """Denotes the number of batches per epoch"""
        delta = 1 if len(self.list_paths) % self.batch_size else 0 
        return len(self.list_paths) // self.batch_size + delta

    def __getitem__(self, index):
        # Must be implemented
        """To feed the model with data in training
        It generates one batch of data
        """
        # Generate indexes of the batch
        indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]

        # Find list of paths to ecg
        list_paths_temp = [self.list_paths[k] for k in indexes]

        # Generate data
        X = self.batch_generation(list_paths_temp)

        if self.inference_mode is True:
            return X
        return X, X
    
    def batch_generation(self, list_path_temp: List[str]): 
        """Generates and augment data containing batch_size samples
        Args:
            list_path_temp (List[str]): sublist of list_path
        Returns:
            X : numpy.array
            y : numpy.array hot-encoding
        """ 
        X_batch = []
        for path in list_path_temp: 
            npy = np.load(path)
            npy = self.preprocessing(npy)
            npy = np.expand_dims(npy, axis=-1)# add channel dimension
            X_batch.append(np.expand_dims(npy,axis=0)) # add to list with batch dims
            
        return np.concatenate(X_batch, axis=0)