# Embedding bacteria
The goal is to build an embedding space for bacterial sequences and use them as an index of dense vector to perform fast queries using faiss

## 1. generate FCGR

Create virtual environment for snakemake (each rule has its own environment, see `envs`)
```bash
conda activate base
mamba create -c bioconda -c conda-forge -n snakemake snakemake-minimal
conda activate snakemake
```

This pipeline count kmers using [`kmc`](https://github.com/refresh-bio/KMC) and then creates a `npy` file with the [FCGR](https://github.com/AlgoLab/complexCGR)
```bash
snakemake -s count_kmers.smk -c16 --use-conda
```
___
For the next steps, create an environment with pip

```
python -m venv env 
source env/bin/activate
pip install -r requirements.txt
```

## 2. train VAR
Once FCGR (npy file) has been generated, we can train a VAR (see `params.yaml`)

```bash
python src/train.py
```

## 3. build and test the index
Build the index, query the most similar embeddings
```bash 
python src/index.py
```