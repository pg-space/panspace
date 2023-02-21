configfile: "params.yaml"
import tarfile
from os.path import join as pjoin

# params 
KMER_SIZE=config["kmer_size"]
OUTDIR=config["outdir"]

# --- check all tarfiles ---
DIR_TARFILES=config["fcgr"]["dir_tarfiles"]
TARFILES,= glob_wildcards(pjoin(DIR_TARFILES,"{tarfile}"+".tar.xz"))

def getnames(tar):
    "get filenames in tarfiles"
    with tarfile.open(tar,"r") as fp:
        return [f for f in  fp.getnames()[:10]]

FILES_BY_TAR = {tar: getnames(pjoin(DIR_TARFILES, tar + ".tar.xz")) for tar in TARFILES }
LIST_FASTA = []
for v in FILES_BY_TAR.values():
    LIST_FASTA.extend(v)

# --- RULES ---
rule all:
    input:
        # expand(pjoin(OUTDIR, "kmer-count", "{fasta}"+".kmer.txt"),fasta=LIST_FASTA),
        expand(pjoin(OUTDIR, "fcgr", "{fasta}.npy"), fasta=LIST_FASTA)
        
rule count_kmers:
    input:
        tarfile=lambda wildcards: \
            pjoin(DIR_TARFILES, f"{Path(wildcards.fasta).parent.stem}" + ".tar.xz") ,
    output:
        kmer_count=pjoin(OUTDIR, "kmer-count", "{fasta}"+".kmer.txt")
    conda:
        "envs/kmc.yaml"
    params:
        max_ram=config["kmc"]["max_ram"],
        tmp_kmc=config["kmc"]["tmp"],
        min_threshold=config["kmc"]["min_threshold"],
        max_threshold=config["kmc"]["max_threshold"],
        kmer_size=KMER_SIZE,
        path_kmer_count=pjoin(OUTDIR, "kmer-count")
    threads:
        config["kmc"]["threads"]
    shell:
        """
        ./scripts/count_kmers.sh {input.tarfile} {wildcards.fasta} {params.kmer_size} {params.path_kmer_count} \
        {params.max_ram} {params.tmp_kmc} {threads} {params.min_threshold} {params.max_threshold}
        """

rule fcgr:
    input: 
        kmer_count=pjoin(OUTDIR, "kmer-count", "{fasta}"+".kmer.txt")
    output:
        fcgr=pjoin(OUTDIR, "fcgr", "{fasta}.npy")
    conda: 
        "envs/fcgr.yaml"
    shell:
        """
        python3 src/fcgr_kmc.py --path-kmc {input.kmer_count} --path-save {output.fcgr}
        """
