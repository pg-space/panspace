# !/bin/bash

DIRSAVE=data/batches
BASEPATH=https://ftp.ebi.ac.uk/pub/databases/AllTheBacteria/Releases/0.2

# 1. Download _md5.txt with names of files
wget $BASEPATH/md5sum.txt

# 2. Download batches
mkdir -p $DIRSAVE

cut md5sum.txt -d" " -f3 | head -n 3 | \
while read f; \
do wget $BASEPATH/$f -O $DIRSAVE/$f;\
done