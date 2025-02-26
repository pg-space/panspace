<div align="center">
    <img src="img/panspace-logo.png" width="350" height="200">
</div>

# Taxonomy-aware embeddings for rapid querying of prokaryotes pangenomes

`panspace` is a library for creating and querying vector based indexes for bacterial genome (draft) assemblies.

1. Each genome represented by its Frequency matrix of the Chaos Game Representation of DNA (FCGR)
2. The FCGR is mapped to a n-dimensional vector (_embedding_) using a Convolutional Neural Network called `CNNFCGR`
3. The _embedding_ works as a compressed representation of the input genome, and is used to query an index of these vectors representing a bacterial pangenome. 

<div align="center">
    <img src="img/panspace-query.png" width="800" height="450">
</div>

The library is based on tensorflow and faiss index.

 
## Install the package
`panspace` requires  python >= 3.9, < 3.11.

with **CPU** support

```bash
pip install "panspace[cpu] @ git+https://github.com/pg-space/panspace.git"
```

with **GPU** support

```bash
pip install "panspace[gpu] @ git+https://github.com/pg-space/panspace.git"
```

Alternatively, first clone the repository

```bash
git clone git@github.com:pg-space/panspace.git
cd panspace
``` 

with **CPU** support
```bash
pip install .[cpu]
```

or with **GPU** support 
```bash
pip install .[gpu]
```

### Install from conda environment
with **CPU** support
```bash
conda env create -f envs/cpu.yml
conda activate panspace-cpu
```

with **GPU** support
```bash
conda env create -f envs/gpu.yml
conda activate panspace-gpu
```

## CLI

It provides commands for
- creating FCGR from kmer counts,
- train an encoder using metric learning (if labels are available) or an autoencoder,
- create and query an Index of _embeddings_.


```bash
panspace --help 

Usage: panspace [OPTIONS] COMMAND [ARGS]...                                                                               
                                                                                                                           
 🐱 Welcome to panspace, a tool for Indexing and Querying a pan-genome in an embedding space                               
                                                                                                                           
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                                 │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.          │
│ --help                        Show this message and exit.                                                               │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ data-curation    Find outliers and mislabaled samples.                                                                  │
│ docs             Open documentation webpage.                                                                            │
│ fcgr             Create FCGRs from fasta file or from txt file with kmers and counts.                                   │
│ index            Create and query index. Utilities to test index.                                                       │
│ stats-assembly   N50, number of contigs, avg length, total length.                                                      │
│ trainer          Train Autoencoder/Metric Learning. Utilities.                                                          │
│ utils            Extract info from text or log files                                                                    │
│ what-to-do       🐱 If you are new here, check this step-by-step guide                                                  │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Query `index`

We provide a snakemake pipeline to query an index, 

1. [install snakemake](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html),
```bash
conda create -c conda-forge -c bioconda -n snakemake snakemake
```

2. set parameters in `scripts/config.yml`, 
here you need to provide:
    - path to a directory with sequences (accepted extensions `.fa.gz`, `.fa`, `.fna`) 
    - the extension of the sequences (one of the accepted extensions)
    - define an output directory to save query results
    - use gpu or cpu
    - path to the encoder (`<path/to/encoder>.keras`)
    - path to the index  (<path/to/panspace-index>.index)

finally run
```bash
snakemake -s scripts/query_panspace.smk --cores 8 --use-conda
```

## Available indexes

| Encoder | Kmer | Embedding Size | Download Link |
|---------|------|----------------|---------------|
| CNNFCGR | 6    | 128            | [Download](https://example.com/index_6_128) |
| CNNFCGR | 7    | 256            | [Download](https://example.com/index_7_256) |


## Create your own `encoder` and `index`

___
# Author
`panspace` is developed by [Jorge Avila Cartes](https://github.com/jorgeavilacartes/)