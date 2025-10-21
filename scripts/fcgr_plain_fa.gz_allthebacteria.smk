workdir: "."
configfile: "scripts/config_fcgr.yml"

"""
- This pipeline creates FCGR representations as .npy files using the AllTheBacteria dataset
where fasta files are stored in folders as *.fa.gz 

- It requires that all folders (<batch_name>/) are stored in <dir_sequences> directory. Eg: dir_sequences/batches/achromobacter_xylosoxidans__01

- For each batch, the FCGRs will be saved in <outdir>/fcgr-mask<mask>/<batch_name>
"""

import json
from os.path import join as pjoin
from pathlib import Path

# params
MASKS=config["mask"]; print("Mask:", MASKS, type(MASKS))
KMER=sum([int(x) for x in MASKS[0]]); print("Kmer size:", KMER)
KMER_KMC = len(MASKS[0]); print("Kmer size for KMC:", KMER_KMC)
DATADIR=Path(config["dir_sequences"])
OUTDIR=Path(config["outdir"])
SUBSET=config["subset"]

# Find all folders in <dir_sequences> directory
def load_batches(subset):
    list_folders=[]
    with open(DATADIR.joinpath(f"allthebacteria_{subset}.txt")) as fp:
        for line in fp.readlines():
            foldername = line.replace("\n","").strip()
            list_folders.append(foldername)
    return list_folders

print("FCGR mask:", config["mask"])
BATCHES=load_batches(SUBSET)

rule all:
    input:
        expand(pjoin(OUTDIR, "flags", "kmer-deleted-{batch_name}.flag"), batch_name=BATCHES)
        
# -- 1. Count k-mers

# store KMC output (.kmc_pre and .kmc_suf) in fcgr/ directory
rule count_kmers:
    input:
        pjoin(DATADIR, "{batch_name}", "{fasta}.fa.gz")
    output:
        pjoin(OUTDIR, "kmer-count", "{batch_name}", "{fasta}.kmc_pre"),
        pjoin(OUTDIR, "kmer-count", "{batch_name}", "{fasta}.kmc_suf"),
    log:
        pjoin(OUTDIR, "logs", "count_kmers-{batch_name}-{fasta}.log")
    params:
        kmer=KMER_KMC,
        out=lambda wildcards: pjoin(OUTDIR, "kmer-count", f"{wildcards.batch_name}", f"{wildcards.fasta}"),
        mem_gb=lambda wildcards, resources: int(resources.mem_mb) // 1024,
        tmp_dir = lambda wildcards: f"tmp_kmc/{wildcards.fasta}"
    conda:
        "envs/kmc.yml"
    threads:
        config["kmc_threads"],
    resources:
        mem_mb=16_000,
    retries: 2,
    shell:
        """
        mkdir -p {params.tmp_dir}
        timeout 10s /usr/bin/time -v kmc -v -k{params.kmer} -m{params.mem_gb} -sm -ci0 -cs65535 -b -t{threads} -fm {input} {params.out} {params.tmp_dir} 2> {log}
        """

# -- 2. create list of kmc files to run fcgr tool

def get_kmc_sufs(wildcards):
    "Get input for list_path_kmc_output rule"
    dir_files = DATADIR.joinpath(wildcards.batch_name)
    fastas = [p.stem.replace(".fa","") for p in dir_files.glob("*.fa.gz")]
    return expand(pjoin(OUTDIR, "kmer-count", wildcards.batch_name, "{fasta}.kmc_suf"),
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

# -- 4. create a flag to check that all FCGR for a given mask were created

# check that FCGR were created for each batch-mask pair
def aggregate_numpy_fcgr(wildcards):
    "Helper function to collect all FCGR .npy files generated for a set of assemblies of a folder"
    output_batch = checkpoints.save_fcgr_as_numpy.get(**wildcards).output[0]
    list_fasta = glob_wildcards(pjoin(output_batch, "{fasta}.fa.gz")).fasta
    return expand(pjoin(OUTDIR.joinpath(f"fcgr-mask{wildcards.mask}"), f"{wildcards.batch_name}", "{fasta}.npy"), fasta=list_fasta)    

rule fcgr_aggregate_mask:
    input: 
        aggregate_numpy_fcgr
    output: 
        pjoin(OUTDIR, "flags","{batch_name}-mask-{mask}.flag")
    priority:
        200
    log:
        pjoin(OUTDIR, "logs", "fcgr_aggregate_mask-{batch_name}_{mask}.log")
    shell:
        """
        echo '{wildcards.batch_name}-{wildcards.mask} done'
        echo 'all masks done' > {output} 2> {log}
        """

# check that FCGR were created for ALL MASKS for one batch, and delete kmer counts
rule fcgr_aggregate_all_masks:
    input:
        flags = [ pjoin(OUTDIR, "flags", f"{{batch_name}}-mask-{mask}.flag") for mask in MASKS ],
    output:
        pjoin(OUTDIR, "flags", "all-masks-{batch_name}.flag")
    log:
        pjoin(OUTDIR, "logs", "fcgr_aggregate_all_masks-{batch_name}.log")
    shell:
        """
        echo "Checking input flags for {wildcards.batch_name}..." > {log}
        for f in {input.flags}; do
            if [ ! -f "$f" ]; then
                echo "Missing required input flag: $f" >> {log}
                exit 1
            fi
        done

        echo "All masks done successfully for {wildcards.batch_name}" >> {log}
        echo "done" > {output}
        """

rule delete_kmer_counts:
    input:
        flag = pjoin(OUTDIR, "flags", "all-masks-{batch_name}.flag")
    output:
        pjoin(OUTDIR, "flags", "kmer-deleted-{batch_name}.flag")
    params:     
        kmerdir=lambda w: pjoin(OUTDIR,"kmer-count",f"{w.batch_name}"),
    shell:
        """
        echo 'Deleting kmer counts for {wildcards.batch_name}'

        if [ -d "{params.kmerdir}" ]; then
            rm -rf "{params.kmerdir}"
            if [ ! -d "{params.kmerdir}" ]; then
                echo "Successfully deleted {params.kmerdir}"
            else
                echo "Warning: Failed to delete {params.kmerdir}" >&2
                exit 1
            fi
        else
            echo "Directory {params.kmerdir} does not exist. Skipping deletion."
        fi

        echo 'deleted' > {output}
        """