workdir: "."
configfile: "scripts/config.yml"

"""
This script query the index with fasta files in a folder
The output is a numpy file with the embeddings and a CSV with the top-10 predictions and distances
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
    input:
        lambda wildcards: path_by_seqid[wildcards.seqid]
    output:
        temp(
        pjoin(OUTDIR, "fcgr","{seqid}.kmer-count.txt")
            )
    params:
        kmer=KMER_SIZE,
    conda:
        "envs/kmc.yml"
    log:
        kmc=OUTDIR.joinpath("logs/count_kmers_kmc-{seqid}.log"),
        dump=OUTDIR.joinpath("logs/count_kmers_dump-{seqid}.log"),
    shell:
        """
        mkdir -p tmp-kmc
        /usr/bin/time -v kmc -v -k{params.kmer} -m4 -sm -ci0 -cs100000 -b -t4 -fm {input} {input} "tmp-kmc" 2> {log.kmc}
        /usr/bin/time -v kmc_tools -t2 -v transform {input} dump {output} 2> {log.dump}
        rm -r {input}.kmc_pre {input}.kmc_suf
        """

rule fcgr:
    input: 
        pjoin(OUTDIR, "fcgr", "{seqid}.kmer-count.txt")
    output:
        pjoin(OUTDIR, "fcgr", "{seqid}.npy")
    params:
        kmer=KMER_SIZE
    conda: 
        f"envs/{HARDWARE}.yml"
    log:
        std=OUTDIR.joinpath("logs/fcgr-{seqid}.log"),
        err=OUTDIR.joinpath("logs/fcgr-{seqid}.err.log"),
    shell:
        """
        /usr/bin/time -vo {log.std} panspace fcgr from-kmer-counts \
            --kmer {params.kmer} \
            --path-kmer-counts {input} \
            --path-save {output} 2> {log.err}
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
        std=OUTDIR.joinpath("logs/query_index.log"),
        err=OUTDIR.joinpath("logs/query_index..err.log"),
    shell:
        """
        /usr/bin/time -vo {log.std} panspace index query \
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