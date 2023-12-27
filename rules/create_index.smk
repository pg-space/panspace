"""
This script train a model with the available data
then creates a faiss index with the embeddings of the train and validation sets
"""

configfile: "params.yaml"

from pathlib import Path

KMER = config["kmer_size"]
OUTDIR=config["outdir"]
PATH_FCGR = Path(OUTDIR).joinpath(f"{KMER}mer/fcgr")
NAME_EXPERIMENT=config["train"]["name_experiment"]
PATH_TRAIN=Path(OUTDIR).joinpath(f"{KMER}mer/{NAME_EXPERIMENT}")
ARCHITECTURE = config["train"]["architecture"]
LATENT_DIM = config["train"]["latent_dim"]

rule: 
    input: 
        Path(PATH_TRAIN).joinpath("test/test_index.tsv"),
        expand( Path(PATH_TRAIN).joinpath("test/precision_recall_consensus_{n_neighbors}.csv"), n_neighbors=[1,3,5,10])

rule train:
    output:
        Path(PATH_TRAIN).joinpath(f"checkpoints/weights-{ARCHITECTURE}.keras")
    input:
        list(Path(PATH_FCGR).joinpath(f"{KMER}mer/fcgr").rglob("*/*.npy"))
    log:
        Path(PATH_TRAIN).joinpath("logs/train.log")
    conda:
        "../envs/train.yaml"
    resources:
        nvidia_gpu=1
    shell:
        "/usr/bin/time -v python3 src/train.py 2> {log}"

rule encoder_decoder:
    output:
        Path(PATH_TRAIN).joinpath(f"models/encoder.keras"),
        Path(PATH_TRAIN).joinpath(f"models/decoder.keras")
    input:
        Path(PATH_TRAIN).joinpath(f"checkpoints/weights-{ARCHITECTURE}.keras")
    params:
        dir_save=Path(PATH_TRAIN).joinpath("models")
    log:
        Path(PATH_TRAIN).joinpath("logs/encoder_decoder.log")
    conda: 
        "../envs/train.yaml"
    shell:
        "/usr/bin/time -v python3 src/get_encoder_decoder.py --path-chkpt {input} --dir-save {params.dir_save} 2> {log}"

rule create_index:
    output:
        Path(PATH_TRAIN).joinpath("faiss-embeddings/bacterial.index"),
        Path(PATH_TRAIN).joinpath("faiss-embeddings/embeddings.npy"),
        Path(PATH_TRAIN).joinpath("faiss-embeddings/id_embeddings.json"),
    input:
        Path(PATH_TRAIN).joinpath(f"models/encoder.keras"),
    params:
        path_exp=PATH_TRAIN,
        latent_dim=LATENT_DIM
    resources:
        nvidia_gpu=1
    log:
        Path(PATH_TRAIN).joinpath("logs/create_index.log")
    conda: 
        "../envs/train.yaml"
    shell:
        "/usr/bin/time -v python3 src/create_index.py --path-exp {params.path_exp} --latent-dim {params.latent_dim} 2> {log}"

rule test_index:
    output:
        Path(PATH_TRAIN).joinpath("faiss-embeddings/query_embeddings.npy"),
        Path(PATH_TRAIN).joinpath("faiss-embeddings/id_query_embeddings.json"),
        Path(PATH_TRAIN).joinpath("test/test_index.tsv"),
    input:
        Path(PATH_TRAIN).joinpath("faiss-embeddings/bacterial.index")
    params:
        path_exp=PATH_TRAIN,
    resources:
        nvidia_gpu=1
    log:
        Path(PATH_TRAIN).joinpath("logs/test_index.log")
    conda: 
        "../envs/train.yaml"
    shell:
        "/usr/bin/time -v python3 src/test_index.py --path-exp {params.path_exp} 2> {log}"

rule metrics_test_index:
    output:
        Path(PATH_TRAIN).joinpath("test/precision_recall_consensus_{n_neighbors}.csv")
    input:
        Path(PATH_TRAIN).joinpath("test/test_index.tsv"),
    conda: 
        "../envs/train.yaml"
    params:
        path_exp=PATH_TRAIN
    shell:
        "python3 src/metrics_test_index.py --n-neighbors {wildcards.n_neighbors} --path-exp {params.path_exp}"