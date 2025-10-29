import streamlit as st
import numpy as np
import plotly.express as px
from complexcgr import FCGR

# --- Function to display the interactive FCGR ---
def show_fcgr(fcgr_matrix, kmers, width=800, height = 800, rotation: int = 90, color_continuous_scale="gray_r"): 
            #   transpose:bool=False):
    """
    Display an interactive FCGR heatmap in Streamlit.
    Clicking or hovering a cell shows the corresponding k-mer and value.
    """
    kmer_size = len(list(kmers.keys())[0])
    fcgr = FCGR(k=kmer_size)
    pixel2kmer = {(px-1,py-1): kmer for kmer, (px,py) in fcgr.kmer2pixel.items()}
    
    nrows, ncols = fcgr_matrix.shape

    hover_text = [
        [f"k-mer: {pixel2kmer[(i,j)]}<br>Value: {fcgr_matrix[i, j]:.4f}"
        for j in range(ncols)]
        for i in range(nrows)
    ]

    hover_text = np.array(hover_text)

    # --- Apply rotation (counterclockwise) ---
    rotation = rotation % 360
    if rotation == 90:
        fcgr_matrix = np.rot90(fcgr_matrix, k=-3)  # 90° clockwise
        hover_text = np.rot90(hover_text, k=-3)
    elif rotation == 180:
        fcgr_matrix = np.rot90(fcgr_matrix, k=-2)
        hover_text = np.rot90(hover_text, k=-2)
    elif rotation == 270:
        fcgr_matrix = np.rot90(fcgr_matrix, k=-1)  # 270° clockwise = 90° counterclockwise
        hover_text = np.rot90(hover_text, k=-1)


    fig = px.imshow(
        fcgr_matrix,
        color_continuous_scale=color_continuous_scale,
        labels=dict(color="Frequency"),
    )

    # Add hover text
    fig.update_traces(text=hover_text, hoverinfo="text", hovertemplate="%{text}<extra></extra>")

    fig.update_layout(
        width=width,   # adjust width as needed
        height=height   # adjust height as needed
    )
    st.plotly_chart(fig, use_container_width=True)