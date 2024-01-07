import typer
from typing_extensions import Annotated

app = typer.Typer()

from typing import Union
from .fcgr.fcgr_from_kmc import FCGRKmc
import numpy as np
from pathlib import Path


app = typer.Typer(rich_markup_mode="rich")

@app.command(help="Create the Frequency matrix of CGR (FCGR) from k-mer counts")
def create_fcgr(path_kmer_counts: Annotated[Path, typer.Option("--path-kmer-counts","-pk",mode="r", help="path to .txt file with kmer counts")],
                path_save: Annotated[Path, typer.Option("--path-save","-ps",mode="w", help="path to .npy file to store FCGR")],
                kmer: Annotated[int, typer.Option("--kmer","-k",min=1)] = 6):
    fcgr = FCGRKmc(kmer)
    m = fcgr(path_kmer_counts)
    Path(path_save).parent.mkdir(exist_ok=True, parents=True)
    np.save(path_save, m)