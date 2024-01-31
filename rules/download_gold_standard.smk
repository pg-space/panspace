"""Download datasets
- GEBA
- FDA-ARGOS
- NCTC3000
"""

from pathlib import Path

PATH_DATASETS=Path("/data/bacteria/gold-standard-datasets")
PATH_DATASETS.mkdir(exist_ok=True, parents=True)

ACCESSIONS_NCBI={
    "NCTC3000": "PRJEB6403",
    "GEBA": "PRJNA30815",
    "FDA-ARGOS": "PRJNA231221",
}
datasets = list(ACCESSIONS_NCBI.keys())

rule all:
    input: 
        expand(
            PATH_DATASETS.joinpath("{dataset}/ncbi_dataset.zip"), dataset=datasets,    
        )

rule download:
    output:
        PATH_DATASETS.joinpath("{dataset}/ncbi_dataset.zip"),
    # input:
    #     pass
    params:
        accession=lambda w: ACCESSIONS_NCBI[w.dataset],
        filename=lambda w: PATH_DATASETS.joinpath(f"{w.dataset}/ncbi_dataset.zip"),
    conda: 
        "../envs/ncbi.yaml"
    shell:
        "/usr/bin/time -v datasets download genome accession {params.accession} --filename {params.filename}"


# TODO: include rules below
# checkpoint unzip:
#     output:
#         directory(PATH_DATASETS.joinpath("{dataset}")) 
#     input:
#         PATH_DATASETS.joinpath("{dataset}/ncbi_dataset.zip"),
#     params:
#         outdir_zip=lambda w: PATH_DATASETS.joinpath(f"{w.dataset}"),
#         path_datasets=PATH_DATASETS
#     log:
#         OUTDIR.joinpath("logs/{dataset}-unzip.log")
#     shell:
#         """
#         unzip {input} -d {params.outdir_zip}
#         """        


# rule create_list_paths:
#     output:
#         PATH_DATASETS.joinpath("{dataset}/list_paths.txt"),
#     input:
#         PATH_DATASETS.joinpath("{dataset}/ncbi_dataset/data") 
#     params:
#         outdir_zip=lambda w: PATH_DATASETS.joinpath(f"{w.dataset}"),
#         path_datasets=PATH_DATASETS
#     log:
#         OUTDIR.joinpath("logs/{dataset}-create_list_paths.log")
#     shell:
#         """
#         ls {params.outdir_zip}/ncbi_dataset/data/*/*fna | while read f; do echo $f >> {output}; done
#         """
