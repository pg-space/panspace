from enum import Enum
import typer
from typing_extensions import Annotated
from typing import Optional
from pathlib import Path

import json
import logging 
logger = logging.getLogger()
logger.setLevel(logging.INFO)

from rich.progress import track
from rich import print 
from rich.console import Console

console=Console()
app = typer.Typer(rich_markup_mode="rich",
    help="Create FCGRs from fasta file or from txt file with kmers and counts.")

@app.command("fcgr",help="Create the Frequency matrix of CGR (FCGR) from k-mer counts.")
def create_fcgr_kmc(path_kmer_counts: Annotated[Path, typer.Option("--path-kmer-counts","-pk",mode="r", help="path to .txt file with kmer counts.")],
                path_save: Annotated[Path, typer.Option("--path-save","-ps",mode="w", help="path to .npy file to store FCGR.")],
                kmer: Annotated[int, typer.Option("--kmer","-k",min=1)] = 6) -> None:

    from .fcgr_mods.fcgr_from_kmc import FCGRKmc
    import numpy as np
    from pathlib import Path

    fcgr = FCGRKmc(kmer)
    m = fcgr(path_kmer_counts)
    Path(path_save).parent.mkdir(exist_ok=True, parents=True)
    np.save(path_save, m)

@app.command("fcgr-fasta",help="Create the Frequency matrix of CGR (FCGR) from a fasta file.")
def create_fcgr_fasta(path_fasta: Annotated[Path, typer.Option("--path-fasta","-pf",mode="r", help="path to .fa file with assembly.")],
                path_save: Annotated[Path, typer.Option("--path-save","-ps",mode="w", help="path to .npy file to store FCGR.")],
                kmer: Annotated[int, typer.Option("--kmer","-k",min=1)] = 6) -> None:

    from complexcgr import FCGR
    import numpy as np
    from pathlib import Path
    from Bio import SeqIO

    fcgr = FCGR(kmer)
    with open(path_fasta,"r") as fp:
        record = SeqIO.read(fp, format="fasta")
    
    m = fcgr(sequence=record.seq)

    Path(path_save).parent.mkdir(exist_ok=True, parents=True)
    np.save(path_save, m)

@app.command("plot-outliers", help="Create image in jpg format for a list of FCGR")
def plot_outliers(path_outliers:  Annotated[Path, typer.Option("--path-outliers","-po",mode="r", help="file with list of outliers .csv")],
            # column_path: Annotated[int, typer.Option("--column-path", "-cp", help="column with path to FCGR in .npy format")] = 1,
            # column_label: Annotated[int, typer.Option("--column-label", "-cl", help="column with label in .npy format")] = 2,
            dir_save: Annotated[Path, typer.Option("--dir-save","-s",mode="w", help="path to .jpg file to store FCGR.")]=None,
            kmer: Annotated[int, typer.Option("--kmer","-k",min=1)] = 6) -> None:

    import pandas as pd
    import numpy as np
    from complexcgr import FCGR
    # fcgr = FCGR(kmer)
    
    df_outliers = pd.read_csv(path_outliers, sep="\t", index_col=0)

    path_save=Path(dir_save)#.joinpath(f"outliers.jpg")
    path_save.parent.mkdir(exist_ok=True, parents=True)

    display_images(
        list_fcgr=df_outliers.path.tolist(),
        labels=df_outliers.label.tolist(),
        avg_dist=df_outliers.avg_dist.tolist(),
        k=kmer,
        max_images=30,
        path_save=path_save
    )
    


def display_images(
    list_fcgr, labels, avg_dist, k, 
    columns=5, width=25, height=25, max_images=30, 
    label_wrap_length=50, label_font_size=15,
    path_save=None):


    import matplotlib.pyplot as plt
    from PIL.Image import Image as PilImage
    import textwrap, os
    import numpy as np
    from complexcgr import FCGR


    if not list_fcgr:
        print("No images to display.")
        return 

    if len(list_fcgr) > max_images:
        print(f"Showing {max_images} images of {len(list_fcgr)}:")
        list_fcgr=list_fcgr[0:max_images]
        labels = labels[0:max_images]
        avg_dist = avg_dist[0:max_images]

    # height = max(height, int(len(images)/columns) * height)
    fig = plt.figure(figsize=(width, height))
    fig.subplots_adjust(hspace=.3)

    i = 0 
    for path, lb, ad in zip(list_fcgr,labels, avg_dist):

        plt.subplot(int(len(list_fcgr) / columns + 1), columns, i + 1)
        m=np.load(path)
        plt.imshow(FCGR(k).array2img(m),"gray")

        # if hasattr(image, 'filename'):
        title=lb+"|"+ str(round(ad,4)) # label + average distance
        # title=textwrap.wrap(title, label_wrap_length)
        # title="\n".join(title)
        plt.title(title, fontsize=label_font_size)

        i+=1
    plt.tight_layout()
    
    if path_save:
        Path(path_save).parent.mkdir(exist_ok=True, parents=True)
        fig.savefig(path_save, dpi=300)
    plt.close(fig)