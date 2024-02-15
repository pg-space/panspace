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
        Path(PATH_TRAIN).joinpath("test/query_results.csv"),
        Path(PATH_TRAIN).joinpath("test/embeddings.npy"),

rule train:
    output:
        PATH_TRAIN.joinpath(f"checkpoints/weights-{ARCHITECTURE}.keras"),
        PATH_TRAIN.joinpath("split-train-val-test.json")
    input:
        list(PATH_FCGR.rglob("*/*.npy"))
    log:
        Path(PATH_TRAIN).joinpath("logs/train.log")
    conda:
        "../envs/panspace.yaml"
    resources:
        nvidia_gpu=1
    params:
        datadir=PATH_FCGR,
        outdir=PATH_TRAIN,
        autoencoder=config["train"]["architecture"],
        latent_dim=config["train"]["latent_dim"],
        kmer=config["kmer_size"],
        epochs=config["train"]["epochs"],
        batch_size=config["train"]["batch_size"],
        optimizer=config["train"]["optimizer"],
        patiente_early_stopping=config["train"]["patiente_early_stopping"],
        patiente_learning_rate=config["train"]["patiente_learning_rate"],
        train_size=config["train"]["train_size"],
        seed=config["train"]["seed"],
    shell:
        """/usr/bin/time -v panspace trainer train-autoencoder \
        --datadir {params.datadir} \
        --outdir {params.outdir} \
        --autoencoder {params.autoencoder} \
        --latent-dim {params.latent_dim} \
        --kmer {params.kmer} \
        --epochs {params.epochs} \
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
        "../envs/panspace.yaml"
    shell:
        "/usr/bin/time -v panspace trainer split-autoencoder --path-checkpoint {input} --dirsave {params.dir_save} 2> {log}"

rule files_to_index_and_query:
    output:
        files_to_index=Path(PATH_TRAIN).joinpath("files_to_index.txt"),
        files_to_query=Path(PATH_TRAIN).joinpath("files_to_query.txt")
    input:
        Path(PATH_TRAIN).joinpath("split-train-val-test.json")
    run:
        """Create a .txt file with paths and labels for the index"""
        import json
        with open(input[0],"r") as fp:
            datasets = json.load(fp)
        paths_train = datasets["id_labels"]["train"]
        paths_val   = datasets["id_labels"]["val"]
        paths_test  = datasets["id_labels"]["test"]
        
        paths_index = paths_train + paths_val

        labels_train = datasets["labels"]["train"]
        labels_val   = datasets["labels"]["val"]
        labels_test  = datasets["labels"]["test"]
        labels_index = labels_train + labels_val

        with open(output[0],"w") as fp:
            for path, label in zip(paths_index, labels_index):
                fp.write(f"{path}\t{label}\n")

        with open(output[1],"w") as fp:
            for path, label in zip(paths_test, labels_test):
                fp.write(f"{path}\t{label}\n")

rule create_index:
    output:
        Path(PATH_TRAIN).joinpath("faiss-embeddings/panspace.index"),
        Path(PATH_TRAIN).joinpath("faiss-embeddings/embeddings.npy"),
        Path(PATH_TRAIN).joinpath("faiss-embeddings/id_embeddings.json"),
    input:
        Path(PATH_TRAIN).joinpath("models/encoder.keras"),
        Path(PATH_TRAIN).joinpath("files_to_index.txt")
    params:
        latent_dim=LATENT_DIM
    resources:
        nvidia_gpu=1
    log:
        Path(PATH_TRAIN).joinpath("logs/create_index.log")
    conda: 
        "../envs/panspace.yaml"
    shell:
        """/usr/bin/time -v panspace index create \
        --files-to-index {input[1]} \
        --col-labels 1 \
        --path-encoder {input[0]} \
        --path-index {output[0]}\
        --latent-dim {params.latent_dim} 2> {log}"""

rule test_index:
    output:
        embeddings=Path(PATH_TRAIN).joinpath("test/embeddings.npy"),
        query=Path(PATH_TRAIN).joinpath("test/query_results.csv"),
    input:
        path_index=Path(PATH_TRAIN).joinpath("faiss-embeddings/panspace.index"),
        path_encoder=Path(PATH_TRAIN).joinpath(f"models/encoder.keras"),
        files_to_query=Path(PATH_TRAIN).joinpath("files_to_query.txt")
    params:
        path_index=Path(PATH_TRAIN).joinpath("faiss-embeddings/panspace.index"),
        outdir=Path(PATH_TRAIN).joinpath("test")
    resources:
        nvidia_gpu=1
    log:
        Path(PATH_TRAIN).joinpath("logs/test_index.log")
    conda: 
        "../envs/panspace.yaml"
    shell:        
        """
        /usr/bin/time -v panspace index query \
        --path-fcgr {input.files_to_query} \
        --path-encoder {input.path_encoder} \
        --path-index {input.path_index} \
        --outdir {params.outdir} 2> {log}
        """