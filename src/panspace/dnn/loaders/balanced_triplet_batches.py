import tensorflow as tf
import numpy as np
import random
from collections import defaultdict

# Assume data_dict is your class-to-samples mapping
# data_dict = {
#     'class_1': [sample1, sample2, ...],
#     'class_2': [sample1, sample2, ...],
#     ...
# }

def generator_balanced_triplet_batches(data_dict, batch_size, num_classes_per_batch,):
    """
    Creates batches with a fixed number of classes and samples per class.
    
    Args:
        data_dict (dict): Mapping from class labels to lists of paths.
        batch_size (int): Total number of samples per batch.
        num_classes_per_batch (int): Number of classes per batch.
    
    Returns:
        tf.data.Dataset: A dataset yielding balanced batches.
    """
    samples_per_class = batch_size // num_classes_per_batch
    class_labels = list(data_dict.keys())
    encoder_output = {label: num for num, label in enumerate(data_dict.keys())}

    def generator():
        
        # for batch in range(batches_per_epoch):
        while True:
            selected_classes = random.sample(class_labels, num_classes_per_batch)
            paths = []
            labels = []
            for cls in selected_classes:
                paths_class = data_dict[cls]
                selected_samples = random.choices(paths_class, k=samples_per_class)
                
                # load paths and labels in the batch
                paths.extend(selected_samples)        
                labels.extend(encoder_output[cls] for _ in selected_samples)

            # shuffle both paths and labels
            zipped = list(zip(paths, labels))
            random.shuffle(zipped)
            paths, labels = zip(*zipped)

            # load numpy arrays with batch and channel axes
            batch_X = [np.expand_dims(np.expand_dims(np.load(p),axis=0),axis=-1) for p in paths]
            X = np.concatenate(batch_X, axis=0)
            y = np.array(labels)
            
            yield X, y
    
    return generator