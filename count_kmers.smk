configfile: "params.yaml"
from os.path import join as pjoin

# check all tarfiles
DIR_TARFILES=config["fcgr"]["dir_tarfiles"]
TARFILES,= glob_wildcards(pjoin(DIR_TARFILES,"{tarfile}"+".tar.xz"))
print(list(TARFILES))

KMER=config["kmer_size"]

# mkdir -p {params.tmp_kmc}

rule all:
    input:
        expand(pjoin("{tarfile}", "summary.txt"), tarfile=TARFILES)

rule count_kmers:
    input:
        tarfile=pjoin(DIR_TARFILES,"{tarfile}" + ".tar.xz")
    output: 
        check=pjoin("{tarfile}", "summary.txt")
    conda:
        "envs/kmc.yaml"
    params:
        max_ram=4,
        tmp_kmc="tmp-kmc",
        kmer_size=KMER
    shell:
        """
        touch {output.check}
        mkdir -p {params.tmp_kmc}
        tar -tvf {input.tarfile} | \
        awk -F" " '{{ if($NF != "") print $NF }}'  | \
        head -n 2 | \
        while read f
            do
                echo $f 
                tar --extract --file={input.tarfile} $f
                kmc --verbose -k{params.kmer_size} -m{params.max_ram} -sm -ci0 -cs255 -b -t4 -fa $f $f {params.tmp_kmc}
                kmc_tools -t4 -v transform $f dump $f.kmer.txt
                rm -r $f $f.kmc_pre $f.kmc_suf
            done
        """