configfile: "params.yaml"
from os.path import join as pjoin

# check all tarfiles
DIR_TARFILES=config["fcgr"]["dir_tarfiles"]
TARFILES,= glob_wildcards(pjoin(DIR_TARFILES,"{tarfile}"+".tar.xz"))
print(list(TARFILES))

KMER=config["kmer_size"]
OUTDIR=config["outdir"]
# mkdir -p {params.tmp_kmc}

rule all:
    input:
        expand(pjoin(OUTDIR, "kmer-count","{tarfile}", "summary.txt"), tarfile=TARFILES)

rule count_kmers:
    input:
        tarfile=pjoin(DIR_TARFILES,"{tarfile}" + ".tar.xz")
    output: 
        check=pjoin(OUTDIR, "kmer-count", "{tarfile}", "summary.txt")
    conda:
        "envs/kmc.yaml"
    params:
        max_ram=4,
        tmp_kmc="tmp-kmc",
        kmer_size=KMER,
        path_kmer_count=pjoin(OUTDIR, "kmer-count")
    shell:
        """
        ./scripts/count_kmers.sh {input.tarfile} {output.check} {params.kmer_size} {params.path_kmer_count}
        """