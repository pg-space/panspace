"""
CNN FCGR

Last layer is a n-dimensional dense layer L2 normalized
Loss functions to be used with it: 
- contrastive loss
- triplet loss
"""

import tensorflow as tf
from tensorflow.keras.layers import Conv2D

def CNNFCGR(latent_dim: int = 128, 
            hidden_activation="relu", 
            kmer: int = 6, 
            batch_normalization: bool = True,
            level: int = 1,
            ):

    # Input layer (2**k x 2**k x 1)    
    rows = 2**kmer
    cols = rows
    input_ = tf.keras.layers.Input(shape=(rows,cols,1), name="input_encoder")
    x = input_
    
    kernel_size = 2**level
    stride = 2**level

    small_kmer=kmer # input 2^kmer x 2^kmer  x 1 
    while small_kmer >= 4: # there are 256 4-mers, and 64 3-mers, so we stop at for to feed the n-dimensional space (n < 200)
        filters = 4*(small_kmer) # channels / independent features in depth
        
        x = Conv2D(filters=filters, kernel_size=kernel_size, strides=stride, activation=hidden_activation, padding='valid')(x) 
            
        if batch_normalization:
            x = tf.keras.layers.BatchNormalization(axis=-1)(x)
        small_kmer -=1

    # Embedding Space
    x = tf.keras.layers.Flatten()(x)
    x = tf.keras.layers.Dense(latent_dim, activation=hidden_activation, name="output_dense")(x)
    emb = tf.math.l2_normalize(x, axis=1,)   # Embedding: L2 normalization layer
    
    cnn_fcgr = tf.keras.models.Model(inputs=input_, outputs=emb, name="output")

    return cnn_fcgr