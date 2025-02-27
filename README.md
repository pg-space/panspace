<div align="center">
    <img src="img/panspace-logo.png" width="450" height="300">
</div>

# Taxonomy-aware embeddings for rapid querying of prokaryotes pangenomes

`panspace` is a library for creating and querying vector based indexes for bacterial genome (draft) assemblies.

`panspace` pipeline for querying works as follows,
1. First, each genome is represented by its Frequency matrix of the Chaos Game Representation of DNA (FCGR)
2. Then, the FCGR is mapped to a n-dimensional vector, the _embedding_, using a Convolutional Neural Network called `CNNFCGR`, the _Encoder_,
3. Finally, the _embedding_ --the compressed representation of the input genome-- is used to query an index of these vectors representing a bacterial pangenome. 

<div align="center">
    <img src="img/panspace-query.png" width="1000" height="550">
</div>

The library is based on tensorflow and faiss index.


## Query `index`
___

### Available indexes
| Encoder | Kmer | Embedding Size | Download                                    |
|---------|------|----------------|---------------------------------------------|
| CNNFCGR | 7    | 256            | [Download Index](https://zenodo.org/records/14936601/files/index-CNNFCGR-256-7mer.zip?download=1) |


We provide a **snakemake** pipeline to query a collection of genomes (from a folder), 

0. Clone the repository
```bash
git clone https://github.com/pg-space/panspace.git
cd panspace
``` 

1. [install snakemake](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html),
```bash
conda create -c conda-forge -c bioconda -n snakemake snakemake
conda activate snakemake
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

**Optional: for faster queries**
recommended if you have hundreds or thousands of assemblies to query 

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

## Create your own `encoder` and `index`
___
 
### Install the package

`panspace` requires  python >= 3.9, < 3.11.

with **CPU** support

```bash
pip install "panspace[cpu] @ git+https://github.com/pg-space/panspace.git"
```

with **GPU** support

```bash
pip install "panspace[gpu] @ git+https://github.com/pg-space/panspace.git"
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
## step-by-step guide


### CLI

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



### 1. Create FCGR of assemblies


### 2. Train an encoder to create the vector representations

1. Split dataset into train, validation and test sets 
```bash
panspace trainer split-dataset --help
```

2. Train

**Options** 
- Do you have labels for each assembly? 
    - Use metric learning with the triplet loss
    - Or metric learning with the contrastive loss
    Using the `CNNFCGR` architecture.
- If you do not have labels, then use unsupervised learning with the `AutoencoderFCGR` architecture


```bash
panspace trainer metric-learning --help # triplet loss
panspace trainer one-shot --help        # contrastive loss
panspace trainer autoencoder --help     
```

**Get the Encoder**
- If using the triplet loss, the output model is the encoder.
- If using the contrastive loss, you can get the encoder with `panspace trainer extract-backbone-one-shot`
- If using the autoencoder, you can get the encoder with `panspace trainer split-autoencoder`

3. Create Index

```bash
panspace index create --help
```

4. Query Index

If querying is done from FCGR in numpy format, then use
```bash
panspace index query --help
```

but if you want to query the index directly from assemblies, we encourage you to use the snakemake pipelines provided above.



___

# Author
`panspace` is developed by [Jorge Avila Cartes](https://github.com/jorgeavilacartes/)