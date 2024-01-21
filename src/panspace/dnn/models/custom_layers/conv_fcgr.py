# from tensorflow.keras.layers import Layer, Conv2D
import tensorflow as tf

class ConvFCGR(tf.keras.layers.Conv2D):
    "Input 2^k x 2^k -> output 2^(k-l) x 2^(k-l)"
    def __init__(self, filters, levels: int = 1, **kwargs):
        super(ConvFCGR, self).__init__(**kwargs)
        self.filters = filters
        self.levels = levels

    def build(self, input_shape):
        # Define the kernel size based on the parameter
        kernel_size = (2**self.levels, 2**self.levels)
        stride = (2**self.levels, 2**self.levels)
        # Define the convolutional layer
        self.conv_layer = tf.keras.layers.Conv2D(self.filters, kernel_size=kernel_size, strides=stride, padding='valid')
        super(ConvFCGR, self).build(input_shape)

    def call(self, inputs):
        return self.conv_layer(inputs)

    def compute_output_shape(self, input_shape):
        return self.conv_layer.compute_output_shape(input_shape)
