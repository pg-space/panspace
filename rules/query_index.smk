"""
This script query the index with fasta files in a folder
The output is a numpy file with the embeddings and a CSV with the top-10 predictions and distances
"""

configfile: "panspace-query.yaml"
from pathlib import Path
from os.path import join as pjoin

KMER_SIZE=6#config["kmer_size"]
# PATH_EXP=Path(config["outdir"]).joinpath(f"{KMER_SIZE}mer").joinpath(config["train"]["name_experiment"])#.joinpath("cross-validation/mean_squared_error-relu-relu-1-fold")
PATH_EXP=Path(config["query"]["path_panspace"])
OUTDIR = Path(config["query"]["outdir"])
DIR_FASTA=Path(config["query"]["dir_fasta"])
# DIR_FCGR=Path(config["query"]["dir_fcgr"])

# path_by_fcgr  = {p.stem: str(p) for p in DIR_FCGR.rglob("*npy")} 
# pfcgr = path_by_fcgr.keys()
# path_by_fasta  = {p.stem: str(p) for p in DIR_FASTA.rglob("*fa") }# if p.stem in pfcgr } 
# TODO: extensions: fasta fa fna
path_by_fasta  = {p.stem: str(p) for p in DIR_FASTA.rglob("*fna") } # if p.stem in pfcgr } 

LIST_FASTA = list(path_by_fasta.keys())

# LIST_FCGR = list(path_by_fcgr.keys())
# LIST_FASTA = LIST_FCGR
# print(LIST_FASTA)

rule all:
    input:
        pjoin(OUTDIR, "embeddings.npy"),
        pjoin(OUTDIR, "query.csv")

rule count_kmers:
    input:
        lambda wildcards: path_by_fasta[wildcards.fasta]
    output:
        # temp(
        pjoin(OUTDIR, "fcgr","{fasta}.kmer-count.txt")
            # )
    params:
        kmer=KMER_SIZE,
    conda:
        "../envs/kmc.yaml"
    log:
        kmc=OUTDIR.joinpath("logs/count_kmers_kmc-{fasta}.log"),
        dump=OUTDIR.joinpath("logs/count_kmers_dump-{fasta}.log"),
    shell:
        # TODO: split rule and check check if the bottleneck is the dump step
        """
        mkdir -p tmp-kmc
        /usr/bin/time -v kmc -v -k{params.kmer} -m4 -sm -ci0 -cs100000 -b -t4 -fm {input} {input} "tmp-kmc" 2> {log.kmc}
        /usr/bin/time -v kmc_tools -t4 -v transform {input} dump {output} 2> {log.dump}
        rm -r {input}.kmc_pre {input}.kmc_suf
        """

rule fcgr:
    input: 
        pjoin(OUTDIR, "fcgr", "{fasta}.kmer-count.txt")
    output:
        pjoin(OUTDIR, "fcgr", "{fasta}.npy")
    params:
        kmer=KMER_SIZE
    conda: 
        "../envs/panspace.yaml"
    log:
        OUTDIR.joinpath("logs/fcgr-{fasta}.log")
    shell:
        """
        /usr/bin/time -v panspace trainer fcgr -k {params.kmer} --path-kmer-counts {input} --path-save {output} 2> {log}
        """

rule query_index:
    input:
        expand( pjoin(OUTDIR, "fcgr", "{fasta}.npy"), fasta=LIST_FASTA),
    output:
        pjoin(OUTDIR, "embeddings.npy"),
        temp(pjoin(OUTDIR, "query_results.csv"))
    conda:
        "../envs/panspace.yaml"
    resources:
        nvidia_gpu=1
    params:
        path_fcgr=pjoin(OUTDIR,"fcgr"),
        path_encoder=PATH_EXP.joinpath("models/encoder.keras"),
        path_index=PATH_EXP.joinpath("faiss-embeddings/panspace.index"),
        outdir=OUTDIR
    log:
        OUTDIR.joinpath("logs/query_index.log")
    shell:
        """
        /usr/bin/time -v panspace index query \
        --path-encoder {params.path_encoder} \
        --path-index {params.path_index} \
        --path-fcgr {params.path_fcgr} \
        --outdir {params.outdir} 2> {log}
        """

rule add_path_fasta_to_predictions:
    input:
        pjoin(OUTDIR, "query_results.csv")
    output:
        pjoin(OUTDIR, "query.csv")
    run:
        import pandas as pd 
        df = pd.read_csv(input[0])
        df.insert(0, "path_fasta", df["sample_id_query"].apply(lambda sample_id: path_by_fasta[sample_id]))
        df.to_csv(output[0],sep="\t")