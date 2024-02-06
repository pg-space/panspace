# Embedding bacterial assemblies
The goal is to build an embedding space for bacterial sequences and use them as an index of dense vector to perform fast queries using faiss

## CLI `panspace`

`panspace` is a library based on tensorflow and faiss index.
It provides commands for creating FCGR from kmer counts, train an autoencoder,
extract Encoder and Decoder from a trained model, and create and query an Index
of embeddings.
 
```bash
git clone git@github.com:jorgeavilacartes/embedding-bacteria.git
cd embedding-bacteria

mamba env create -n panspace -f condaenv.yaml
mamba activate panspace

panspace --help 
```
___


## 0. Download dataset
run the following script to download all compressed file from the [661k-bacterial dataset](https://zenodo.org/records/4602622/).
```bash
./scripts/download.sh
```
___ 
Create virtual environment for snakemake (each rule has its own environment, see `envs`)

```bash
mamba env create -n snakemake -f envs/smk.yaml
mamba activate snakemake
```

## 1. Generate FCGR

This pipeline count kmers using [`kmc`](https://github.com/refresh-bio/KMC) and then creates a `npy` file with the [FCGR](https://github.com/AlgoLab/complexCGR)

To create FCGR from all 661k bacterial dataset, run
```bash
snakemake -s rules/create_fcgr_tarxz.smk -c16 --use-conda
```
In the bacterial dataset input files are like `<some-name>.tar.xz`, where each compressed file contains a foder named `<some-name>/<assembly-id>.fa`
this pipeline assumes that assemblies follow this.

If you have a set of fasta files, you can use

```bash
snakemake -s rules/create_fcgr_fasta.smk -c16 --use-conda
```

*EXTENSIONS ACCEPTED*: `.fa` , `.fna`, `.fasta`


## 2. Train Autoencoder and create index

```bash
snakemake -s rules/create_index.smk -c16 --use-conda --resources nvidia_gpu=1
```

## 3. Query index
In `params-query.yaml`, define the following parameters:

```yaml 
query:
  dir_fasta: "/data/bacteria/test-query" # all fasta files inside the folder will be used to query the index
  outdir: "output-query"
```

and then run

```bash
snakemake -s rules/query_index.smk -c16 --use-conda --resources nvidia_gpu=1
```


___
# Author
`panspace` is developed by [Jorge Avila](https://github.com/jorgeavilacartes/)