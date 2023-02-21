#!/bin/bash

# inputs (tarfile, path to fasta inside the tarfile, kmersize, dir to save kmer counts)
TARFILE=$1
FASTA=$2
KMER=$3
PATH_KCOUNTS=$4
MAX_RAM=$5
TMP=$6
THREADS=$7

mkdir -p $PATH_KCOUNTS
mkdir -p $TMP

# extract one fasta file from the tarfile and count kmers with KMC, keep only the kmer counts
tar --extract --file=$TARFILE -C $PATH_KCOUNTS $FASTA
kmc -v -k$KMER -m$MAX_RAM -sm -ci0 -cs255 -b -t$THREADS -fa "$PATH_KCOUNTS/$FASTA" "$PATH_KCOUNTS/$FASTA" $TMP
kmc_tools -t4 -v transform "$PATH_KCOUNTS/$FASTA" dump "$PATH_KCOUNTS/$FASTA.kmer.txt" 
rm -r "$PATH_KCOUNTS/$FASTA" "$PATH_KCOUNTS/$FASTA.kmc_pre" "$PATH_KCOUNTS/$FASTA.kmc_suf" 