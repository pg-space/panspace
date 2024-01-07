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
        PATH_TRAIN.joinpath(f"checkpoints/weights-{ARCHITECTURE}.keras")
    input:
        list(PATH_FCGR.rglob("*/*.npy"))
    log:
        Path(PATH_TRAIN).joinpath("logs/train.log")
    conda:
        "../envs/bacterspace.yaml"
    resources:
        nvidia_gpu=1
    params:
        datadir=PATH_FCGR,
        outdir=PATH_TRAIN,
        autoencoder=config["train"]["architecture"],
        latent_dim=config["train"]["latent_dim"],
        kmer=config["kmer_size"],
        batch_size=config["train"]["batch_size"],
        optimizer=config["train"]["optimizer"],
        patiente_early_stopping=config["train"]["patiente_early_stopping"],
        patiente_learning_rate=config["train"]["patiente_learning_rate"],
        train_size=config["train"]["train_size"],
        seed=config["train"]["seed"],
    shell:
        """/usr/bin/time -v bacterspace trainer train-autoencoder \
        --datadir {params.datadir} \
        --outdir {params.outdir} \
        --autoencoder {params.autoencoder} \
        --latent-dim {params.latent_dim} \
        --kmer {params.kmer} \
        --batch-size {params.batch_size} \
        --optimizer {params.optimizer} \
        --patiente-early-stopping {params.patiente_early_stopping} \
        --patiente-learning-rate {params.patiente_learning_rate} \
        --train-size {params.train_size} \
        --seed {params.seed} 2> {log}
        """

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
        "../envs/bacterspace.yaml"
    shell:
        "/usr/bin/time -v bacterspace trainer split-autoencoder --path-checkpoint {input} --dirsave {params.dir_save} 2> {log}"

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
        "../envs/bacterspace.yaml"
    shell:
        "/usr/bin/time -v bacterspace index create --path-experiment {params.path_exp} --latent-dim {params.latent_dim} 2> {log}"

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
        "../envs/bacterspace.yaml"
    shell:
        "/usr/bin/time -v bacterspace index test --path-experiment {params.path_exp} 2> {log}"

# TODO: join with test_index rule 
rule metrics_test_index:
    output:
        Path(PATH_TRAIN).joinpath("test/precision_recall_consensus_{n_neighbors}.csv")
    input:
        Path(PATH_TRAIN).joinpath("test/test_index.tsv"),
    conda: 
        "../envs/bacterspace.yaml"
    params:
        path_exp=PATH_TRAIN
    shell:
        "bacterspace index metrics-test --n-neighbors {wildcards.n_neighbors} --path-experiment {params.path_exp} 2> log.err" 