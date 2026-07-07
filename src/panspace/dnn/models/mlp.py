"""
Simple multilayer perceptron (MLP) architecture for learning an embedding space from FCGR images.

Last layer is a n-dimensional dense layer L2 normalized
Loss functions to be used with it:
- contrastive loss
- triplet loss
"""

import tensorflow as tf

def MLP(latent_dim: int = 128,
            hidden_activation="relu",
            kmer: int = 6,
            batch_normalization: bool = True,
            level: int = 1,
            ):

    # Input layer (2**k x 2**k x 1)
    rows = 2**kmer
    cols = rows
    input_ = tf.keras.layers.Input(shape=(rows,cols,1), name="input_encoder")

    # Embedding Space
    x = tf.keras.layers.Flatten()(input_)
    x = tf.keras.layers.Dense(latent_dim, activation=hidden_activation, name="output_dense")(x)
    emb = tf.math.l2_normalize(x, axis=1)   # Embedding: L2 normalization layer

    mlp_fcgr = tf.keras.models.Model(inputs=input_, outputs=emb, name="output")

    return mlp_fcgr
