configfile: "params-stats.yaml"
import json
import tarfile
from os.path import join as pjoin
from tqdm import tqdm
from collections import defaultdict
from pathlib import Path

# params
OUTDIR=Path(config["outdir"])

# # --- check all tarfiles ---
DIR_TARFILES=config["fcgr"]["dir_tarfiles"]
# TARFILES = ["vibrio_shilonii__01", "vibrio_vulnificus__01"]
TARFILES,= glob_wildcards(pjoin(DIR_TARFILES,"{tarfile}"+".tar.xz"))
# TARFILES = [tarfile for tarfile in TARFILES if "__01" not in tarfile]
print(TARFILES)

rule all:
    input:
        expand( pjoin(OUTDIR, "stats_{tarfile}.csv"), tarfile=TARFILES )

# outut fasta files in assembly/ directory
checkpoint decompress_tarxz:
    input: 
        pjoin(DIR_TARFILES, "{tarfile}" + ".tar.xz")
    output:
        directory(pjoin(OUTDIR, "assembly" ,"{tarfile}"))
    log:
        pjoin(OUTDIR, "logs", "decompress_tarxz-{tarfile}.log")
    params:
        outdir=pjoin(OUTDIR,"assembly")
    resources:
        limit_space=5,
    #     disk_mb=20_000_000
    shell:
        """
        mkdir -p {params.outdir}
        /usr/bin/time -v tar -xvf {input} -C {params.outdir} 2> {log}
        """

def aggregate_fasta(wildcards,):
    "Helper function to collect all fasta files of a tarfile"
    
    output_tarfile = checkpoints.decompress_tarxz.get(**wildcards).output[0]
    list_fasta = glob_wildcards( pjoin(output_tarfile, "{fasta}.fa") ).fasta
    return expand(pjoin(output_tarfile, "{fasta}.fa"), fasta=list_fasta)
    
rule stats:
    input:  
        aggregate_fasta
    output: 
        pjoin(OUTDIR, "stats_{tarfile}.csv")
    params:
        dir_fasta = lambda w: pjoin(OUTDIR, "assembly" ,f"{w.tarfile}")
    log:
        pjoin(OUTDIR, "logs", "stats-{tarfile}.log")
    conda: 
        "../envs/panspace.yaml"
    priority:
        500
    shell:
        """
        /usr/bin/time -v panspace stats-assembly compute --fasta {params.dir_fasta} --outdir {output} 2> {log}
        rm -r {params.dir_fasta}
        """
