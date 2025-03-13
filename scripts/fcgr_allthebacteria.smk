workdir: "."
configfile: "scripts/config.yml"

"""
This script creates fcgr from AllTheBacteria dataset saved as bacthes in <batch_name>.asm.tar.xz
It requires that all tar.xz files are stores in <datadir>/batches/<batch_name>.asm.tar.xz
The fcgr will be saved in <datadir>/fcgr/<kmer_size>mer/<batch_name>
"""

import json
import tarfile
from os.path import join as pjoin
from pathlib import Path

# params
KMER=config["kmer_size"]
DATADIR=Path(config["datadir"])
DIRFCGR=DATADIR.joinpath(f"fcgr/{KMER}mer")
SUBSET=config["subset"]

### ---- FCGR ----
def load_batches(subset):
    list_files=[]
    with open(DATADIR.joinpath(f"allthebacteria_{subset}.txt") as fp:
        
        for line in fp.readlines():
            tarxz = line.replace("\n","").strip().split(" ")
            name = tarxz.replace(".asm.tar.xz","")
            list_files.append(name)
    return list_files

print("H0ola")
TARFILES=load_batches(SUBSET)
print(TARFILES)

rule fcgr_verification:
    input:
        expand( pjoin(DIRFCGR,"{tarfile}_fcgr.flag"), tarfile=TARFILES)

# outut fasta files in assembly/ directory
checkpoint decompress_tarxz:
    input: 
        tarfile=pjoin(DATADIR, "batches", "{tarfile}.asm.tar.xz"),
    output:
        directory(pjoin(DATADIR, "assembly" ,"{tarfile}")),
    log:
        pjoin(DATADIR, "logs", "decompress_tarxz-{tarfile}.log"),
    params:
        outdir=pjoin(DATADIR,"assembly"),
    resources:
        limit_space=5,
    #     disk_mb=20_000_000
    shell:
        """
        mkdir -p {params.outdir}
        /usr/bin/time -v tar -xvf {input.tarfile} -C {params.outdir} 2> {log}
        """

# store KMC output (.kmc_pre and .kmc_suf) in fcgr/ directory
rule count_kmers:
    input:
        pjoin(DATADIR, "assembly", "{tarfile}", "{fasta}.fa")
    output:
        pjoin(DATADIR, "kmer-count","{tarfile}","{fasta}.kmc_pre"),
        pjoin(DATADIR, "kmer-count","{tarfile}","{fasta}.kmc_suf"),
    log:
        pjoin(DATADIR, "logs", "count_kmers-{tarfile}-{fasta}.log")
    params:
        kmer=KMER,
        out=lambda w: pjoin(DATADIR, "kmer-count",f"{w.tarfile}",f"{w.fasta}"),
    conda:
        "envs/kmc.yml"
    threads:
        config["kmc_threads"],
    shell:
        """
        /usr/bin/time -v kmc -v -k{params.kmer} -m4 -sm -ci0 -cs65535 -b -t{threads} -fm {input} {params.out} . 2> {log}
        rm -r {input}
        """


def aggregate_fasta_kmc(wildcards,):
    "Helper function to collect all .kmc_suf files resulting from running KMC on the set of assemblies of a tarfile"
    
    output_tarfile = checkpoints.decompress_tarxz.get(**wildcards).output[0]
    list_fasta = glob_wildcards( pjoin(output_tarfile, "{fasta}.fa") ).fasta
    outdir = pjoin(DATADIR, "kmer-count",f"{wildcards.tarfile}")
    return expand( pjoin(outdir,"{fasta}.kmc_suf"), fasta=list_fasta)    

rule list_path_fasta:
    input:  
        aggregate_fasta_kmc
    output: 
        pjoin(DATADIR, "list_path_kmc_{tarfile}.txt")
    params:
        kmerdir=lambda w: pjoin(DATADIR,"kmer-count",f"{w.tarfile}"),
        fcgrdir=lambda w: pjoin(DIRFCGR,f"{w.tarfile}"),
        parent_fcgrdir = lambda w: DIRFCGR
    log:
        DATADIR.joinpath("logs/list_path_fasta-{tarfile}.log")
    shell:
        """
        /usr/bin/time -v ls {params.kmerdir}/*.kmc_suf | while read f; do echo ${{f::-8}} >> {output} ; done 2> {log}
        """


checkpoint save_fcgr_as_numpy:
    input:
        pjoin(DATADIR, "list_path_kmc_{tarfile}.txt")
    output:
        directory(pjoin(DIRFCGR, "{tarfile}"))
    params:
        kmer=KMER,
        kmerdir=lambda w: pjoin(DATADIR,"kmer-count",f"{w.tarfile}"),
        fcgrdir=lambda w: pjoin(DIRFCGR, f"{w.tarfile}"),
        bin_fcgr=config["bin_fcgr"]
    log:
        DATADIR.joinpath("logs/fcgr-{tarfile}.log")
    priority:
        100
    shell:
        """
        /usr/bin/time -v {params.bin_fcgr} {input} 2> {log}
        mkdir -p {params.fcgrdir} 
        mv {params.kmerdir}/*.npy {params.fcgrdir}
        """


def aggregate_numpy_fcgr(wildcards,):
    "Helper function to collect all FCGR .npy files generated for a set of assemblies of a tarfile"
    
    output_tarfile = checkpoints.save_fcgr_as_numpy.get(**wildcards).output[0]
    list_fasta = glob_wildcards( pjoin(output_tarfile, "{fasta}.fa") ).fasta
    return expand( pjoin(DIRFCGR, f"{wildcards.tarfile}", "{fasta}.npy"), fasta=list_fasta)    


rule fcgr_aggregate:
    input: 
        aggregate_numpy_fcgr
    output: 
        touch( pjoin(DIRFCGR, "{tarfile}_fcgr.flag"))
    priority:
        200
    params:     
        kmerdir=lambda w: pjoin(DATADIR,"kmer-count",f"{w.tarfile}"),
        dir_assemblies=pjoin(DATADIR,"assembly"),
        dir_kmer_count=pjoin(DATADIR,"kmer-count"),
    shell:
        """
        rm -rf {params.kmerdir}
        rm -rf {params.dir_assemblies}
        ""