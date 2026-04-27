workdir: "."
configfile: "scripts/config_gtdb.yml"

"""
Pipeline to create FCGR representations from .fna.gz files (GTDB / NCBI dataset).

- Input: a batch file (batch_file in config) with one absolute path to a .fna.gz file per line.
- The stem of each .fna.gz filename is used as the {fasta} wildcard.
- BATCH_NAME is derived from the batch file stem (e.g. batch_0001.txt → batch_0001).
- Run snakemake separately for each batch file to keep the DAG manageable.

Example config override:
    snakemake -s scripts/fcgr_plain_fna.gz_GTDB.smk --config batch_file=batches/batch_0001.txt
"""

from os.path import join as pjoin
from pathlib import Path

KMER       = config["kmer"]
OUTDIR     = Path(config["outdir"])
BATCH_FILE = config["batch_file"]
BATCH_NAME = Path(BATCH_FILE).stem

print(f"Batch:      {BATCH_NAME}")
print(f"Batch file: {BATCH_FILE}")
print(f"Kmer size:  {KMER}")

# Map fasta_stem → absolute path for every sequence in this batch
FASTA_PATHS: dict = {}
with open(BATCH_FILE) as fh:
    for line in fh:
        line = line.strip()
        if line:
            p = Path(line)
            stem = p.name.replace(".fna.gz", "")
            FASTA_PATHS[stem] = line

FASTAS = list(FASTA_PATHS.keys())
print(f"Sequences:  {len(FASTAS)}")

# ---------------------------------------------------------------------------
# Target
# ---------------------------------------------------------------------------

rule all:
    input:
        pjoin(OUTDIR, "flags", f"kmer-deleted-{BATCH_NAME}.flag")

# ---------------------------------------------------------------------------
# 1. Count k-mers with KMC
# ---------------------------------------------------------------------------

rule count_kmers:
    input:
        lambda wildcards: FASTA_PATHS[wildcards.fasta]
    output:
        pjoin(OUTDIR, "kmer-count", BATCH_NAME, "{fasta}.kmc_pre"),
        pjoin(OUTDIR, "kmer-count", BATCH_NAME, "{fasta}.kmc_suf"),
    log:
        pjoin(OUTDIR, "logs", f"count_kmers-{BATCH_NAME}-{{fasta}}.log")
    params:
        out     = lambda w: pjoin(OUTDIR, "kmer-count", BATCH_NAME, w.fasta),
        mem_gb  = lambda w, resources: int(resources.mem_mb) // 1024,
        tmp_dir = lambda w: f"tmp_kmc/{BATCH_NAME}/{w.fasta}",
    conda:
        "envs/kmc.yml"
    threads:
        config["kmc_threads"]
    resources:
        mem_mb = 16_000
    retries: 2
    shell:
        """
        mkdir -p {params.tmp_dir}
        timeout 10s /usr/bin/time -v kmc \
            -v -k{KMER} -m{params.mem_gb} -sm -ci0 -cs65535 -b \
            -t{threads} -fm \
            {input} {params.out} {params.tmp_dir} 2> {log}
        """

# ---------------------------------------------------------------------------
# 2. Collect paths of KMC output files into a list
# ---------------------------------------------------------------------------

rule list_path_kmc_output:
    input:
        expand(
            pjoin(OUTDIR, "kmer-count", BATCH_NAME, "{fasta}.kmc_suf"),
            fasta=FASTAS,
        )
    output:
        pjoin(OUTDIR, f"list_path_kmc_{BATCH_NAME}.txt")
    params:
        kmerdir = pjoin(OUTDIR, "kmer-count", BATCH_NAME),
    log:
        pjoin(OUTDIR, "logs", f"list_path_kmc-{BATCH_NAME}.log")
    shell:
        """
        /usr/bin/time -v ls {params.kmerdir}/*.kmc_suf \
            | while read f; do echo ${{f::-8}} >> {output}; done 2> {log}
        """

# ---------------------------------------------------------------------------
# 3. Create FCGR numpy arrays
# ---------------------------------------------------------------------------

rule save_fcgr_as_numpy:
    input:
        pjoin(OUTDIR, f"list_path_kmc_{BATCH_NAME}.txt")
    output:
        pjoin(OUTDIR, "flags", f"fcgr-done-{BATCH_NAME}.flag")
    params:
        fcgrdir  = pjoin(OUTDIR, "fcgr", BATCH_NAME),
        bin_fcgr = config["bin_fcgr"],
    log:
        pjoin(OUTDIR, "logs", f"fcgr-{BATCH_NAME}.log")
    shell:
        """
        mkdir -p {params.fcgrdir}
        /usr/bin/time -v {params.bin_fcgr} single \
            -o {params.fcgrdir} {input} 2> {log}
        echo "done" > {output}
        """

# ---------------------------------------------------------------------------
# 4. Delete KMC counts to free disk space
# ---------------------------------------------------------------------------

rule delete_kmer_counts:
    input:
        pjoin(OUTDIR, "flags", f"fcgr-done-{BATCH_NAME}.flag")
    output:
        pjoin(OUTDIR, "flags", f"kmer-deleted-{BATCH_NAME}.flag")
    params:
        kmerdir = pjoin(OUTDIR, "kmer-count", BATCH_NAME)
    shell:
        """
        if [ -d "{params.kmerdir}" ]; then
            rm -rf "{params.kmerdir}"
            [ ! -d "{params.kmerdir}" ] || {{ echo "Failed to delete {params.kmerdir}" >&2; exit 1; }}
            echo "Deleted {params.kmerdir}"
        else
            echo "Directory {params.kmerdir} not found, skipping."
        fi
        echo "deleted" > {output}
        """
