"""
FCGR autoencoder
"""
import tensorflow as tf
from .custom_layers import ConvFCGR, DeConvFCGR
from tensorflow.keras.layers import Conv2D, Conv2DTranspose

def AutoencoderFCGR(latent_dim: int = 100, 
                    output_activation="sigmoid", 
                    hidden_activation="relu", 
                    kmer: int = 6, 
                    batch_normalization: bool = True,
                    ):
    
    rows = 2**kmer
    cols = rows

    # Encoder 
    input_enc = tf.keras.layers.Input(shape=(rows,cols,1), name="input_encoder")

    l=kmer # input 2^kmer x 2^kmer  x 1 
    while l > 4: # there are 256 4-mers, and 64 3-mers, so we stop at for to feed the n-dimensional space (n < 200)
        filters = l*4 # channels / independent features in depth
        kernel_size=2
        stride=2
        x = Conv2D(filters=filters, kernel_size=kernel_size, strides=stride, activation=hidden_activation, padding='valid')(input_enc) if l==kmer else  Conv2D(filters=filters, kernel_size=kernel_size, strides=stride, padding='valid')(x) #ConvFCGR(filters=filters,levels=1)(input_enc) if l==kmer else ConvFCGR(filters=filters,levels=1)(x)
        if batch_normalization:
            x = tf.keras.layers.BatchNormalization(axis=-1)(x)
        l -=1

    # Embedding Space
    x = tf.keras.layers.Flatten()(x)
    x = tf.keras.layers.Dense(latent_dim, activation=hidden_activation, name="output_dense")(x)
    x = tf.math.l2_normalize(x, axis=1,)   # Embedding: L2 normalization layer
    emb = tf.keras.layers.Identity(False, name="output_encoder")(x)

    # adaptation to feed Decoder
    # start reconstruction with 2^4 x 2^4
    filters=4
    x = tf.keras.layers.Dense(16 * 16 * filters , activation="relu", name="input_decoder")(emb)
    x = tf.keras.layers.Reshape((16, 16, filters))(x) # output (16,16,4)

    l=4 
    while l < kmer-1: 
        filters = l*4
        x =  Conv2DTranspose(filters=filters, kernel_size=(2,2), strides=(2,2), activation=hidden_activation, padding='valid')(x)# DeConvFCGR(filters=filters,levels=1)(x)
        if batch_normalization:
            x = tf.keras.layers.BatchNormalization(axis=-1)(x)
        l +=1

    out_dec = Conv2DTranspose(filters=1, kernel_size=(2,2), strides=(2,2))(x) # output (2^kmer,2^kmer, 1)
    out_dec = eval(f"tf.keras.activations.{output_activation}(out_dec)")
    autoencoder = tf.keras.models.Model(inputs=input_enc, outputs=out_dec, name="output_decoder")

    return autoencoder