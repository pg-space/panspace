"""
Compute FCGR for all fasta files that are saved in a 
path/to/<name-bacteria>__<group>.tar.xz file
"""
from genericpath import exists
import tarfile
import numpy as np

from tqdm import tqdm
from typing import Callable, Optional
from io import StringIO
from pathlib import Path

from Bio import SeqIO
from complexcgr import FCGR
from rich.progress import track
from concurrent.futures import ThreadPoolExecutor, as_completed

class FCGRFromTar(FCGR):
    
    def __init__(self, k: int, path_save: Optional[str]):
        self.path_save = Path(path_save) if path_save is not None else Path(f"data/fcgr-{k}mer")
        super().__init__(k,)

    def fcgr_from_tar(self, path_tarfile: str, progress: Callable = tqdm): 
        
        path_tarfile = Path(path_tarfile)
        # assume path/to/<name-specie>__<group>.tar.xz file
        name_specie=path_tarfile.stem.split("__")[0]    
        path_fcgr_specie=self.path_save.joinpath(name_specie)
        path_fcgr_specie.mkdir(exist_ok=True, parents=True)
        
        # open tarfile 
        tar = tarfile.open(path_tarfile,"r")

        for name in progress(tar.getnames(), f"Working on {path_tarfile.stem}"):
            # save fcgr 
            path_save = path_fcgr_specie.joinpath(Path(name).stem + ".npy")
            
            if path_save.exists():
                continue

            file = tar.extractfile(name)
            seq  = file.read().decode("utf-8")
            seq_io = StringIO(seq)
            seqbio = next(SeqIO.parse(seq_io,"fasta"))
            m = self.__call__(seqbio.seq)
            np.save(path_save, m)

        return f"{path_tarfile} is done!"

    def fcgr_from_dirtar(self, dirtar: str, max_workers: int):

        tarfiles = list(str(path) for path in  Path(dirtar).rglob("*tar.xz"))

        LENGTH = len(list(tarfiles))  # Number of iterations required to fill pbar
        pbar = tqdm(total=LENGTH, desc='tarfiles')  # Init pbar
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # futures = [executor.submit(self.fcgr_from_tar, path_tarfile) for path_tarfile in tarfiles]
            futures = executor.map(self.fcgr_from_tar, tarfiles)
            for _ in as_completed(futures):
                pbar.update(n=1)  # Increments counter
