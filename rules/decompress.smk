configfile: "params.yaml"
import json
import tarfile
from os.path import join as pjoin
from tqdm import tqdm
from collections import defaultdict
from pathlib import Path

# params 
KMER_SIZE=config["kmer_size"]
OUTDIR=Path(config["outdir"]).joinpath(f"{KMER_SIZE}mer")

# # --- check all tarfiles ---
DIR_TARFILES=config["fcgr"]["dir_tarfiles"]
# TARFILES = ["vibrio_shilonii__01", "vibrio_vulnificus__01"]
TARFILES,= glob_wildcards(pjoin(DIR_TARFILES,"{tarfile}"+".tar.xz"))
TARFILES = [tarfile for tarfile in TARFILES if "__01" in tarfile]
print(TARFILES)

def aggregate_decompress_tarxz(wildcards,):
    
    output_tarfile = checkpoints.decompress_tarxz.get(**wildcards).output[0]
    list_fasta = glob_wildcards( pjoin(output_tarfile, "{fasta}.fa") ).fasta
    
    return expand( pjoin(OUTDIR, "fcgr",f"{wildcards.tarfile}","{fasta}.npy"), fasta=list_fasta)    
    
rule all:
    input:
        expand( pjoin(OUTDIR,"{tarfile}_aggregate.flag"), tarfile=TARFILES)

checkpoint decompress_tarxz:
    input: 
        pjoin(DIR_TARFILES, "{tarfile}" + ".tar.xz")
    output:
        directory(pjoin(OUTDIR, "kmer-count" ,"{tarfile}"))
    params:
        outdir=pjoin(OUTDIR,"kmer-count")
    shell:
        """
        mkdir -p {params.outdir}
        tar -xvf {input} -C {params.outdir}
        """

rule count_kmers:
    input:
        pjoin(OUTDIR, "kmer-count", "{tarfile}", "{fasta}.fa")
    output:
        pjoin(OUTDIR,"kmer-count","{tarfile}", "{fasta}.txt")
    conda:
        "../envs/kmc.yaml"
    params:
        kmer=KMER_SIZE,
    shell:
        """
        mkdir -p tmp-kmc
        kmc -v -k{params.kmer} -m4 -sm -ci0 -cs100000 -b -t4 -fa {input} {input} "tmp-kmc"
        kmc_tools -t4 -v transform {input} dump {output} 
        rm -r {input} {input}.kmc_pre {input}.kmc_suf
        """

rule fcgr:
    input: 
        pjoin(OUTDIR, "kmer-count", "{tarfile}","{fasta}"+".txt"),
    output:
        pjoin(OUTDIR, "fcgr", "{tarfile}","{fasta}.npy")
    params:
        kmer=KMER_SIZE
    conda: 
        "../envs/fcgr.yaml"
    shell:
        """
        python3 src/fcgr_kmc.py -k {params.kmer} --path-kmc {input} --path-save {output}
        """

rule fake_aggregate:
    input: 
        aggregate_decompress_tarxz
    output: 
        touch( pjoin(OUTDIR, "{tarfile}_aggregate.flag"))
