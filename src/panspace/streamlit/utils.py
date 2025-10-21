import json
import gzip
import faiss
import numpy as np
import pandas as pd
import tensorflow as tf

from Bio import SeqIO
from collections import Counter, namedtuple
from complexcgr import FCGR
from pathlib import Path

import streamlit as st

@st.cache_data()
def count_kmers_from_fasta(fasta_path, k=5):
    """
    Count k-mer frequencies in a FASTA file.

    Args:
        fasta_path (str): Path to the FASTA file.
        k (int): K-mer size.

    Returns:
        dict: {kmer: frequency}
    """
    kmer_counts = Counter()

    # gzip files
    if str(fasta_path).endswith(".gz"):
        

        with gzip.open(fasta_path, "rt") as handle:
            for record in SeqIO.parse(handle, "fasta"):
                seq = str(record.seq).upper()
                for i in range(len(seq) - k + 1):
                    kmer = seq[i:i + k]
                    if "N" not in kmer:  # skip ambiguous kmers
                        kmer_counts[kmer] += 1
    # plain fasta
    else:
        with open(fasta_path, "r") as fasta_path:
            for record in SeqIO.parse(fasta_path, "fasta"):
                seq = str(record.seq).upper()
                for i in range(len(seq) - k + 1):
                    kmer = seq[i:i + k]
                    if "N" not in kmer:  # skip ambiguous kmers
                        kmer_counts[kmer] += 1

    return dict(kmer_counts)

@st.cache_data()
def compute_fcgr_matrix(kmer_counts, k=5):
    """
    Generate FCGR matrix from k-mer counts.

    Args:
        kmer_counts (dict): {kmer: frequency}
        k (int): K-mer size.

    Returns:
        np.ndarray: FCGR matrix.
    """
    fcgr = FCGR(k=k)
    size = 2 ** k
    fcgr_matrix = np.zeros((size, size))

    # Assign frequency to each box in the matrix
    for kmer, freq in kmer_counts.items():        
        pos_x, pos_y = fcgr.kmer2pixel[kmer]
        fcgr_matrix[int(pos_x)-1,int(pos_y)-1] = freq
    
    return fcgr_matrix

def clip_fcgr(fcgr_matrix, percentile_clip=80):
    # Compute the desired percentile
    percentile = np.percentile(fcgr_matrix, percentile_clip)
    # Clip values above the percentile
    x_clipped = np.minimum(fcgr_matrix, percentile)

    return x_clipped


def create_embedding(fcgr_matrix, model, preprocessing="clip", percentile_clip=80):
    
    import tensorflow_probability as tfp

    # preprocessing of each FCGR to feed the model 
    if preprocessing == "distribution":
        # sum = 1
        preprocessing = lambda x: x / tf.math.reduce_sum(x)   
    elif preprocessing == "scale_zero_one": 
        # scale [0,1]
        preprocessing = lambda x: x / tf.math.reduce_max(x)
    elif preprocessing == "clip_scale_zero_one":

        def preprocessing(x):
            "clip and rescale [0,1]"
            # Compute the 90th percentile
            percentile = tfp.stats.percentile(x, percentile_clip)
            # Clip values above the 95th percentile
            x_clipped = tf.minimum(x, percentile)
            x_clipped = tf.cast(x_clipped, tf.float32)

            # Rescale the x to [0, 1]
            max_val = tf.reduce_max(x_clipped)
            max_val = tf.cast(max_val, tf.float32)
            
            x_rescaled = x_clipped / (max_val + 1e-8)  # add epsilon to avoid division by zero
            return x_rescaled
        
    elif preprocessing == "clip":
        
        def preprocessing(x):
            "clip"
            # Compute the 90th percentile
            percentile = tfp.stats.percentile(x, percentile_clip)
            # Clip values above the 95th percentile
            x_clipped = tf.minimum(x, percentile)
            return x_clipped
    
    fcgr_matrix = preprocessing(fcgr_matrix)
    embedding = model.predict(fcgr_matrix)

    return embedding

def query_embedding(embedding, index, neighbors, get_label, get_sampleid):

    D,I = index.search(embedding, neighbors)
     
    neighbors_labels= get_label(I)
    neighbors_sample_ids = get_sampleid(I)
    
    df = pd.DataFrame({"sampleid": neighbors_sample_ids[0], "label": neighbors_labels[0], "distance": D[0]})
    df["distance"] = df["distance"].astype("float32")
    df["url"] = df["sampleid"].apply(lambda sid: f"https://www.ebi.ac.uk/ena/browser/view/{sid}")  # link to ENA browser

    return df


@st.cache_data()
def load_model(path_model):
    model = tf.keras.models.load_model(path_model)
    return model

@st.cache_data()
def load_index(path_index):
    index = faiss.read_index(str(path_index))
    return index

@st.cache_resource()
def load_labels(dir_index):
    dir_index = Path(dir_index)
    with open(dir_index.joinpath("id_embeddings.json"), "r") as fp:
        pos_to_path = {int(idx): path for idx,path in json.load(fp).items()}

    with open(dir_index.joinpath("labels.json"), "r") as fp:
        pos_to_label = {int(idx): label for idx,label in json.load(fp).items()}

    labels_by_sampleid = dict()
    for pos, path in pos_to_path.items():       
        sampleid=Path(path).stem
        label = pos_to_label[pos]
        labels_by_sampleid[sampleid] = label

    Metadata=namedtuple("Metadata",["sample_id","label"])
    
    with open(dir_index.joinpath("id_embeddings.json"),"r") as fp:
        index2metadata = {int(idx): 
                        Metadata(
                            Path(path).stem, 
                            labels_by_sampleid.get(Path(path).stem,"unknown")
                            )   
                            for idx, path in json.load(fp).items()}

    return labels_by_sampleid, list(index2metadata.keys()), list(index2metadata.values())
