import json
import streamlit as st
import numpy as np
import pandas as pd

from pathlib import Path

from collections import namedtuple

from rich.progress import track
from complexcgr import FCGR
from panspace import version
from panspace.streamlit.utils import (
    count_kmers_from_fasta,
    compute_fcgr_matrix,
    clip_fcgr,
)
from panspace.streamlit.interactive_plot import show_fcgr

import tensorflow as tf
import faiss

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
    
    print(neighbors_labels)
    print(neighbors_sample_ids)
    print(D)

    df = pd.DataFrame({"sampleid": neighbors_sample_ids[0], "label": neighbors_labels[0], "distance": D[0]})
    df["distance"] = df["distance"].astype("float32")

    return df

with st.sidebar:
    st.image("img/panspace-logo-v4.png", caption=f"panspace v{version}")
    
    st.header("FCGR")
    kmer_size = st.slider("k-mer size", min_value=2, max_value=11, value=8, step=1, key="kmer_size")
    percentile_clip = st.slider("percentile clip", min_value=0.0, max_value=100.0, value=80.0, step=0.1, key="percentile_clip")

    col1, col2 = st.columns(2)
    with col1: width = st.number_input("width", value=800)
    with col2: height = st.number_input("height", value=800)

    button_query = st.toggle("Query")

    if button_query:
        dir_index = st.text_input("Directory Index", value="indexes/8mer-mask11111111/triplet_semihard_loss-ranger-0.5-hq-128-CNNFCGR_Levels-level1-clip100/index")
        path_model = st.text_input("Encoder", value="indexes/8mer-mask11111111/triplet_semihard_loss-ranger-0.5-hq-128-CNNFCGR_Levels-level1-clip100/checkpoints/weights-CNNFCGR_Levels.keras")
        neighbors = st.number_input("Neighbors", value=11, min_value=1, max_value=100,)

st.set_page_config(layout="wide")

with st.expander("About panspace :dna:"):
    st.markdown(
        """
        `panspace` is a Python library for querying bacterial assemblies in an embedding space.
        
        **Key Features:**
        - Based on Frequency Chaos Representation of DNA (FCGR).
        - Index is embedding based.
        - Fast and accurate identification of species against AllTheBacteria data base.
        
        **Documentation:**
        For detailed documentation and usage examples, visit the [panspace documentation](https://github.com/pg-space/panspace).
        """
    )
    st.image("img/panspace-pipeline.png", width="stretch", caption=f"Querying assemblies in panspace")


path = st.text_input("Path to FASTA file or directory", 
                          value="/home/koke/Servers/watson/Github/panspace/sequences/SAMEA747610.fa", 
                          help="Enter the path to your FASTA file here. Accepted extension: .fasta, .fa, .fna .fa.gz")
path = Path(path)
if path.is_dir():
    paths = list(path.rglob("*.fa")) + \
            list(path.rglob("*.fa.gz")) + \
            list(path.rglob("*.fna")) + \
            list(path.rglob("*.fasta"))
    path_file = st.selectbox("Select file", [str(x) for x in paths])

elif path.is_file():
    assert any([str(path).endswith(x) for x in [".fa",".fasta",".fna",".fa.gz"]]), "incorrect extension file"
    path_file = path
                
button = st.button("Submit", type="primary")

if path_file is not None and button:
    
    if Path(path_file).exists():
        st.success(f"Working on {Path(path_file)}.")
    else:
        st.error("File does not exists")
        
    with st.status("Query", expanded=True) as status:

        st.write("Counting k-mers...")
        kmers = count_kmers_from_fasta(path_file, k = kmer_size)

        if len(kmers) > 0:
            st.write("k-mers done!")
        else:
            st.write("No k-mers found")

        st.write("Computing FCGR matrix...")
        fcgr_matrix = compute_fcgr_matrix(kmers, k = kmer_size)

        if percentile_clip < 100:
            st.write("Applying clipping to FCGR") 
            fcgr_matrix_plot = clip_fcgr(fcgr_matrix, percentile_clip=percentile_clip)
        else:
            fcgr_matrix_plot = fcgr_matrix
        fcgr = FCGR(k=kmer_size)
        st.write("Showing FCGR...")        
        status.update(label="FCGR Done!", state="complete", expanded=False)

    # Display the interactive plot
    show_fcgr(fcgr_matrix_plot, kmers, width=width, height=height)

if button_query and button:
    with st.status("Query", expanded=True) as status:

        dir_index = Path(dir_index)
        path_index = dir_index.joinpath("panspace.index")
        
        st.write("Loading Encoder...")
        model = load_model(path_model)
        
        st.write("Loading FAISS index...")
        index = load_index(path_index)

        st.write("Loading Index metadata...") 
        labels_by_sampleid, index2metadata_keys, index2metadata_values = load_labels(dir_index)

        # get labels from idx
        index2metadata = {k: v for k,v in zip(index2metadata_keys, index2metadata_values)}
        get_label_ = lambda idx: index2metadata.get(idx).label if idx>=0 else "unanswer"
        get_sampleid_ = lambda idx: index2metadata.get(idx).sample_id if idx>=0 else "unanswer"
        
        get_label = np.vectorize(get_label_)
        get_sampleid = np.vectorize(get_sampleid_)
        
        print(fcgr_matrix.shape)
        st.write("Creating embedding...")       
        embedding = create_embedding(np.expand_dims(fcgr_matrix,axis=0), model, preprocessing="scale_zero_one", percentile_clip=percentile_clip)

        st.write("Querying...")
        query_result = query_embedding(embedding, index, neighbors, get_label, get_sampleid)

        status.update(label="Query Done!", state="complete", expanded=False)

    st.dataframe(query_result)   