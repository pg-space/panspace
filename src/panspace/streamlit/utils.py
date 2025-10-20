import numpy as np

from Bio import SeqIO
from collections import Counter

from complexcgr import FCGR

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

    with open(fasta_path, "r") as fasta_path:
        for record in SeqIO.parse(fasta_path, "fasta"):
            seq = str(record.seq).upper()
            for i in range(len(seq) - k + 1):
                kmer = seq[i:i + k]
                if "N" not in kmer:  # skip ambiguous kmers
                    kmer_counts[kmer] += 1

    return dict(kmer_counts)

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