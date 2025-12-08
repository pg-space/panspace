import json
import orjson
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
                    kmer = ''.join([base if base in "ACGT" else "N" for base in kmer])
                    if "N" not in kmer:  # skip ambiguous kmers
                        kmer_counts[kmer] += 1
    # plain fasta
    else:
        with open(fasta_path, "r") as fasta_path:
            for record in SeqIO.parse(fasta_path, "fasta"):
                seq = str(record.seq).upper()
                for i in range(len(seq) - k + 1):
                    kmer = seq[i:i + k]
                    kmer = ''.join([base if base in "ACGT" else "N" for base in kmer])
                    if "N" not in kmer:  # skip ambiguous kmers
                        kmer_counts[kmer] += 1

    return dict(kmer_counts)

@st.cache_data()
def count_kmers_from_contig(fasta_path, contig_id=0, k=5):
    """
    Count k-mer frequencies in a contig sequence.

    Args:
        fasta_path (str): Path to the FASTA file.
        contig (str): Contig sequence.
        k (int): K-mer size.

    Returns:
        dict: {kmer: frequency}
    """
    kmer_counts = Counter()

    num_contig = 0
    # gzip files
    if str(fasta_path).endswith(".gz"):
        
        with gzip.open(fasta_path, "rt") as handle:
            for record in SeqIO.parse(handle, "fasta"):
                if num_contig == contig_id:

                    seq = str(record.seq).upper()
                    for i in range(len(seq) - k + 1):
                        kmer = seq[i:i + k]
                        kmer = ''.join([base if base in "ACGT" else "N" for base in kmer])
                        if "N" not in kmer:  # skip ambiguous kmers
                            kmer_counts[kmer] += 1
                    return dict(kmer_counts) 
                num_contig += 1

    # plain fasta
    else:
        with open(fasta_path, "r") as fasta_path:
            for record in SeqIO.parse(fasta_path, "fasta"):
                
                if num_contig == contig_id:
                    
                    seq = str(record.seq).upper()
                    for i in range(len(seq) - k + 1):
                        kmer = seq[i:i + k]
                        kmer = ''.join([base if base in "ACGT" else "N" for base in kmer])
                        if "N" not in kmer:  # skip ambiguous kmers
                            kmer_counts[kmer] += 1

                    return dict(kmer_counts)
                num_contig += 1

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

@st.cache_data()
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

# Function to generate a download link for each sample
def make_download_link(sample_id):
    import requests

    url=f"https://allthebacteria-assemblies.s3.eu-west-2.amazonaws.com/{sample_id}.fa.gz"
    # response = requests.get(url)
    # button = st.download_button(
    #     label=f"Click to save {sample_id}",
    #     data=response.content,
    #     file_name=f"{sample_id}.tar.gz",
    #     mime="gz"
    # )
    return url #f'<a href="{url}" download>Download</a>'


def query_embedding(embedding, index, neighbors, get_label, get_sampleid):

    D,I = index.search(embedding, neighbors)
     
    neighbors_labels= get_label(I)
    neighbors_sample_ids = get_sampleid(I)
    
    df = pd.DataFrame({"sampleid": neighbors_sample_ids[0], "label": neighbors_labels[0], "distance": D[0]})
    df["distance"] = df["distance"].astype("float32")
    df["ENA Browser"] = df["sampleid"].apply(lambda sid: f"https://www.ebi.ac.uk/ena/browser/view/{sid}")  # link to ENA browser

    # Option 1 — Simple clickable links inside dataframe
    df["Download Assembly"] = df["sampleid"].apply(lambda x: make_download_link(x))
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

    # Load JSON files once
    with open(dir_index / "id_embeddings.json", "rb") as fp:
        pos_to_path = orjson.loads(fp.read())
    with open(dir_index / "labels.json", "rb") as fp:
        pos_to_label = orjson.loads(fp.read())

    # Prepare reusable references
    Metadata = namedtuple("Metadata", ["sample_id", "label"])
    labels_by_sampleid = {}
    index2metadata = {}

    # Build both dicts in a single loop
    for idx_str, path in pos_to_path.items():
        idx = int(idx_str)
        label = pos_to_label.get(idx_str) or pos_to_label.get(idx)
        stem = path.rsplit("/", 1)[-1].rsplit(".", 1)[0]  # faster than Path(path).stem
        labels_by_sampleid[stem] = label
        index2metadata[idx] = Metadata(stem, label)

    return labels_by_sampleid, list(index2metadata.keys()), list(index2metadata.values())