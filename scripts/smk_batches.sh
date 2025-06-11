#!/usr/bin/bash
total=1  # Set the total parameter

for ((n=1; n<=total; n++)); do
    snakemake -s scripts/fcgr_allthebacteria_mask.smk -c8 \
        --use-conda \
        --config \
            kmer_size=8 \
            datadir=/home/avila/Servers/watson/data \
            subset=test1 \
            mask="111000000011111" \
            kmc_threads=2 \
            bin_fcgr_mask=/home/avila/Servers/watson/fcgr-mask/fcgr/fcgr \
        --batch fcgr_verification=$n/$total
done
