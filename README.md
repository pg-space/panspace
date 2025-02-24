# Embedding bacterial assemblies
The goal is to build an embedding space for bacterial sequences and use them as an index of dense vector to perform fast queries using faiss

## CLI `panspace`

`panspace` is a library based on tensorflow and faiss index.
It provides commands for creating FCGR from kmer counts, train an autoencoder,
extract Encoder and Decoder from a trained model, and create and query an Index
of embeddings.
 
```bash
git clone git@github.com:pg-space/panspace.git
cd panspace
``` 

### Install the package

To install the package from the `pyproject.toml` file:

#### Install with CPU support

To install the package with CPU support from the `pyproject.toml` file:

```bash
pip install .[cpu]
```

To install the package with CPU support directly from the GitHub repository:

```bash
pip install "panspace[cpu] @ git+https://github.com/pg-space/panspace.git"
```

#### Install with GPU support

To install the package with GPU support from the `pyproject.toml` file:

```bash
pip install .[gpu]
```

To install the package with GPU support directly from the GitHub repository:

```bash
pip install "panspace[gpu] @ git+https://github.com/pg-space/panspace.git"
```

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

___
# Author
`panspace` is developed by [Jorge Avila Cartes](https://github.com/jorgeavilacartes/)