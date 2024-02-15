"""
This script query the index with fasta files in a folder
The output is a numpy file with the embeddings and a CSV with the top-10 predictions and distances
"""

configfile: "panspace-query.yaml"
from pathlib import Path
from os.path import join as pjoin
import json

KMER_SIZE=6#config["kmer_size"]
# PATH_EXP=Path(config["outdir"]).joinpath(f"{KMER_SIZE}mer").joinpath(config["train"]["name_experiment"])#.joinpath("cross-validation/mean_squared_error-relu-relu-1-fold")
PATH_EXP=Path(config["path_panspace"])
OUTDIR = Path(config["outdir"])
DIR_FASTA=Path(config["dir_fasta"])
# DIR_FCGR=Path(config["query"]["dir_fcgr"])
OUTDIR.mkdir(exist_ok=True, parents=True)

# TODO: extensions: fasta fa fna
path_by_fasta  = {p.stem: str(p) for p in DIR_FASTA.rglob("*fna") } # if p.stem in pfcgr } 

with open(OUTDIR.joinpath("path_by_fasta.json"),"w") as  fp:
    json.dump(path_by_fasta, fp, indent=1)

LIST_FASTA = list(path_by_fasta.keys())

rule all:
    input:
        pjoin(OUTDIR, "embeddings.npy"),
        pjoin(OUTDIR, "query.csv")

rule count_kmers:
    output:
        # temp()
        pjoin(OUTDIR, "fcgr","{fasta}.kmc_pre"),
        pjoin(OUTDIR, "fcgr","{fasta}.kmc_suf"),
    input:
        lambda wildcards: path_by_fasta[wildcards.fasta]
    params:
        kmer=KMER_SIZE,
        prefix=pjoin(OUTDIR, "fcgr","{fasta}")
    conda:
        "../envs/kmc.yaml"
    log:
        kmc=OUTDIR.joinpath("logs/count_kmers_kmc-{fasta}.log"),
    shell:
        """
        mkdir -p tmp-kmc
        /usr/bin/time -v kmc -v -k{params.kmer} -m4 -sm -ci0 -cs100000 -b -t4 -fm {input} {params.prefix} "tmp-kmc" 2> {log.kmc}
        """

rule list_path_fasta:
    input:  
        expand(
            pjoin(OUTDIR, "fcgr","{fasta}.kmc_suf"),
            fasta=LIST_FASTA
        )
    output: 
        pjoin(OUTDIR, "list_path_kmc.txt")
    params:
        log=OUTDIR.joinpath("logs/list_path_fasta.log"),
        folder_kmc_output=pjoin(OUTDIR, "fcgr")
    shell:
        "ls {params.folder_kmc_output}/*.kmc_suf | while read f; do echo ${{f::-8}} >> {output} ; done 2> {params.log} "
    
rule fcgr:
    input:
        pjoin(OUTDIR, "list_path_kmc.txt")
    output:
        expand(
            pjoin(OUTDIR, "fcgr", "{fasta}.npy"),
            fasta=LIST_FASTA,
            )
    params:
        kmer=KMER_SIZE,
        log=OUTDIR.joinpath("logs/fcgr.log"),
    conda: 
        "../envs/panspace.yaml"
    shell:
        """
        /usr/bin/time -v /home/avila/github/fcgr/fcgr {input} 2> {params.log}
        """

rule query_index:
    input:
        expand(
            pjoin(OUTDIR, "fcgr", "{fasta}.npy"),
            fasta=LIST_FASTA
        ),
    output:
        pjoin(OUTDIR, "embeddings.npy"),
        temp(pjoin(OUTDIR, "query_results.csv")),
    conda:
        "../envs/panspace.yaml"
    resources:
        nvidia_gpu=1
    params:
        path_fcgr=pjoin(OUTDIR,"fcgr"),
        # path_encoder=PATH_EXP.joinpath("models/encoder.keras"),
        path_encoder=PATH_EXP.joinpath("checkpoints/weights-CNNFCGR.keras"),
        path_index=PATH_EXP.joinpath("faiss-embeddings/panspace.index"),
        outdir=OUTDIR,
        log=Path(OUTDIR).joinpath("logs/query_index.log"),
        kmer=KMER_SIZE,
        threshold_outlier=config["threshold_outlier"]
    shell:
        """
        /usr/bin/time -v panspace index query \
        --path-encoder {params.path_encoder} \
        --path-index {params.path_index} \
        --path-fcgr {params.path_fcgr} \
        --kmer-size {params.kmer} \
        --threshold-outlier {params.threshold_outlier} \
        --outdir {params.outdir} 2> {params.log}
        """
        
rule add_path_fasta_to_predictions:
    input:
        pjoin(OUTDIR, "query_results.csv")
    output:
        pjoin(OUTDIR, "query.csv")
    run:
        import pandas as pd 
        df = pd.read_csv(input[0], index_col=0)
        print(df.head(4))
        df.insert(0, "path_fasta", df["sample_id_query"].apply(lambda sample_id: path_by_fasta.get(sample_id,"not-found")))
        df.to_csv(output[0],sep="\t")