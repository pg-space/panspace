"""
Starting from a dataset of FCGR (.npy files) in folder (PATH_FCGR), 
this pipeline performs a k-fold cross-validation training of the autoencoder. 

For each k-fold, train and test sets (list of paths) are created, 
- the train set is used to train an autoencoder
- the train set is used to create an Index
- the test set is used to identify outliers and mislabeled assemblies
- the test set is used to query the Index 
"""

# wildcards: kfold

configfile: "params.yaml"

from pathlib import Path

KMER = config["kmer_size"]
OUTDIR=Path(config["outdir"])
PATH_FCGR = Path(OUTDIR).joinpath(f"{KMER}mer/fcgr")
NAME_EXPERIMENT=config["train"]["name_experiment"]
PATH_TRAIN=Path(OUTDIR).joinpath(f"{KMER}mer/{NAME_EXPERIMENT}/cross-validation")
ARCHITECTURE = config["train"]["architecture"]
LATENT_DIM = config["train"]["latent_dim"]
KFOLD = config["train"]["kfold"]
KFOLDS = [x+1 for x in range(KFOLD)]
LABELS = config["labels"]

rule all:
    input:
        expand( PATH_TRAIN.joinpath("train_{kfold}-fold.txt") , kfold=KFOLDS),
        expand( PATH_TRAIN.joinpath("test_{kfold}-fold.txt") , kfold=KFOLDS),
        expand( PATH_TRAIN.joinpath("{kfold}-fold/checkpoints").joinpath(f"weights-{ARCHITECTURE}.keras"), kfold=KFOLDS)


rule kfold_split:
    output:
        expand( Path(PATH_TRAIN).joinpath("train_{kfold}-fold.txt") , kfold=KFOLDS),
        expand( Path(PATH_TRAIN).joinpath("test_{kfold}-fold.txt") , kfold=KFOLDS),
    input:
        list(PATH_FCGR.rglob("*.npy"))
    params: 
        datadir=PATH_FCGR, 
        outdir=PATH_TRAIN,
        kfold=KFOLD,
        labels=LABELS
    log:
        Path(PATH_TRAIN).joinpath("logs/kfold_split.log")
    conda: 
        "../envs/panspace.yaml"
    shell:
        "/usr/bin/time -v panspace trainer split-data --datadir {params.datadir} --outdir {params.outdir} --kfold {params.kfold} --labels {params.labels} 2> {log}"

rule train:
    output:
        PATH_TRAIN.joinpath("{kfold}-fold/checkpoints").joinpath(f"weights-{ARCHITECTURE}.keras"),
    input:
        Path(PATH_TRAIN).joinpath("train_{kfold}-fold.txt"),
    log:
        Path(PATH_TRAIN).joinpath("logs/train_{kfold}-fold.log")
    conda:
        "../envs/panspace.yaml"
    resources:
        nvidia_gpu=1
    params:
        outdir=lambda wildcards: PATH_TRAIN.joinpath(f"{wildcards.kfold}-fold"),
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
        --training-list {input} \
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

rule extract_encoder:
    output:
        Path(PATH_TRAIN).joinpath("{kfold}-fold/models/encoder.keras"),
        # Path(PATH_TRAIN).joinpath(f"models/decoder.keras")
    input:
        PATH_TRAIN.joinpath("{kfold}-fold/checkpoints").joinpath(f"weights-{ARCHITECTURE}.keras"),
    params:
        dir_save=Path(PATH_TRAIN).joinpath("{kfold}-fold/models")
    log:
        Path(PATH_TRAIN).joinpath("logs/extract_encoder_{kfold}-fold.log")
    conda: 
        "../envs/panspace.yaml"
    shell:
        "/usr/bin/time -v panspace trainer split-autoencoder --path-checkpoint {input} --dirsave {params.dir_save} --encoder-only 2> {log}"

# rule create_index:
#     pass


# rule test_index:
#     output:
#         embeddings=Path(PATH_TRAIN).joinpath("test/embeddings.npy"),
#         query=Path(PATH_TRAIN).joinpath("test/query_results.csv"),
#     input:
#         path_index=Path(PATH_TRAIN).joinpath("faiss-embeddings/panspace.index"),
#         path_encoder=Path(PATH_TRAIN).joinpath(f"models/encoder.keras"),
#         files_to_query=Path(PATH_TRAIN).joinpath("files_to_query.txt")
#     params:
#         path_index=Path(PATH_TRAIN).joinpath("faiss-embeddings/panspace.index"),
#         outdir=Path(PATH_TRAIN).joinpath("test")
#     resources:
#         nvidia_gpu=1
#     log:
#         Path(PATH_TRAIN).joinpath("logs/test_index.log")
#     conda: 
#         "../envs/panspace.yaml"
#     shell:        
#         """
#         /usr/bin/time -v panspace index query \
#         --path-fcgr {input.files_to_query} \
#         --path-encoder {input.path_encoder} \
#         --path-index {input.path_index} \
#         --outdir {params.outdir} 2> {log}
#         """