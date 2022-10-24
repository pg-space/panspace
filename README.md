# Embedding bacteria
The goal is to build an embedding space for bacterial sequences and use them as an index of dense vector to perform fast queries using faiss

```bash
python src/fcgr.py --help

USAGE: fcgr [-h] [-k KMER] [--path-fcgr PATH_FCGR] [--path-tarfile PATH_TARFILE] [--dir-tarfiles DIR_TARFILES] [-w WORKERS]

generate FCGR

OPTIONAL ARGUMENTS:
  -h, --help            show this help message and exit
  -k, --kmer KMER       kmer size, the FCGR will be of size (2^kmer,2^kmer). Default 6
  --path-fcgr PATH_FCGR
                        directory where to save fcgr generated. A subfolder for each specie will be created inside. if not provided data/fcgr-<kmer>mer
                        will be created
  --path-tarfile PATH_TARFILE
                        path to tarfile with one or several fasta files
  --dir-tarfiles DIR_TARFILES
                        path to directory with tarfiles, each tarfile should contain one or several fasta files. Used only if --dir-tarfiles is not
                        provided
  -w, --workers WORKERS
                        number of workers to use with ThreadPoolExecutor in case --dir-tarfile is provided.
```