"""
This script train a model with the available data
then creates a faiss index with the embeddings of the train and validation sets
"""

configfile: "params.yaml"

from pathlib import Path

KMER = config["kmer_size"]
PATH_FCGR = Path(config["outdir"]).joinpath(f"{KMER}mer/fcgr")
PATH_TRAIN = config["train"]["outdir"]
ARCHITECTURE = config["train"]["architecture"]
LATENT_DIM = config["train"]["latent_dim"]
rule: 
    input: 
        Path(PATH_TRAIN).joinpath("test/test_index.tsv"),
        # Path(PATH_TRAIN).joinpath("faiss-embeddings/bacterial.index")

rule train:
    output:
        Path(PATH_TRAIN).joinpath(f"checkpoints/weights-{ARCHITECTURE}.keras")
    input:
        list(Path(PATH_FCGR).joinpath(f"{KMER}mer/fcgr").rglob("*/*.npy"))
    conda:
        "../envs/train.yaml"
    resources:
        nvidia_gpu=1
    shell:
        "python3 src/train.py"

rule encoder_decoder:
    output:
        Path(PATH_TRAIN).joinpath(f"models/encoder.keras"),
        Path(PATH_TRAIN).joinpath(f"models/decoder.keras")
    input:
        Path(PATH_TRAIN).joinpath(f"checkpoints/weights-{ARCHITECTURE}.keras")
    params:
        dir_save=Path(PATH_TRAIN).joinpath("models")
    conda: 
        "../envs/train.yaml"
    shell:
        "python3 src/get_encoder_decoder.py --path-chkpt {input} --dir-save {params.dir_save}"

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
    conda: 
        "../envs/train.yaml"
    shell:
        "python3 src/create_index.py --path-exp {params.path_exp} --latent-dim {params.latent_dim}"

rule test_index:
    output:
        Path(PATH_TRAIN).joinpath("faiss-embeddings/query_embeddings.npy"),
        Path(PATH_TRAIN).joinpath("faiss-embeddings/id_query_embeddings.json"),
        Path(PATH_TRAIN).joinpath("test/test_index.tsv"),
    input:
        Path(PATH_TRAIN).joinpath("faiss-embeddings/bacterial.index")
    params:
        path_exp=PATH_TRAIN,
        latent_dim=LATENT_DIM
    resources:
        nvidia_gpu=1
    conda: 
        "../envs/train.yaml"
    shell:
        "python3 src/test_index.py --path-exp {params.path_exp} --latent-dim {params.latent_dim}"