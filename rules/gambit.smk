"""
Evaluate GAMBIT
"""

from pathlib import Path

GAMBIT_DATABASE="/data/bacteria/gambit"
PATH_DATASETS=Path("/data/bacteria/gold-standard-datasets")
OUTDIR=Path("/data/bacteria/tools-evaluation/gambit")

ACCESSIONS_NCBI={
    "NCTC3000": "PRJEB6403",
    "GEBA": "PRJNA30815",
    "FDA-ARGOS": "PRJNA231221",
}
datasets = list(ACCESSIONS_NCBI.keys())

rule all:
    input: 
        expand(
            OUTDIR.joinpath("output-gambit-{dataset}.csv"), dataset=datasets
        )

# TODO: remove unzip and create_list_paths rules
checkpoint unzip:
    output:
        directory(PATH_DATASETS.joinpath("{dataset}")) 
    input:
        PATH_DATASETS.joinpath("{dataset}/ncbi_dataset.zip"),
    params:
        outdir_zip=lambda w: PATH_DATASETS.joinpath(f"{w.dataset}"),
        path_datasets=PATH_DATASETS
    log:
        OUTDIR.joinpath("logs/{dataset}-unzip.log")
    shell:
        """
        unzip {input} -d {params.outdir_zip}
        """        


rule create_list_paths:
    output:
        PATH_DATASETS.joinpath("{dataset}/list_paths.txt"),
    input:
        PATH_DATASETS.joinpath("{dataset}/ncbi_dataset/data") 
        # directory(PATH_DATASETS.joinpath("{dataset}"))
        # PATH_DATASETS.joinpath("{dataset}/ncbi_dataset.zip"),
    params:
        outdir_zip=lambda w: PATH_DATASETS.joinpath(f"{w.dataset}"),
        path_datasets=PATH_DATASETS
    log:
        OUTDIR.joinpath("logs/{dataset}-create_list_paths.log")
    shell:
        """
        ls {params.outdir_zip}/ncbi_dataset/data/*/*fna | while read f; do echo $f >> {output}; done
        """


rule classify:
    output:
        OUTDIR.joinpath("output-gambit-{dataset}.csv")
    input:
        PATH_DATASETS.joinpath("{dataset}/list_paths.txt")
    conda: 
        "../envs/gambit.yaml"
    log:
        OUTDIR.joinpath("logs/{dataset}-classify.log")
    params:
        database=GAMBIT_DATABASE
    threads:
        8
    shell:
        """
        /usr/bin/time -v gambit -d {params.database} \
        query -l {input} \
        -o  {output} \
        --progress -f csv -c {threads} 2> {log}
        """
