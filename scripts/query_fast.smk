workdir: "."
configfile: "scripts/config.yml"

"""
This script query the index with fasta files in a folder
The output is a numpy file with the embeddings and a CSV with the top-NEIGHBOR predictions and distances
"""

from pathlib import Path
from os.path import join as pjoin

NEIGHBORS=config["neighbors"]
KMER_SIZE=config["kmer"]
PATH_ENCODER=config["path_encoder"]
PATH_INDEX=config["path_index"]
DIR_SEQUENCES=config["dir_sequences"]
OUTDIR = Path(config["outdir"])
HARDWARE = "gpu" if config["gpu"] else "cpu"
FCGRBIN = config["fcgr_bin"]
OUTDIR.mkdir(exist_ok=True, parents=True)
KMC_THREADS=config["kmc_threads"]

# get list of sequences in DIR_SEQUENCES
ALLOWED_EXTENSIONS = [".fa.gz", ".fa", ".fna"]
path_by_seqid = {}
for EXTENSION in ALLOWED_EXTENSIONS:
    path_by_seqid.update(
        {p.stem: str(p) for p in Path(DIR_SEQUENCES).rglob(f"*{EXTENSION}")}
    ) 
LIST_SEQID = list(path_by_seqid.keys())
print(LIST_SEQID)

rule all:
    input:
        pjoin(OUTDIR, "embeddings.npy"),
        pjoin(OUTDIR, "query.csv")


rule count_kmers:
    output:
        # temp()
        pjoin(OUTDIR, "fcgr","{seqid}.kmc_pre"),
        pjoin(OUTDIR, "fcgr","{seqid}.kmc_suf"),
    input:
        lambda wildcards: path_by_seqid[wildcards.seqid]
    params:
        kmer=KMER_SIZE,
        prefix=pjoin(OUTDIR, "fcgr","{seqid}"),
    threads:
        KMC_THREADS,
    conda:
        "envs/kmc.yml"
    log:
        log=OUTDIR.joinpath("logs/count_kmers_kmc-{seqid}.log"),
        err=OUTDIR.joinpath("logs/count_kmers_kmc-{seqid}.err.log"),
    shell:
        """
        mkdir -p tmp-kmc
        /usr/bin/time -vo {log.log} kmc -v -k{params.kmer} -m4 -sm -ci0 -cs100000 -b -t{threads} -fm {input} {params.prefix} 'tmp-kmc' 2> {log.err}
        """


rule list_path_seqid:
    input:  
        expand(
            pjoin(OUTDIR, "fcgr","{seqid}.kmc_suf"),
            seqid=LIST_SEQID
        )
    output: 
        pjoin(OUTDIR, "list_path_kmc.txt")
    params:
        folder_kmc_output=pjoin(OUTDIR, "fcgr")
    log:
        log=OUTDIR.joinpath("logs/list_path_seqid.log"),
        err=OUTDIR.joinpath("logs/list_path_seqid.err.log"),
    shell:
        "/usr/bin/time -vo {log.log} ls {params.folder_kmc_output}/*.kmc_suf | while read f; do echo ${{f::-8}} >> {output} ; done 2> {log.err}"


rule fcgr:
    input:
        pjoin(OUTDIR, "list_path_kmc.txt")
    output:
        expand(
            pjoin(OUTDIR, "fcgr", "{seqid}.npy"),
            seqid=LIST_SEQID,
            )
    params:
        kmer=KMER_SIZE,
        fcgr_bin=FCGRBIN,
    log:
        log=OUTDIR.joinpath("logs/fcgr.log"),
        err=OUTDIR.joinpath("logs/fcgr.err.log"),
    shell:
        """
        /usr/bin/time -vo {log.log} {params.fcgr_bin} {input} 2> {log.err}
        """


rule query_index:
    input:
        expand( pjoin(OUTDIR, "fcgr", "{seqid}.npy"), seqid=LIST_SEQID),
    output:
        pjoin(OUTDIR, "embeddings.npy"),
        temp(pjoin(OUTDIR, "query_results.csv"))
    conda:
        f"envs/{HARDWARE}.yml"
    resources:
        nvidia_gpu=1
    params:
        path_fcgr=pjoin(OUTDIR,"fcgr"),
        path_encoder=PATH_ENCODER,
        path_index=PATH_INDEX,
        outdir=OUTDIR,
        kmer=KMER_SIZE,
    log:
        log=OUTDIR.joinpath("logs/query_index.log"),
        err=OUTDIR.joinpath("logs/query_index.err.log"),
    shell:
        """
        /usr/bin/time -vo {log.log} panspace index query \
            --kmer-size {params.kmer} \
            --path-encoder {params.path_encoder} \
            --path-index {params.path_index} \
            --path-fcgr {params.path_fcgr} \
            --outdir {params.outdir} 2> {log.err}
        """


rule add_path_seq_to_predictions:
    input:
        pjoin(OUTDIR, "query_results.csv")
    output:
        pjoin(OUTDIR, "query.csv")
    run:
        import pandas as pd 
        df = pd.read_csv(input[0], index_col=0)
        df.insert(0, "path_seq", df["sample_id_query"].apply(lambda seqid: path_by_seqid[seqid]))
        df.to_csv(output[0],sep="\t")