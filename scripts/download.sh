# !/bin/bash

DIRSAVE=dataset
BASEPATH=https://zenodo.org/records/4602622/files


# 1. download _md5.txt with names of files
wget $BASEPATH/_md5.txt

mkdir -p $DIRSAVE
cut _md5.txt -d" " -f3 | head -n 3 | \
while read f; \
do wget $BASEPATH/$f -O $DIRSAVE/$f;\
done