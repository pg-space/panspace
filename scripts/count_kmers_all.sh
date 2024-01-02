#!/bin/bash

# inputs (tarfile, summarypath, kmersize, path save count kmers)
TARFILE=$1
# OUTFILE=$2
# KMER=$1
PATH_KCOUNTS=$2

mkdir -p $PATH_KCOUNTS
mkdir -p "tmp-kmc"
tar -tvf $TARFILE | \
awk -F" " '{{ if($NF != "") print $NF }}'  | \
head -n 2 | \
while read f
    do  
        tar --extract --file=$TARFILE -C $PATH_KCOUNTS $f
        # kmc -v -k$KMER -m4 -sm -ci0 -cs100000 -b -t4 -fa "$PATH_KCOUNTS/$f" "$PATH_KCOUNTS/$f" "tmp-kmc"
        # kmc_tools -t4 -v transform "$PATH_KCOUNTS/$f" dump "$PATH_KCOUNTS/$f.kmer.txt" 
        # rm -r "$PATH_KCOUNTS/$f" "$PATH_KCOUNTS/$f.kmc_pre" "$PATH_KCOUNTS/$f.kmc_suf" 
        # echo "Done with $f" >> $OUTFILE
    done
