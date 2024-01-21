"Add batch normalization"
import tensorflow as tf

def CNNAutoencoderBN(latent_dim: int = 100, output_activation="sigmoid", hidden_activation="relu"):

  # Encoder 
  input_enc = tf.keras.layers.Input(shape=(64,64,1), name="input_encoder")
  x = tf.keras.layers.Conv2D(filters=32, kernel_size=(3,3), strides=2, padding="same", activation=hidden_activation)(input_enc)
  x = tf.keras.layers.BatchNormalization(axis=-1)(x)
  x = tf.keras.layers.Conv2D(filters=64, kernel_size=(3,3), strides=2, padding="same", activation=hidden_activation)(x)
  x = tf.keras.layers.BatchNormalization(axis=-1)(x)
  x = tf.keras.layers.Flatten()(x)
  emb = tf.keras.layers.Dense(latent_dim, activation=hidden_activation, name="output_encoder")(x)

  # Decoder
  x = tf.keras.layers.Dense(16 * 16 * 64 , activation=hidden_activation, name="input_decoder")(emb)
  x = tf.keras.layers.Reshape((16, 16, 64))(x) # output (16,16,64)
  x = tf.keras.layers.BatchNormalization(axis=-1)(x)
  x = tf.keras.layers.Conv2DTranspose(filters=32, kernel_size=(2,2), strides=2, activation=hidden_activation)(x)  # output (32,32,32)
  x = tf.keras.layers.BatchNormalization(axis=-1)(x)
  # out_dec = tf.keras.layers.Conv2DTranspose(filters=1, kernel_size=(2,2), strides=2, activation=hidden_activation, name="output_decoder")(x)   # output (64,64,1) 
  out_dec = tf.keras.layers.Conv2DTranspose(filters=1, kernel_size=(2,2), strides=2, activation=output_activation, name="output_decoder")(x)   # output (64,64,1), values in [0,1] 

  autoencoder = tf.keras.models.Model(inputs=input_enc, outputs=out_dec)

  return autoencoder