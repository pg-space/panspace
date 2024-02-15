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

configfile: "params-metric-learning.yaml"
import json
from pathlib import Path
import datetime
import copy

KMER = config["kmer_size"]
OUTDIR=Path(config["outdir"])
PATH_FCGR = Path(config["path_fcgr"]) #Path(OUTDIR).joinpath(f"{KMER}mer/fcgr")
NAME_EXPERIMENT=config["train"]["name_experiment"]
PATH_TRAIN=Path(OUTDIR).joinpath(f"{KMER}mer/{NAME_EXPERIMENT}/cross-validation")
ARCHITECTURE = config["train"]["architecture"]
LATENT_DIM = config["train"]["latent_dim"]
KFOLD = config["train"]["kfold"]
KFOLDS = [x+1 for x in range(KFOLD)]
LABELS = config["labels"]
PERCENTIL = config["outliers"]["percentil_avg_distance"] 

LOSS = config["train"]["loss"]
HIDDEN_ACTIVATION = config["train"]["hidden_activation"]

# save params used to run these pipeline

_params = config["train"]
# _params["datetime"] =  datetime.datetime.now()
_params["kmer_size"] = KMER

path_save_params = Path(PATH_TRAIN).joinpath("params.yaml")
path_save_params.parent.mkdir(exist_ok=True, parents=True)
with open(path_save_params, "w") as fp: 
    json.dump(_params, fp, indent=1)


def get_outputs(wildcards):

    outputs = []
    for kfold in KFOLDS: 
        
        outputs.extend(
            Path(PATH_TRAIN).joinpath(f"{loss}-{hidden_activation}-{kfold}-fold/data-curation/outliers_avg_dist_percentile.csv")
            for loss, hidden_activation in zip(LOSS, HIDDEN_ACTIVATION)
        )
        outputs.extend(
            Path(PATH_TRAIN).joinpath(f"{loss}-{hidden_activation}-{kfold}-fold/data-curation/percentile_threshold.json")
            for loss, hidden_activation in zip(LOSS, HIDDEN_ACTIVATION)
        )
        # outputs.extend(
        #     PATH_TRAIN.joinpath(f"{loss}-{hidden_activation}-{kfold}-fold/checkpoints/weights-{ARCHITECTURE}.keras")
        #     for loss, hidden_activation in zip(LOSS, HIDDEN_ACTIVATION)
        # )
        # outputs.extend(
        #     Path(PATH_TRAIN).joinpath(f"{loss}-{hidden_activation}-{kfold}-fold/faiss-embeddings/panspace.index")
        #     for loss, hidden_activation in zip(LOSS, HIDDEN_ACTIVATION)
        # )
        
    return outputs

rule all:
    input:
        get_outputs
        # expand( PATH_TRAIN.joinpath("train_{kfold}-fold.txt") , kfold=KFOLDS),
        # expand( PATH_TRAIN.joinpath("test_{kfold}-fold.txt") , kfold=KFOLDS),
        # expand( PATH_TRAIN.joinpath("{loss}-{hidden_activation}-{output_activation}-{kfold}-fold/checkpoints").joinpath(f"weights-{ARCHITECTURE}.keras"), kfold=KFOLDS),
        # expand( Path(PATH_TRAIN).joinpath("{loss}-{hidden_activation}-{output_activation}-{kfold}-fold/faiss-embeddings/panspace.index"), kfold=KFOLDS),
        # expand( Path(PATH_TRAIN).joinpath("{loss}-{hidden_activation}-{output_activation}-{kfold}-fold/test/query_results.csv"), kfold=KFOLDS)

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
        """/usr/bin/time -v panspace trainer split-data \
        --datadir {params.datadir} \
        --outdir {params.outdir} \
        --kfold {params.kfold} \
        --labels {params.labels} 2> {log}
        """

rule train:
    output:
        PATH_TRAIN.joinpath("{loss}-{hidden_activation}-{kfold}-fold/checkpoints").joinpath(f"weights-{ARCHITECTURE}.keras"),
    input:
        Path(PATH_TRAIN).joinpath("train_{kfold}-fold.txt"),
    log:
        Path(PATH_TRAIN).joinpath("logs/train_{loss}-{hidden_activation}-{kfold}-fold.log")
    conda:
        "../envs/panspace.yaml"
    resources:
        nvidia_gpu=1
    params:
        outdir=lambda w: PATH_TRAIN.joinpath(f"{w.loss}-{w.hidden_activation}-{w.kfold}-fold"),
        architecture=config["train"]["architecture"],
        latent_dim=config["train"]["latent_dim"],
        kmer=config["kmer_size"],
        epochs=config["train"]["epochs"],
        batch_size=config["train"]["batch_size"],
        optimizer=config["train"]["optimizer"],
        margin=config["train"]["margin"],
        patiente_early_stopping=config["train"]["patiente_early_stopping"],
        patiente_learning_rate=config["train"]["patiente_learning_rate"],
        train_size=config["train"]["train_size"],
        seed=config["train"]["seed"],
        loss=lambda wildcards: wildcards.loss,
        hidden_activation=lambda wildcards: wildcards.hidden_activation,
        preprocessing=config["train"]["preprocessing"]
    shell:
        """/usr/bin/time -v panspace trainer train-metric-learning \
        --training-list {input} \
        --outdir {params.outdir} \
        --architecture {params.architecture} \
        --latent-dim {params.latent_dim} \
        --kmer {params.kmer} \
        --preprocessing {params.preprocessing} \
        --epochs {params.epochs} \
        --batch-size {params.batch_size} \
        --batch-normalization \
        --optimizer {params.optimizer} \
        --patiente-early-stopping {params.patiente_early_stopping} \
        --patiente-learning-rate {params.patiente_learning_rate} \
        --hidden-activation {params.hidden_activation} \
        --train-size {params.train_size} \
        --loss {params.loss} \
        --margin {params.margin} \
        --seed {params.seed} 2> {log}
        """

