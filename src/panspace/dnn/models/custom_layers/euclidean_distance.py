from tensorflow.keras.layers import Layer
import tensorflow.keras.backend as K


class EuclideanDistance(Layer):
    def call(self, inputs):
        x, y = inputs
        sum_square = K.sum(K.square(x - y), axis=1, keepdims=True)
        return K.sqrt(K.maximum(sum_square, K.epsilon()))