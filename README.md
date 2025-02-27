<div align="center">
    <img src="img/panspace-logo.png" width="450" height="300">
</div>

# Taxonomy-aware embeddings for rapid querying of prokaryotes pangenomes

`panspace` is a library for creating and querying vector based indexes for bacterial genome (draft) assemblies.

`panspace` pipeline for querying works as follows,
1. First, each genome is represented by its Frequency matrix of the Chaos Game Representation of DNA (FCGR)
2. Then, the FCGR is mapped to a n-dimensional vector, the _embedding_, using a Convolutional Neural Network called `CNNFCGR`,
3. Finally, the _embedding_ --the compressed representation of the input genome-- is used to query an index of these vectors representing a bacterial pangenome. 

<div align="center">
    <img src="img/panspace-query.png" width="1000" height="550">
</div>

The library is based on tensorflow and faiss index.

 
## Install the package
___
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
___

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
___
We provide a **snakemake** pipeline to query a collection of genomes (from a folder), 

1. [install snakemake](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html),
```bash
conda create -c conda-forge -c bioconda -n snakemake snakemake
```

2. set parameters in `scripts/config.yml`, 

    - **directory with sequences** (accepted extensions `.fa.gz`, `.fa`, `.fna`) 
    - define an **output directory** to save query results
    - **gpu** or **cpu** usage
    - path to the **encoder** (`<path/to/encoder>.keras`)
    - path to the **index**  (<path/to/panspace-index>.index)

finally run
```bash
snakemake -s scripts/query.smk --cores 8 --use-conda
```

**Optional** 

For faster queries, recommended if you have hundreds or thousands of assemblies to query 

First install the [FCGR extension to KMC3](https://github.com/pg-space/fcgr/)
and put the path to the installed tool in the `scripts/config.yml` file and run, 
 
```bash
snakemake -s scripts/query_fast.smk --cores 8 --use-conda
```
or put it directly on bash
```bash
snakemake -s scripts/query_fast.smk --cores 8 --use-conda --config fcgr_bin=<path/to/fcgr>
```

_NOTES_ 
- change the number of cores (`--cores <NUM_CORES>`) if you have more availables, this will allow the parallelization of k-mer counts from assemblies done by [KMC3](https://github.com/refresh-bio/KMC).
- This extension constructs FCGR representations with a C++ extending KMC3 output. The default version parses the output of KMC as a dictionary of k-mer counts and then uses the python library [ComplexCGR](https://github.com/AlgoLab/complexCGR) for the construction of the FCGR. 

## Available indexes
___
| Encoder | Kmer | Embedding Size | Download                                    |
|---------|------|----------------|---------------------------------------------|
| CNNFCGR | 7    | 256            | [Download Index](https://zenodo.org/records/14936601/files/index-CNNFCGR-256-7mer.zip?download=1) |


## Create your own `encoder` and `index`
___
TODO.

___
# Author
`panspace` is developed by [Jorge Avila Cartes](https://github.com/jorgeavilacartes/)