rule create_index:
    output:
        index=Path(PATH_TRAIN).joinpath("{loss}-{hidden_activation}-{kfold}-fold/faiss-embeddings/panspace.index"),
        embeddings=Path(PATH_TRAIN).joinpath("{loss}-{hidden_activation}-{kfold}-fold/faiss-embeddings/embeddings.npy"),
        id_embeddings=Path(PATH_TRAIN).joinpath("{loss}-{hidden_activation}-{kfold}-fold/faiss-embeddings/labels.json"),
    input:
        encoder=Path(PATH_TRAIN).joinpath("{loss}-{hidden_activation}-{kfold}-fold/checkpoints").joinpath(f"weights-{ARCHITECTURE}.keras"),
        files_to_index=Path(PATH_TRAIN).joinpath("train_{kfold}-fold.txt"),
    params:
        latent_dim=LATENT_DIM
    resources:
        nvidia_gpu=1
    log:
        Path(PATH_TRAIN).joinpath("logs/create_index_{loss}-{hidden_activation}-{kfold}-fold.log")
    priority:
        100
    conda: 
        "../envs/panspace.yaml"
    shell:
        """/usr/bin/time -v panspace index create \
        --files-to-index {input.files_to_index} \
        --col-labels 1 \
        --path-encoder {input.encoder} \
        --path-index {output.index}\
        --latent-dim {params.latent_dim} 2> {log}"""

rule test_index:
    output:
        embeddings=Path(PATH_TRAIN).joinpath("{loss}-{hidden_activation}-{kfold}-fold/test/embeddings.npy"),
        query=Path(PATH_TRAIN).joinpath("{loss}-{hidden_activation}-{kfold}-fold/test/query_results.csv"),
    input:
        index=Path(PATH_TRAIN).joinpath("{loss}-{hidden_activation}-{kfold}-fold/faiss-embeddings/panspace.index"),
        encoder=Path(PATH_TRAIN).joinpath("{loss}-{hidden_activation}-{kfold}-fold/checkpoints").joinpath(f"weights-{ARCHITECTURE}.keras"),
        files_to_query=Path(PATH_TRAIN).joinpath("test_{kfold}-fold.txt")
    params:
        outdir=lambda w: Path(PATH_TRAIN).joinpath(f"{w.loss}-{w.hidden_activation}-{w.kfold}-fold/test")
    resources:
        nvidia_gpu=1
    log:
        Path(PATH_TRAIN).joinpath("logs/test_index_{loss}-{hidden_activation}-{kfold}-fold.log")
    conda: 
        "../envs/panspace.yaml"
    priority:
        200
    shell:        
        """
        /usr/bin/time -v panspace index query \
        --path-fcgr {input.files_to_query} \
        --path-encoder {input.encoder} \
        --path-index {input.index} \
        --col-labels 1 \
        --outdir {params.outdir} 2> {log}
        """


# # TODO: cross validation metrics
# # rule cross_validation_metrics:
# #     pass

# # TODO: outlier detection rule
rule outlier_detection:
    output:
        path_outliers = Path(PATH_TRAIN).joinpath("{loss}-{hidden_activation}-{kfold}-fold/data-curation/outliers_avg_dist_percentile.csv"),
        path_threshold = Path(PATH_TRAIN).joinpath("{loss}-{hidden_activation}-{kfold}-fold/data-curation/percentile_threshold.json"),
    input:
        index=Path(PATH_TRAIN).joinpath("{loss}-{hidden_activation}-{kfold}-fold/faiss-embeddings/panspace.index"),
        train_embeddings=Path(PATH_TRAIN).joinpath("{loss}-{hidden_activation}-{kfold}-fold/faiss-embeddings/embeddings.npy"),
        test_embeddings=Path(PATH_TRAIN).joinpath("{loss}-{hidden_activation}-{kfold}-fold/test/embeddings.npy"),
    params:
        train_metadata=lambda w: Path(PATH_TRAIN).joinpath(f"train_{w.kfold}-fold.txt"),
        test_metadata=lambda w: Path(PATH_TRAIN).joinpath(f"test_{w.kfold}-fold.txt"),
        outdir=lambda w: Path(PATH_TRAIN).joinpath(f"{w.loss}-{w.hidden_activation}-{w.kfold}-fold/data-curation"),
        neighbors=10,
        threshold=PERCENTIL,
    conda: 
        "../envs/panspace.yaml"
    log:
        log=Path(PATH_TRAIN).joinpath("logs/outlier_detection_{loss}-{hidden_activation}-{kfold}-fold.log")
    shell:
        """
        /usr/bin/time -v panspace data-curation find-outliers \
        --path-index {input.index} \
        --path-train-embeddings {input.train_embeddings} \
        --path-train-metadata {params.train_metadata} \
        --path-test-embeddings {input.test_embeddings}\
        --path-test-metadata {params.test_metadata} \
        --outdir {params.outdir} \
        --neighbors {params.neighbors} \
        --threshold {params.threshold} 2> {log} 
        """    
# # TODO: mislabeled detection rule