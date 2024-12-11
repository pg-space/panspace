import tensorflow as tf
import numpy as np
import random
from collections import defaultdict

random.seed(42)

# Assume data_dict is your class-to-samples mapping
# data_dict = {
#     'class_1': [sample1, sample2, ...],
#     'class_2': [sample1, sample2, ...],
#     ...
# }

def generator_balanced_triplet_batches(data_dict, batch_size, num_classes_per_batch, ):
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
            selected_classes = random.sample(class_labels, num_classes_per_batch) # TODO: weight such that all classes has the same prob of being chosen (already works like that)
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


def generator_balanced_batches(data_dict, batch_size, num_classes_per_batch, weights=False ):
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
    n_classes = len(class_labels)

    if weights is True:
        class_labels_freq = np.array([len(x) for x in data_dict.values()])
        class_probs = (class_labels_freq.sum() - class_labels_freq) / ((n_classes-1)*class_labels_freq.sum()) # probabilities to sample each class. Underrepresented ones have higher probability
    else:
        class_probs = None
    encoder_output = {label: num for num, label in enumerate(data_dict.keys())}

    def generator():
        
        # for batch in range(batches_per_epoch):
        while True:
            
            # select classes
            selected_classes = np.random.choice(class_labels, size=num_classes_per_batch, replace=False, p=class_probs)

            paths = []
            labels = []
            for cls in selected_classes:
                paths_class = data_dict[cls]
                selected_samples = random.choices(paths_class, k=samples_per_class) # sampling with replacement
                
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


def generator_one_shot(data_dict, batch_size, weights=False):
    """Create pairs to train contrastive loss
    output label=1 for similar classes, and label=0 for disimilar ones

    Args:
        data_dict (dict): dictionary where keys are species labels, and values are list of paths to FCGR
        batch_size (int): number of FCGR in each batch
        weights (bool, optional): if True, species labels are sampled based on their number of paths, underrepresented ones have higher probability. Defaults to False, means species are sampled randomly.

    Returns:
        generator: to be used with tf.data.Dataset.from_generato()

    Yields:
        tuple: (batch1, batch2), labels to train siamese network
    """    
    from collections import defaultdict

    # samples_per_class = batch_size // num_classes_per_batch
    class_labels = list(data_dict.keys())
    n_classes = len(class_labels)

    class_labels_by_genus = defaultdict(list)
    for label in class_labels:
        genus, _ =  label.split("_")[0]
        class_labels_by_genus[genus].append(label)

    if weights is True:
        class_labels_freq = np.array([len(x) for x in data_dict.values()])
        class_probs = (class_labels_freq.sum() - class_labels_freq) / ((n_classes-1)*class_labels_freq.sum()) # probabilities to sample each class. Underrepresented ones have higher probability
    else:
        class_probs = None
    
    def generator():
        while True:

            # get (batch_size/2) classes to create the batch
            size = int(batch_size/2)
            selected_classes = np.random.choice(class_labels, size=size, replace=False, p=class_probs)    

            paths1, paths2  = [], []
            labels = []

            for cls in selected_classes:
                
                # get two paths of the same class
                paths_positive = np.random.choice(data_dict[cls], size=2)

                paths1.append(paths_positive[0])
                paths2.append(paths_positive[1])
                labels.append(1)

                # get one example of a different class
                cls_negative = np.random.choice(selected_classes)
                while cls == cls_negative:
                    cls_negative = np.random.choice(selected_classes)

                path_negative = np.random.choice(data_dict[cls_negative])
                
                paths1.append(paths_positive[0])
                paths2.append(path_negative)
                labels.append(0)


            batch_X1 = [np.expand_dims(np.expand_dims(np.load(p),axis=0),axis=-1) for p in paths1]
            batch_X2 = [np.expand_dims(np.expand_dims(np.load(p),axis=0),axis=-1) for p in paths2]
            X1 = np.concatenate(batch_X1, axis=0)
            X2 = np.concatenate(batch_X2, axis=0)
            y = np.array(labels)

            yield (X1, X2), y.astype(np.float32)

    return generator



