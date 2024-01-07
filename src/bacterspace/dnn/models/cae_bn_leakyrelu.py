"CAE with Batch Normalization and LeakyReLU as activation function instead of relu"
import tensorflow as tf

def CNNAutoencoderCAEBNLeakyRelu(latent_dim: int = 100):

  # Encoder 
  input_enc = tf.keras.layers.Input(shape=(64,64,1), name="input_encoder")
  x = tf.keras.layers.Conv2D(filters=16, kernel_size=(3,3), strides=1, padding="same", activation=None)(input_enc) # output (62,62,16)
  x = tf.keras.layers.BatchNormalization(axis=-1)(x)
  x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
  x = tf.keras.layers.Conv2D(filters=32, kernel_size=(3,3), strides=1, padding="same", activation=None)(x) # output (60,60,32)
  x = tf.keras.layers.BatchNormalization(axis=-1)(x)
  x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
  x = tf.keras.layers.Conv2D(filters=64, kernel_size=(3,3), strides=2, padding="same", activation=None)(x) # output (29,29,64)
  x = tf.keras.layers.BatchNormalization(axis=-1)(x)
  x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
  x = tf.keras.layers.Conv2D(filters=128, kernel_size=(3,3), strides=1, padding="same", activation=None)(x) # output (27,27,128)
  x = tf.keras.layers.BatchNormalization(axis=-1)(x)
  x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
  x = tf.keras.layers.Flatten()(x)
  emb = tf.keras.layers.Dense(latent_dim, activation=None, name="output_encoder")(x)
  x = tf.keras.layers.LeakyReLU(alpha=0.1)(emb)

  # Decoder
  x = tf.keras.layers.Dense(27 * 27 * 128 , activation=None, name="input_decoder")(emb)
  x = tf.keras.layers.Reshape((27, 27, 128))(x) # output (27,27,128)
  x = tf.keras.layers.BatchNormalization(axis=-1)(x)
  x = tf.keras.layers.Conv2DTranspose(filters=64, kernel_size=(3,3), strides=1, activation=None)(x) # output (29,29,64)
  x = tf.keras.layers.BatchNormalization(axis=-1)(x)
  x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
  x = tf.keras.layers.Conv2DTranspose(filters=32, kernel_size=(3,3), strides=2, activation=None)(x) # output (59,59,32)
  x = tf.keras.layers.BatchNormalization(axis=-1)(x)
  x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
  x = tf.keras.layers.Conv2DTranspose(filters=16, kernel_size=(3,3), strides=1, activation=None)(x) # output (61,61,16)
  x = tf.keras.layers.BatchNormalization(axis=-1)(x)
  x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
  out_dec = tf.keras.layers.Conv2DTranspose(filters=1, kernel_size=(4,4), strides=1, activation="sigmoid", name="output_decoder")(x) # output (64,64,1) 

  autoencoder = tf.keras.models.Model(inputs=input_enc, outputs=out_dec)

  return autoencoder