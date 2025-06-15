workdir: "."
configfile: "scripts/config_fcgr_plain_fasta.yml"

"""
This script creates fcgr from uncompressed AllTheBacteria dataset, fasta files are saved by bacthes in folders
<batch_name>/

It requires that all folders are stored in <dir_sequences>
For each batch, the FCGRs will be saved in <datadir>/fcgr-mask<mask>/<kmer_size>mer/<batch_name>
"""

import json
from os.path import join as pjoin
from pathlib import Path

# params
MASKS=config["mask"]
print("Mask:", MASKS, type(MASKS))
print(MASKS[0])
KMER=sum([int(x) for x in MASKS[0]])  # kmer size of the FCGR, from the mask
print("Kmer size:", KMER)
KMER_KMC = len(MASKS[0])  # kmer size needed to use KMC
print("Kmer size for KMC:", KMER_KMC)

DATADIR=Path(config["dir_sequences"]) #Path(dir_sequences)
OUTDIR=Path(config["outdir"]) #Path(outdir)
SUBSET="test3"#config["subset"]

# Find all folders in <dir_sequences> directory
def load_batches(subset):
    list_folders=[]
    with open(DATADIR.joinpath(f"allthebacteria_{subset}.txt")) as fp:
        for line in fp.readlines():
            print(line)
            foldername = line.replace("\n","").strip()
            list_folders.append(foldername)
    return list_folders

print("FCGR mask:", config["mask"])
BATCHES=load_batches(SUBSET)
print(BATCHES)

rule all:
    input:
        # expand(pjoin(OUTDIR, "{batch_name}_{mask}.flag"), batch_name=BATCHES, mask=MASKS)
        expand(pjoin(OUTDIR, "flags", "all-masks-{batch_name}.flag"), batch_name=BATCHES)

# -- 1. Count k-mers
# store KMC output (.kmc_pre and .kmc_suf) in fcgr/ directory
rule count_kmers:
    input:
        pjoin(DATADIR, "{batch_name}", "{fasta}.fa")
    output:
        pjoin(OUTDIR, "kmer-count", "{batch_name}", "{fasta}.kmc_pre"),
        pjoin(OUTDIR, "kmer-count", "{batch_name}", "{fasta}.kmc_suf"),
    log:
        pjoin(OUTDIR, "logs", "count_kmers-{batch_name}-{fasta}.log")
    params:
        kmer=KMER_KMC,
        out=lambda w: pjoin(OUTDIR, "kmer-count", f"{w.batch_name}", f"{w.fasta}"),
        mem_gb=lambda wildcards, resources: int(resources.mem_mb) // 1024
    conda:
        "envs/kmc.yml"
    threads:
        config["kmc_threads"],
    resources:
        mem_mb=16_000,
    shell:
        """
        /usr/bin/time -v kmc -v -k{params.kmer} -m{params.mem_gb} -sm -ci0 -cs65535 -b -t{threads} -fm {input} {params.out} . 2> {log}
        """


# -- 2. create list of kmc files to run fcgr tool
all_fastas = glob_wildcards(pjoin(DATADIR, "{batch_name}", "{fasta}.fa"))

def get_kmc_sufs(wildcards):
    "Get input for list_path_kmc_output rule"
    fastas = [f for b, f in zip(all_fastas.batch_name, all_fastas.fasta) if b == wildcards.batch_name]
    return expand(pjoin(OUTDIR, "kmer-count", "{batch_name}", "{fasta}.kmc_suf"),
                  batch_name=wildcards.batch_name,
                  fasta=fastas)

rule list_path_kmc_output:
    input:  
        get_kmc_sufs
    output: 
        pjoin(OUTDIR, "list_path_kmc_{batch_name}.txt")
    params:
        kmerdir=lambda w: pjoin(OUTDIR,"kmer-count",f"{w.batch_name}"),
    log:
        pjoin(OUTDIR, "logs", "list_path_fasta-{batch_name}.log")
    shell:
        """
        /usr/bin/time -v ls {params.kmerdir}/*.kmc_suf | while read f; do echo ${{f::-8}} >> {output} ; done 2> {log}
        """

## -- 3. create FCGR as numpy files with 'fcgr' tool using one mask
checkpoint save_fcgr_as_numpy:
    input:
        pjoin(OUTDIR, "list_path_kmc_{batch_name}.txt")
    output:
        directory(pjoin(OUTDIR.joinpath("fcgr-mask{mask}"), "{batch_name}"))
    params:
        kmer=KMER,
        kmerdir=lambda w: pjoin(OUTDIR,"kmer-count",f"{w.batch_name}"),
        fcgrdir=lambda w: pjoin(OUTDIR.joinpath(f"fcgr-mask{w.mask}"), f"{w.batch_name}"),
        bin_fcgr=config["bin_fcgr_mask"],
    log:
        pjoin(OUTDIR, "logs", "fcgr-{batch_name}_{mask}.log")
    priority:
        100
    shell:
        """
        mkdir -p {params.fcgrdir}
        /usr/bin/time -v {params.bin_fcgr} -m {wildcards.mask} -o {params.fcgrdir} {input} 2> {log}
        """
        # mv {params.kmerdir}/*.npy {params.fcgrdir}

# -- 4. create a flag to check that all FCGR for a given mask were created


# check that FCGR were created for each batch-mask pair
def aggregate_numpy_fcgr(wildcards):
    "Helper function to collect all FCGR .npy files generated for a set of assemblies of a folder"
    output_batch = checkpoints.save_fcgr_as_numpy.get(**wildcards).output[0]
    list_fasta = glob_wildcards(pjoin(output_batch, "{fasta}.fa")).fasta
    return expand(pjoin(OUTDIR.joinpath(f"fcgr-mask{wildcards.mask}"), f"{wildcards.batch_name}", "{fasta}.npy"), fasta=list_fasta)    

rule fcgr_aggregate_mask:
    input: 
        aggregate_numpy_fcgr
    output: 
        touch(pjoin(OUTDIR, "flags","{batch_name}-mask-{mask}.flag"))
    priority:
        200
    shell:
        "echo '{wildcards.batch_name}-{wildcards.mask} done'"

# check that FCGR were created for ALL MASKS for one batch, and delete kmer counts
rule fcgr_aggregate_all_masks:
    input:
        [ pjoin(OUTDIR, "flags", f"{{batch_name}}-mask-{mask}.flag") for mask in MASKS ],
    output:
        touch(pjoin(OUTDIR, "flags", "all-masks-{batch_name}.flag"))
    params:     
        kmerdir=lambda w: pjoin(OUTDIR,"kmer-count",f"{w.batch_name}"),
    shell:
        """
        echo 'All masks done successfully. Removing kmer counts...'
        rm -rf {params.kmerdir}
        """