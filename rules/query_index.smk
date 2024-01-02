"""
This script query the index with fasta files in a folder
The output is a numpy file with the embeddings and a CSV with the top-10 predictions and distances
"""

configfile: "params.yaml"
from pathlib import Path
from os.path import join as pjoin

KMER_SIZE=config["kmer_size"]
PATH_EXP=Path(config["outdir"]).joinpath(f"{KMER_SIZE}mer").joinpath(config["train"]["name_experiment"])
OUTDIR = Path(config["query"]["outdir"])
DIR_FASTA=Path(config["query"]["dir_fasta"])

path_by_fasta  = {p.stem: str(p) for p in DIR_FASTA.rglob("*fa")} 
LIST_FASTA = list(path_by_fasta.keys())

print(LIST_FASTA)
print(path_by_fasta)

rule all:
    input:
        pjoin(OUTDIR, "embeddings.npy"),
        pjoin(OUTDIR, "predictions.csv")

rule count_kmers:
    input:
        lambda wildcards: path_by_fasta[wildcards.fasta]
    output:
        temp(pjoin(OUTDIR, "fcgr","{fasta}.kmer-count.txt"))
    params:
        kmer=KMER_SIZE,
    conda:
        "../envs/kmc.yaml"
    shell:
        """
        mkdir -p tmp-kmc
        kmc -v -k{params.kmer} -m4 -sm -ci0 -cs100000 -b -t4 -fa {input} {input} "tmp-kmc"
        kmc_tools -t4 -v transform {input} dump {output} 
        rm -r {input} {input}.kmc_pre {input}.kmc_suf
        """

rule fcgr:
    input: 
        pjoin(OUTDIR, "fcgr", "{fasta}.kmer-count.txt")
    output:
        pjoin(OUTDIR, "fcgr", "{fasta}.npy")
    params:
        kmer=KMER_SIZE
    conda: 
        "../envs/fcgr.yaml"
    shell:
        """
        python3 src/fcgr_kmc.py -k {params.kmer} --path-kmc {input} --path-save {output}
        """

rule query_index:
    input:
        expand( pjoin(OUTDIR, "fcgr", "{fasta}.npy"), fasta=LIST_FASTA),
    output:
        pjoin(OUTDIR, "embeddings.npy"),
        temp(pjoin(OUTDIR, "predictions-aux.csv"))
    conda:
        "../envs/train.yaml"
    resources:
        nvidia_gpu=1
    params:
        path_fcgr=pjoin(OUTDIR,"fcgr"),
        path_exp=PATH_EXP,
        outdir=OUTDIR
    shell:
        """
        python3 src/query_index.py \
        --path-exp {params.path_exp} \
        --path-fcgr {params.path_fcgr} \
        --outdir {params.outdir}
        """

rule add_path_fasta_to_predictions:
    input:
        pjoin(OUTDIR, "predictions-aux.csv")
    output:
        pjoin(OUTDIR, "predictions.csv")
    run:
        import pandas as pd 
        df = pd.read_csv(input[0])
        df["path_fasta"] = df["sample_id_query"].apply(lambda sample_id: path_by_fasta[sample_id])
        df.to_csv(output[0])