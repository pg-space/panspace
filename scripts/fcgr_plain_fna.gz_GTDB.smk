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

MASKS     = config["mask"]
KMER      = sum([int(x) for x in MASKS[0]])
KMER_KMC  = len(MASKS[0])
OUTDIR    = Path(config["outdir"])
BATCH_FILE = config["batch_file"]
BATCH_NAME = Path(BATCH_FILE).stem

print(f"Batch:      {BATCH_NAME}")
print(f"Batch file: {BATCH_FILE}")
print(f"Masks:      {MASKS}")
print(f"Kmer size:  {KMER}  (KMC k: {KMER_KMC})")

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
        kmer    = KMER_KMC,
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
            -v -k{params.kmer} -m{params.mem_gb} -sm -ci0 -cs65535 -b \
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

checkpoint save_fcgr_as_numpy:
    input:
        pjoin(OUTDIR, f"list_path_kmc_{BATCH_NAME}.txt")
    output:
        directory(pjoin(OUTDIR, "fcgr-mask{mask}", BATCH_NAME))
    params:
        kmer    = KMER,
        fcgrdir = lambda w: pjoin(OUTDIR, f"fcgr-mask{w.mask}", BATCH_NAME),
        bin_fcgr = config["bin_fcgr_mask"],
    log:
        pjoin(OUTDIR, "logs", f"fcgr-{BATCH_NAME}_{{mask}}.log")
    priority: 100
    shell:
        """
        mkdir -p {params.fcgrdir}
        /usr/bin/time -v {params.bin_fcgr} \
            -m {wildcards.mask} -o {params.fcgrdir} {input} 2> {log}
        """

# ---------------------------------------------------------------------------
# 4. Aggregate: check all .npy files were written for a given mask
# ---------------------------------------------------------------------------

def aggregate_numpy_fcgr(wildcards):
    """Return expected .npy paths after the checkpoint directory is ready."""
    checkpoints.save_fcgr_as_numpy.get(**wildcards)
    return expand(
        pjoin(OUTDIR, f"fcgr-mask{wildcards.mask}", BATCH_NAME, "{fasta}.npy"),
        fasta=FASTAS,
    )

rule fcgr_aggregate_mask:
    input:
        aggregate_numpy_fcgr
    output:
        pjoin(OUTDIR, "flags", f"{BATCH_NAME}-mask-{{mask}}.flag")
    priority: 200
    log:
        pjoin(OUTDIR, "logs", f"fcgr_aggregate_mask-{BATCH_NAME}_{{mask}}.log")
    shell:
        """
        echo '{wildcards.mask} done for {BATCH_NAME}' > {output} 2> {log}
        """

rule fcgr_aggregate_all_masks:
    input:
        flags = [
            pjoin(OUTDIR, "flags", f"{BATCH_NAME}-mask-{mask}.flag")
            for mask in MASKS
        ]
    output:
        pjoin(OUTDIR, "flags", f"all-masks-{BATCH_NAME}.flag")
    log:
        pjoin(OUTDIR, "logs", f"fcgr_aggregate_all_masks-{BATCH_NAME}.log")
    shell:
        """
        echo "Checking flags for {BATCH_NAME}..." > {log}
        for f in {input.flags}; do
            if [ ! -f "$f" ]; then
                echo "Missing: $f" >> {log}
                exit 1
            fi
        done
        echo "All masks done for {BATCH_NAME}" >> {log}
        echo "done" > {output}
        """

# ---------------------------------------------------------------------------
# 5. Delete KMC counts to free disk space
# ---------------------------------------------------------------------------

rule delete_kmer_counts:
    input:
        flag = pjoin(OUTDIR, "flags", f"all-masks-{BATCH_NAME}.flag")
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
