#!/bin/bash

# inputs (tarfile, summarypath, kmersize, path save count kmers)
TARFILE=$1
OUTFILE=$2
KMER=$3
PATH_KCOUNTS=$4

mkdir -p $PATH_KCOUNTS
mkdir -p "tmp-kmc"
tar -tvf $TARFILE | \
awk -F" " '{{ if($NF != "") print $NF }}'  | \
head -n 2 | \
while read f
    do  
        if [! -f "$PATH_KCOUNTS/$f.kmer.txt"]
        then
            tar --extract --file=$1 -C $PATH_KCOUNTS $f
            kmc -v -k$KMER -m4 -sm -ci0 -cs255 -b -t4 -fa "$PATH_KCOUNTS/$f" "$PATH_KCOUNTS/$f" "tmp-kmc"
            kmc_tools -t4 -v transform "$PATH_KCOUNTS/$f" dump "$PATH_KCOUNTS/$f.kmer.txt" 
            rm -r "$PATH_KCOUNTS/$f" "$PATH_KCOUNTS/$f.kmc_pre" "$PATH_KCOUNTS/$f.kmc_suf" 
        fi
        echo "Done with $f" >> $OUTFILE
    done