def generator_one_shot_genus(data_dict, batch_size, weights=False):
    """Create pairs to train contrastive loss
    output label=1 for similar genus, and label=0 for same genus (if possible) but different species

    Args:
        data_dict (dict): dictionary where keys are species labels, and values are list of paths to FCGR
        batch_size (int): number of FCGR in each batch
        weights (bool, optional): if True, species labels are sampled based on their number of paths, underrepresented ones have higher probability. Defaults to False, means species are sampled randomly.

    Returns:
        generator: to be used with tf.data.Dataset.from_generato()

    Yields:
        tuple: (batch1, batch2), labels to train siamese network
    """    
    from collections import defaultdict

    # samples_per_class = batch_size // num_classes_per_batch
    class_labels = list(data_dict.keys())
    n_classes = len(class_labels)

    class_labels_by_genus = defaultdict(list)
    for label in class_labels:
        genus, *_ =  label.split("_")
        class_labels_by_genus[genus].append(label)

    if weights is True:
        class_labels_freq = np.array([len(x) for x in data_dict.values()])
        class_probs = (class_labels_freq.sum() - class_labels_freq) / ((n_classes-1)*class_labels_freq.sum()) # probabilities to sample each class. Underrepresented ones have higher probability
    else:
        class_probs = None
    
    def generator():
        while True:

            # select the positive classes (half of the batch size)
            size = int(batch_size/2)
            selected_classes = np.random.choice(class_labels, size=size, replace=False, p=class_probs)    # the positive classes

            paths1, paths2  = [], []
            labels = []

            for cls in selected_classes:
                
                # get two paths of the same class
                paths_positive = np.random.choice(data_dict[cls], size=2)

                paths1.append(paths_positive[0])
                paths2.append(paths_positive[1])
                labels.append(1)

                # get one example of a different species but from the same genus (if possible)
                genus = cls.split("_")[0] 
                labels_genus  = class_labels_by_genus[genus].copy()
                labels_genus.remove(cls)
                
                # if there are more species in the same genus, select one of them
                if labels_genus:
                    cls_negative = np.random.choice(labels_genus) 
                # otherwise pick another species
                else: 
                    cls_negative = np.random.choice(selected_classes)
                    while cls == cls_negative:
                        cls_negative = np.random.choice(selected_classes)

                path_negative = np.random.choice(data_dict[cls_negative])
                
                paths1.append(paths_positive[0])
                paths2.append(path_negative)
                labels.append(0)

            batch_X1 = [np.expand_dims(np.expand_dims(np.load(p),axis=0),axis=-1) for p in paths1]
            batch_X2 = [np.expand_dims(np.expand_dims(np.load(p),axis=0),axis=-1) for p in paths2]
            X1 = np.concatenate(batch_X1, axis=0)
            X2 = np.concatenate(batch_X2, axis=0)
            y = np.array(labels)

            yield (X1, X2), y.astype(np.float32)

    return generator




def generator_one_shot_genus_mix(data_dict, batch_size, weights=False):
    """Create pairs to train contrastive loss
    output label=1 for similar genus, and label=0 for same genus (if possible) but different species
    randomly select pairs from different genus

    Args:
        data_dict (dict): dictionary where keys are species labels, and values are list of paths to FCGR
        batch_size (int): number of FCGR in each batch
        weights (bool, optional): if True, species labels are sampled based on their number of paths, underrepresented ones have higher probability. Defaults to False, means species are sampled randomly.

    Returns:
        generator: to be used with tf.data.Dataset.from_generato()

    Yields:
        tuple: (batch1, batch2), labels to train siamese network
    """    
    from collections import defaultdict

    # samples_per_class = batch_size // num_classes_per_batch
    class_labels = list(data_dict.keys())
    n_classes = len(class_labels)

    class_labels_by_genus = defaultdict(list)
    for label in class_labels:
        genus, *_ =  label.split("_")
        class_labels_by_genus[genus].append(label)

    if weights is True:
        class_labels_freq = np.array([len(x) for x in data_dict.values()])
        class_probs = (class_labels_freq.sum() - class_labels_freq) / ((n_classes-1)*class_labels_freq.sum()) # probabilities to sample each class. Underrepresented ones have higher probability
    else:
        class_probs = None
    
    def generator():
        while True:

            # select the positive classes (half of the batch size)
            size = int(batch_size/2)
            selected_classes = np.random.choice(class_labels, size=size, replace=False, p=class_probs)    # the positive classes

            paths1, paths2  = [], []
            labels = []

            for cls in selected_classes:
                
                # get two paths of the same class
                paths_positive = np.random.choice(data_dict[cls], size=2)

                paths1.append(paths_positive[0])
                paths2.append(paths_positive[1])
                labels.append(1)

                if np.random.rand() > 0.5:
                    # get one example of a different species but from the same genus (if possible)
                    genus = cls.split("_")[0] 
                    labels_genus  = class_labels_by_genus[genus].copy()
                    labels_genus.remove(cls)
                    
                    # if there are more species in the same genus, select one of them
                    if labels_genus:
                        cls_negative = np.random.choice(labels_genus) 
                    # otherwise pick another species
                    else: 
                        cls_negative = np.random.choice(class_labels)
                        while cls == cls_negative:
                            cls_negative = np.random.choice(class_labels)
                else:
                    # get one example randomly
                    cls_negative = np.random.choice(class_labels)
                    while cls == cls_negative:
                        cls_negative = np.random.choice(class_labels)

                path_negative = np.random.choice(data_dict[cls_negative])
                
                paths1.append(paths_positive[0])
                paths2.append(path_negative)
                labels.append(0)

            batch_X1 = [np.expand_dims(np.expand_dims(np.load(p),axis=0),axis=-1) for p in paths1]
            batch_X2 = [np.expand_dims(np.expand_dims(np.load(p),axis=0),axis=-1) for p in paths2]
            X1 = np.concatenate(batch_X1, axis=0)
            X2 = np.concatenate(batch_X2, axis=0)
            y = np.array(labels)


            yield (X1, X2), y.astype(np.float32)

    return generator
