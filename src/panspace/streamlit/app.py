import json
import faiss
import numpy as np
import pandas as pd
import tensorflow as tf
import requests
import subprocess
import plotly.express as px

from collections import namedtuple
from pathlib import Path
from rich.progress import track
from complexcgr import FCGR
from matplotlib.colors import LinearSegmentedColormap

green_black = LinearSegmentedColormap.from_list("green_black", ["black", "#66FF00"])

from panspace import version
from panspace.streamlit.utils import (
    count_kmers_from_fasta,
    compute_fcgr_matrix,
    clip_fcgr,
    create_embedding,
    query_embedding,
)
from panspace.streamlit.interactive_plot import show_fcgr

from panspace.streamlit.utils import (
    load_model, 
    load_index,
    load_labels,
)
from panspace.streamlit.ena import fetch_ena_sample_metadata
from panspace.streamlit.html import html_swarm_sphere, html_3d_sphere_logo

import streamlit as st
import streamlit.components.v1 as components

color_scales = ["gray"] + px.colors.named_colorscales()

with st.sidebar:

    dir_img = Path(__file__).parent.parent.parent.parent
    # st.image(dir_img / "img" / "panspace-logo-v5.png", caption=f"panspace v{version}")
    components.html(html_3d_sphere_logo, height=300,)
    _, col, _ = st.columns([2,3,1])
    with col: st.caption(f"version {version}")

    st.header("FCGR")
    kmer_size = st.slider("k-mer size", min_value=2, max_value=11, value=8, step=1, key="kmer_size")
    percentile_clip = st.slider("percentile clip", min_value=0.0, max_value=100.0, value=80.0, step=0.1, key="percentile_clip")
    rotation = st.segmented_control("Rotation (counterclockwise)", options = [0, 90, 180, 270], default=0)

    col1, col2 = st.columns(2)
    with col1: color_continuous_scale = st.selectbox("Color Scale", options = color_scales, index = 0)
    with col2: reverse_color = st.toggle("reverse", value=True)

    
    col1, col2 = st.columns(2)
    with col1: width = st.number_input("width", value=800)
    with col2: height = st.number_input("height", value=800)

    button_query = st.toggle("Query")

    if button_query:
        dir_index = st.text_input("Directory Index", value="indexes/8mer-mask11111111/triplet_semihard_loss-ranger-0.5-hq-256-CNNFCGR_Levels-level1-clip80/index")
        path_model = st.text_input("Encoder", value="indexes/8mer-mask11111111/triplet_semihard_loss-ranger-0.5-hq-256-CNNFCGR_Levels-level1-clip80/checkpoints/weights-CNNFCGR_Levels.keras")
        neighbors = st.number_input("Neighbors", value=11, min_value=1, max_value=100,)
        preprocessing = st.selectbox("Preprocessing FCGR", options = ["distribution","scale_zero_one","clip_scale_zero_one","clip"] , index = 2)

        get_ena_metadata = st.toggle("Get ENA Metadata", value=False)


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
    # st.image(dir_img / "img" / "panspace-pipeline.png", width="stretch", caption=f"Querying assemblies in panspace")


path = st.text_input("Path to FASTA file or directory", 
                          value="sequences/SAMEA747610.fa", 
                          help="Enter the path to your FASTA file here. Accepted extension: .fasta, .fa, .fna .fa.gz")
path = Path(path)
if path.is_dir() and path.exists():
    paths = list(path.rglob("*.fa")) + \
            list(path.rglob("*.fa.gz")) + \
            list(path.rglob("*.fna")) + \
            list(path.rglob("*.fasta"))
    if len(paths) == 0: st.warning("No files detected")
    path_file = st.selectbox("Select file", [str(x) for x in paths])
elif path.is_file() and path.exists():
    assert any([str(path).endswith(x) for x in [".fa",".fasta",".fna",".fa.gz"]]), "incorrect extension file"
    path_file = path
else:
    st.warning(f"{path} does not exists")
    path_file = None
button = st.button("Submit", type="primary")


if path_file is not None and button:
    
    if Path(path_file).exists():
        st.success(f"Working on {Path(path_file)}.")
    else:
        st.error("File does not exists")
        
    with st.status("FCGR", expanded=True) as status:

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
        st.write(f"Showing FCGR...tot kmers {fcgr_matrix.sum().sum()}")        
        status.update(label="FCGR", state="complete", expanded=True)

        # --- Display the interactive plot
        color_scale = color_continuous_scale if not reverse_color else color_continuous_scale + "_r"
        show_fcgr(fcgr_matrix_plot, kmers, width=width, height=height, rotation=rotation, color_continuous_scale=color_scale)

# --- Query
if button_query and button and path_file is not None:
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
        embedding = create_embedding(np.expand_dims(fcgr_matrix,axis=0), model, preprocessing=preprocessing, percentile_clip=percentile_clip)

        st.write("Querying...")
        query_result = query_embedding(embedding, index, neighbors, get_label, get_sampleid)

        status.update(label="Query results", state="complete", expanded=True)

        st.dataframe(query_result, column_config={
            "ENA Browser": st.column_config.LinkColumn(),
            "Download Assembly": st.column_config.LinkColumn()
        })   

    if get_ena_metadata:

        with st.status("ENA metadata", expanded=True) as status:         
            data = []
            for sampleid_ena in query_result.sampleid:
                print(sampleid_ena)
                data.append(fetch_ena_sample_metadata(sample_id=sampleid_ena))
                
            st.dataframe(pd.DataFrame(data))
