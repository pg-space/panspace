#!/usr/bin/bash
# Run the FCGR pipeline sequentially for each batch file in BATCH_DIR.
#
# Usage:
#   bash scripts/run_fcgr_batches.sh [BATCH_DIR] [CORES]
#
# Defaults:
#   BATCH_DIR = batches/
#   CORES     = 8

BATCH_DIR="${1:-batches}"
CORES="${2:-8}"
SMK="scripts/fcgr_plain_fna.gz_GTDB.smk"
CONFIG="scripts/config_fcgr.yml"

echo "Batch dir : $BATCH_DIR"
echo "Cores     : $CORES"
echo "Pipeline  : $SMK"
echo ""

for batch_file in "$BATCH_DIR"/batch_*.txt; do
    batch_name=$(basename "$batch_file" .txt)
    echo "=========================================="
    echo "Processing: $batch_name  ($batch_file)"
    echo "=========================================="

    snakemake \
        -s "$SMK" \
        --configfile "$CONFIG" \
        --config batch_file="$batch_file" \
        -c "$CORES" \
        --use-conda \
        --rerun-incomplete \
        --keep-going

    status=$?
    if [ $status -ne 0 ]; then
        echo "ERROR: snakemake failed for $batch_name (exit $status)" >&2
        echo "Continuing with next batch..."
    else
        echo "Done: $batch_name"
    fi
    echo ""
done

echo "All batches finished."
