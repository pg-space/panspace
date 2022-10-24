import tensorflow as tf
# TODO: to functional API

def DenseAutoencoder(latent_dim: int = 100):

  # Encoder
  input_enc = tf.keras.layers.Input(shape=(64,64,1))
  x = tf.keras.layers.Flatten()(input_enc)
  emb = tf.keras.layers.Dense(latent_dim, activation="relu")

  # Decoder
  x = tf.keras.layers.Dense(64 * 64, activation="relu")(emb)
  out_dec = tf.keras.layers.Reshape((64,64,1))

  autoencoder = tf.keras.models.Model(inputs=input_enc, outputs=out_dec)

  return autoencoder