#!/usr/bin/bash
total=3  # Set the total parameter

for ((n=1; n<=total; n++)); do
    snakemake -s scripts/fcgr_allthebacteria.smk -c8 \
        --use-conda \
        --config \
            kmer_size=8 \
            datadir=/home/avila/Servers/watson/data \
            subset=test \
            kmc_threads=2 \
            bin_fcgr=/home/avila/Servers/watson/fcgr/fcgr \
        --batch fcgr_verification=$n/$total
done
