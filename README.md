<p align="center">
  <img src="img/panspace-logo-v5.png" width="300" height="300" alt="Logo">
</p>

<p align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.9--3.10-blue.svg" alt="Python 3.9-3.10"></a>
  <a href="https://www.tensorflow.org/"><img src="https://img.shields.io/badge/TensorFlow-2.0+-FF6F00.svg" alt="TensorFlow"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License"></a>
  <a href="https://doi.org/10.1101/2025.03.19.644115"><img src="https://img.shields.io/badge/DOI-10.1101%2F2025.03.19.644115-blue" alt="DOI"></a>
  <a href="https://pypi.org/project/panspace/"><img src="https://img.shields.io/pypi/v/panspace.svg?logo=pypi" alt="PyPI"></a>
  <a href="https://github.com/pg-space/panspace"><img src="https://img.shields.io/badge/GitHub-pg--space%2Fpansace-blue?logo=github" alt="GitHub"></a>
</p>


<div align="center">
    <strong>Fast and Scalable Indexing for Massive Bacterial Databases</strong>
</div>

<p class="badges">
  <a href="https://doi.org/10.1101/2025.03.19.644115" class="md-button">📄 Paper</a>
  <a href="https://zenodo.org/records/17402877" class="md-button">📦 Models</a>
  <a href="#quick-start" class="md-button md-button--primary">🚀 Quick Start</a>
</p>

---

## Overview

PanSpace is a library for creating and querying vector-based indexes of bacterial genome assemblies. It enables fast similarity search across massive bacterial databases by learning compact embedding representations of genomes.

### How It Works

<div align="center">
    <img src="img/panspace-pipeline.png" width="1200" height="500">
</div>

1. **FCGR Generation**: Genomes are represented as Frequency matrices of Chaos Game Representations (FCGR)
2. **Embedding**: FCGRs are mapped to n-dimensional vectors using a CNN encoder (CNNFCGR)
3. **Indexing & Search**: Embeddings are indexed with FAISS for efficient similarity queries

### Key Features

- **🚀 Fast Queries**: Millisecond-scale searches across millions of genomes
- **📊 FCGR-Based**: Uses Chaos Game Representation for genome encoding
- **🧠 Deep Learning**: CNN-based encoders for learning compact representations
- **🔍 FAISS Integration**: Efficient similarity search at scale
- **📦 Pre-trained Models**: Ready-to-use encoders and indexes available
- **⚙️ Flexible Training**: Supports metric learning (with labels) or autoencoders (unsupervised)
- **🔄 Snakemake Pipelines**: Automated workflows for batch processing

---

## Installation

### Requirements
- Python 3.9 or 3.10 (TensorFlow compatibility)
- Conda or Mamba (recommended)

### Quick Install: from pypi

#### CPU Version
```bash
pip install panspace[cpu]
```

#### GPU Version
```bash
pip install panspace[gpu]
```


### Install from github repository

#### CPU
```bash
pip install "panspace[cpu] @ git+https://github.com/pg-space/panspace.git"
```

#### GPU
```bash
pip install "panspace[gpu] @ git+https://github.com/pg-space/panspace.git"
```

### Install from source

Clone the repository

```bash
git clone https://github.com/pg-space/panspace.git
cd panspace
```

#### CPU Version
```bash
conda env create -f envs/cpu.yml
conda activate panspace-cpu
```

#### GPU Version
```bash
conda env create -f envs/gpu.yml
conda activate panspace-gpu
```

---

## Quick Start

### Try the Interactive App

```bash
panspace app
```

<div align="center">
    <img src="img/panspace-app.gif" width="1200" alt="PanSpace app demo">
</div>

### Query with Pre-trained Models

