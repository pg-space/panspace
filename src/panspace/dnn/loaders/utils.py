from typing import Dict, Optional

class EncoderOutput:
    """
    From list of labels to hot-encoding
    >> encoder_output = EncoderOutput(order_output_model=["lab1","lab2","lab3"])
    >> encoder_output(list_labels=["lab1"])
    >> # output: [1,0,0]
    """
    def __init__(self, order_output_model, encode_labels: Optional[Dict] = None):
        self.order_output_model=order_output_model
        self.encode_labels = encode_labels

    def label2num(self, label, list_labels):
        """Returns 1 if label in list_labels, otherwise, return 0"""
        return 1. if label in list_labels else 0.

    def __call__(self, list_labels):
        """From list of labels to hot-encoding"""
        # If encode_labels if provided, map the current labels to the new ones
        if self.encode_labels:
            list_labels = list(set([self.encode_labels[label] for label in list_labels]))
        
        # Return hot-encode vectors as list -> [0,1,0,1,...]
        return [self.label2num(label, list_labels) for label in self.order_output_model]