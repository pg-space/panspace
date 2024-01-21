# from tensorflow.keras.layers import Layer, Conv2D
import tensorflow as tf

class DeConvFCGR(tf.keras.layers.Conv2DTranspose):
    "Input  2^(k-l) x 2^(k-l) -> output 2^k x 2^k "
    def __init__(self, filters, levels: int = 1, **kwargs):
        super(DeConvFCGR, self).__init__(**kwargs)
        self.filters = filters
        self.levels = levels

    def build(self, input_shape):
        # Define the kernel size and stride based on the parameter levels
        kernel_size = (2*self.levels, 2**self.levels)
        stride = (2*self.levels, 2**self.levels)
        # Define the deconvolutional layer
        self.deconv_layer = tf.keras.layers.Conv2DTranspose(self.filters, kernel_size=kernel_size, strides=stride, padding='valid')
        super(DeConvFCGR, self).build(input_shape)

    def call(self, inputs):
        return self.deconv_layer(inputs)

    def compute_output_shape(self, input_shape):
        return self.deconv_layer.compute_output_shape(input_shape)