1. **Download pre-trained encoder and index** from [Zenodo](https://zenodo.org/records/17402877)
2. **Extract the files**:
   ```
   .
   ├── checkpoints/
   │   └── weights-CNNFCGR_Levels.keras
   └── index/
       ├── panspace.index
       ├── labels.json
       └── *.json
   ```
3. **Run queries**:
   ```bash
   panspace query-smk \
       --dir-sequences "path/to/assemblies/" \
       --path-encoder "checkpoints/weights-CNNFCGR_Levels.keras" \
       --path-index "index/panspace.index"
   ```

---

## Available Pre-trained Models

Download from [Zenodo](https://zenodo.org/records/17402877)

| K-mer | Embedding Size | Model File | Status |
|-------|----------------|------------|--------|
| 8 | 256 | `triplet_semihard_loss-ranger-0.5-hq-256-CNNFCGR_Levels-level1-clip80.zip` | ⭐ **Recommended** |
| 6 | 128 | Available in Zenodo | ✓ |
| 7 | 256 | Available in Zenodo | ✓ |
| 8 | 512 | Available in Zenodo | ✓ |

Each `.zip` contains:
- **Encoder**: `checkpoints/<model-name>.keras`
- **Index**: `index/panspace.index`
- **Metadata**: Label mappings and configurations

---


## Running the App with Docker

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed

### Run the App
```bash
sudo docker-compose up --build
```

The app will be available at **http://localhost:8501**

To run in the background (detached mode):
```bash
sudo docker-compose up --build -d
```

### Stop the App
```bash
sudo docker-compose down
```

### Using Your Own Data

Place your files in the local folders:
- `./indexes/` — your FAISS indexes and metadata
- `./sequences/` — your FASTA files for querying

---

## Complete Workflow

### Option 1: Using Pre-trained Models (Recommended)

Perfect for querying existing databases without training.

#### Step 1: Download Models

```bash
# Download from Zenodo
wget https://zenodo.org/records/17402877/files/triplet_semihard_loss-ranger-0.5-hq-256-CNNFCGR_Levels-level1-clip80.zip
unzip triplet_semihard_loss-ranger-0.5-hq-256-CNNFCGR_Levels-level1-clip80.zip
```

#### Step 2: Prepare Query Sequences

Organize your FASTA files in a directory:
```
assemblies/
├── sample1.fa.gz
├── sample2.fa
└── sample3.fna
```

#### Step 3: Query the Index

**Using the Snakemake wrapper** (recommended):
```bash
panspace query-smk \
    --dir-sequences "assemblies/" \
    --path-encoder "checkpoints/weights-CNNFCGR_Levels.keras" \
    --path-index "index/panspace.index" \
    --outdir "results/" \
    --cores 8
```

**With fast FCGR generation** (requires [FCGR extension](https://github.com/pg-space/fcgr)):
```bash
panspace query-smk \
    --dir-sequences "assemblies/" \
    --path-encoder "checkpoints/weights-CNNFCGR_Levels.keras" \
    --path-index "index/panspace.index" \
    --fast-version \
    --outdir "results/"
```

**Using Snakemake directly**:

1. Configure `scripts/config_query.yml`:
   ```yaml
   dir_sequences: "assemblies/"
   outdir: "results/"
   device: "cpu"  # or "gpu"
   path_encoder: "checkpoints/weights-CNNFCGR_Levels.keras"
   path_index: "index/panspace.index"
   kmer: 8
   ```

2. Run pipeline:
   ```bash
   snakemake -s scripts/query.smk --cores 8 --use-conda
   ```

---

### Option 2: Training Your Own Models

Create custom encoders and indexes for your specific dataset.

#### Step 1: Generate FCGRs

**Option A: From FASTA files (single file)**
```bash
panspace fcgr from-fasta \
    --path-fasta assembly.fa \
    --kmer 8 \
    --path-save fcgr.npy
```

**Option B: From k-mer counts**
```bash
# First count k-mers with KMC3
kmc -k8 -fm assembly.fa assembly.kmc tmp/

# Then create FCGR
panspace fcgr from-kmer-counts \
    --kmer 8 \
    --path-kmer-counts assembly.kmc \
    --path-save fcgr.npy
```

**Option C: Batch processing with Snakemake** (recommended for large datasets)

1. Configure `scripts/config_fcgr.yml`
2. Run:
   ```bash
   snakemake -s scripts/create_fcgr.smk --cores 8 --use-conda
   ```

For faster processing with [FCGR extension](https://github.com/pg-space/fcgr):
```bash
snakemake -s scripts/create_fcgr_fast.smk --cores 8 --use-conda \
    --config fcgr_bin=/path/to/fcgr
```

---

#### Step 2: Prepare Dataset

Split your data into train/validation/test sets:

```bash
panspace trainer split-dataset \
    --data-dir fcgr_data/ \
    --output-dir splits/ \
    --train-ratio 0.7 \
    --val-ratio 0.15 \
    --test-ratio 0.15
```

**Output structure:**
```
splits/
├── train/
├── val/
└── test/
```

---

#### Step 3: Train Encoder

Choose a training strategy based on your data:

##### Option A: Metric Learning with Labels (Recommended)

**Triplet Loss** (best for large datasets):
```bash
panspace trainer metric-learning \
    --train-dir splits/train/ \
    --val-dir splits/val/ \
    --kmer 8 \
    --embedding-dim 256 \
    --batch-size 32 \
    --epochs 100 \
    --learning-rate 1e-4 \
    --output-dir models/triplet/
```

**Contrastive Loss** (one-shot learning):
```bash
panspace trainer one-shot \
    --train-dir splits/train/ \
    --val-dir splits/val/ \
    --kmer 8 \
    --embedding-dim 256 \
    --margin 1.0 \
    --epochs 100 \
    --output-dir models/contrastive/
```

Extract the encoder:
```bash
panspace trainer extract-backbone-one-shot \
    --model-path models/contrastive/model.keras \
    --output-path models/contrastive/encoder.keras
```

##### Option B: Unsupervised Learning (No Labels)

**Autoencoder**:
```bash
panspace trainer autoencoder \
    --train-dir splits/train/ \
    --val-dir splits/val/ \
    --kmer 8 \
    --embedding-dim 256 \
    --epochs 100 \
    --output-dir models/autoencoder/
```

Extract the encoder:
```bash
panspace trainer split-autoencoder \
    --model-path models/autoencoder/autoencoder.keras \
    --output-encoder models/autoencoder/encoder.keras \
    --output-decoder models/autoencoder/decoder.keras
```

---

#### Step 4: Create Index

Build a FAISS index from your trained encoder:

```bash
panspace index create \
    --data-dir fcgr_data/ \
    --encoder-path models/triplet/encoder.keras \
    --output-index index/panspace.index \
    --output-metadata index/metadata.json \
```

**Index types:**
- `Flat`: Exact search, slower but accurate
- `IVF1024,Flat`: Inverted file index, faster with slight approximation
- `HNSW32`: Hierarchical graph, very fast

---

#### Step 5: Query Your Index

**From FCGR files**:
```bash
panspace index query \
    --query-fcgr query.npy \
    --encoder-path models/triplet/encoder.keras \
    --index-path index/panspace.index \
    --metadata-path index/metadata.json \
    --n-neighbors 10
```

**From FASTA files** (use Snakemake wrapper shown above)

---

## CLI Reference

### Main Commands

```bash
panspace --help
```

```
╭─ Commands ──────────────────────────────────────────────────────────────╮
│ app              Run streamlit app for interactive queries              │
│ fcgr             Create FCGRs from fasta files or k-mer counts         │
│ trainer          Train encoders using metric learning or autoencoders   │
│ index            Create and query FAISS indexes                        │
│ query-smk        Run Snakemake query pipeline                          │
│ data-curation    Find outliers and mislabeled samples                  │
│ stats-assembly   Compute assembly statistics (N50, contigs, etc.)      │
│ utils            Extract info from logs and text files                 │
│ what-to-do       Step-by-step guide for new users                      │
│ docs             Open documentation webpage                             │
╰─────────────────────────────────────────────────────────────────────────╯
```

### FCGR Commands

```bash
# Create FCGR from FASTA
panspace fcgr from-fasta \
    --path-fasta <file.fa> \
    --kmer <k> \
    --path-save <output.npy>

# Create FCGR from k-mer counts
panspace fcgr from-kmer-counts \
    --kmer <k> \
    --path-kmer-counts <kmc_output> \
    --path-save <output.npy>

# Save FCGR as image
panspace fcgr to-image \
    --path-fcgr <input.npy> \
    --path-save <output.png>
```

### Training Commands

```bash
# Split dataset
panspace trainer split-dataset \
    --data-dir <dir> \
    --output-dir <output> \
    [--train-ratio 0.7] [--val-ratio 0.15]

# Metric learning (Triplet loss)
panspace trainer metric-learning \
    --train-dir <train/> \
    --val-dir <val/> \
    --kmer <k> \
    --embedding-dim <dim> \
    [--batch-size 32] [--epochs 100]

# One-shot learning (Contrastive loss)
panspace trainer one-shot \
    --train-dir <train/> \
    --val-dir <val/> \
    --kmer <k> \
    --embedding-dim <dim> \
    [--margin 1.0] [--epochs 100]

# Autoencoder (Unsupervised)
panspace trainer autoencoder \
    --train-dir <train/> \
    --val-dir <val/> \
    --kmer <k> \
    --embedding-dim <dim> \
    [--epochs 100]

# Extract encoder from trained models
panspace trainer extract-backbone-one-shot \
    --model-path <model.keras> \
    --output-path <encoder.keras>

panspace trainer split-autoencoder \
    --model-path <autoencoder.keras> \
    --output-encoder <encoder.keras> \
    --output-decoder <decoder.keras>
```

### Index Commands

```bash
# Create index
panspace index create \
    --data-dir <fcgr_data/> \
    --encoder-path <encoder.keras> \
    --output-index <panspace.index> \
    --output-metadata <metadata.json> \

# Query index
panspace index query \
    --query-fcgr <query.npy> \
    --encoder-path <encoder.keras> \
    --index-path <panspace.index> \
    --metadata-path <metadata.json> \
    [--n-neighbors 10]

# Test index performance
panspace index test \
    --test-dir <test/> \
    --encoder-path <encoder.keras> \
    --index-path <panspace.index> \
    --metadata-path <metadata.json>
```

### Query Pipeline

```bash
# Query with Snakemake wrapper
panspace query-smk \
    --dir-sequences <assemblies/> \
    --path-encoder <encoder.keras> \
    --path-index <panspace.index> \
    [--outdir results/] \
    [--cores 8] \
    [--fast-version]  # requires FCGR extension

# See all options
panspace query-smk --help
```

---

## Advanced Usage

### Custom FCGR Generation

For very large datasets (e.g., AllTheBacteria), use specialized k-mer counters:

**With KMC3**:
```bash
# Count k-mers
kmc -k8 -m64 -t8 -fm assembly.fa output tmp/

# Create FCGR
panspace fcgr from-kmer-counts \
    --kmer 8 \
    --path-kmer-counts output \
    --path-save fcgr.npy
```

**With FCGR Extension** (faster):
```bash
# Install from https://github.com/pg-space/fcgr
fcgr -k 8 -i assembly.fa -o fcgr.npy
```

### Batch Processing Examples

**Process AllTheBacteria dataset**:
```bash
# See scripts/allthebacteria_*.smk
snakemake -s scripts/allthebacteria_fcgr.smk \
    --config input_dir=/path/to/allthebacteria \
    --cores 32 \
    --use-conda
```

### Data Curation

Find outliers and potential mislabeling:
```bash
panspace data-curation \
    --embeddings-path embeddings.npy \
    --labels-path labels.json \
    --output-dir curation_results/
```

### Assembly Statistics

Compute N50, contig counts, and more:
```bash
panspace stats-assembly \
    --fasta-path assembly.fa \
    --output stats.json
```

---

## Project Structure

```
panspace/
├── panspace/              # Core Python package
│   ├── cli/              # Command-line interface
│   ├── models/           # TensorFlow models (CNNFCGR)
│   ├── trainers/         # Training logic
│   ├── indexing/         # FAISS index management
│   └── streamlit_app/    # Interactive visualization
├── scripts/              # Snakemake workflows
│   ├── query.smk         # Query pipeline
│   ├── query_fast.smk    # Fast query with FCGR extension
│   ├── create_fcgr.smk   # FCGR generation
│   └── config_*.yml      # Configuration files
├── envs/                 # Conda environments
│   ├── cpu.yml          # CPU version
│   └── gpu.yml          # GPU version
├── tests/               # Unit tests
└── docs/                # Documentation
```

---

## Performance Tips

### Speed Optimization

1. **Use GPU**: 10-100x faster for encoding
   ```bash
   conda activate panspace-gpu
   ```

2. **Use FCGR Extension**: 5-10x faster FCGR generation
   ```bash
   panspace query-smk --fast-version
   ```

3. **Parallel Processing**: Increase cores for Snakemake
   ```bash
   snakemake -s scripts/query.smk --cores 32
   ```

4. **Batch Queries**: Process multiple files at once with Snakemake

### Memory Optimization

- Use appropriate index types for large databases
- Process large datasets in batches
- Configure KMC3 memory limits in `config_*.yml`

---

## Citation

If you use PanSpace in your research, please cite:

```bibtex
@article{cartes2025panspace,
  title={PanSpace: Fast and Scalable Indexing for Massive Bacterial Databases},
  author={Cartes, Jorge Avila and Ciccolella, Simone and Denti, Luca and Dandinasivara, Raghuram and Vedova, Gianluca Della and Bonizzoni, Paola and Sch{\"o}nhuth, Alexander},
  journal={bioRxiv},
  pages={2025--03},
  year={2025},
  publisher={Cold Spring Harbor Laboratory}
}
```

---

## Troubleshooting

### Common Issues

**TensorFlow installation problems:**
```bash
# Ensure correct Python version (3.9-3.10)
python --version

# Reinstall with conda
conda install -c conda-forge tensorflow
```

**FCGR extension not found:**
```bash
# Install from source
git clone https://github.com/pg-space/fcgr
cd fcgr && make install
```

**Snakemake fails:**
```bash
# Clear cache and retry
snakemake --unlock
rm -rf .snakemake/
snakemake -s scripts/query.smk --use-conda --cores 8
```

---

## Related Tools

- **[AllTheBacteria](https://allthebacteria.org)**: Comprehensive bacterial genome database
- **[KMC3](https://github.com/refresh-bio/KMC)**: Fast k-mer counting
- **[FCGR Extension](https://github.com/pg-space/fcgr)**: Optimized FCGR generation
- **[ComplexCGR](https://github.com/AlgoLab/complexCGR)**: Python FCGR library
- **[FAISS](https://github.com/facebookresearch/faiss)**: Efficient similarity search

---

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## Support

- 📧 **Email**: jorgeavilacartes@gmail.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/pg-space/panspace/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/pg-space/panspace/discussions)
<!-- - 📖 **Documentation**: [docs/](docs/) -->

---

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Built with TensorFlow and FAISS
- FCGR generation powered by KMC3 and custom extensions
- Inspired by deep metric learning approaches
<!-- - Funded by [Your funding sources] -->

---

## Author

**PanSpace** is developed and maintained by [Jorge Avila Cartes](https://github.com/jorgeavilacartes)

<div align="center">
    <p>⭐ Star us on GitHub if PanSpace helps your research!</p>
</div>
