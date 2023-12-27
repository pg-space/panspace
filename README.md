# Embedding bacteria
The goal is to build an embedding space for bacterial sequences and use them as an index of dense vector to perform fast queries using faiss

## 0. Download dataset
run the following script to download all compressed file from the [661-bacterial dataset](https://zenodo.org/records/4602622/).
```bash
./scripts/download.sh
```

## 1. generate FCGR

Create virtual environment for snakemake (each rule has its own environment, see `envs`)

```bash
mamba env create -n snakemake -f envs/smk.yaml
mamba activate snakemake
```

This pipeline count kmers using [`kmc`](https://github.com/refresh-bio/KMC) and then creates a `npy` file with the [FCGR](https://github.com/AlgoLab/complexCGR)
```bash
snakemake -s rules/create_fcgr.smk -c16 --use-conda
```

## 2. Train Autoencoder and create index

```bash
snakemake -s rules/create_index.smk -c16 --use-conda
```


___

## 2. train VAR
Once FCGR (npy file) has been generated, we can train an Autoencoder (see `params.yaml`)

```bash
mamba env create -n train -f envs/train.yaml
mamba activate train
```

```bash
python src/train.py
```

## 3. build and test the index
Build the index, query the most similar embeddings
```bash 
python src/index.py
```