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


@app.command("to-image", help="Save FCGR as image from npy file.")
def fcgr2image(list_npy: Annotated[Path, typer.Option("--list-npy", "-l", mode="r", help="path to .txt file with paths to npy <folder>/<species>/<sampleid>.npy")],
               dir_save: Annotated[Path, typer.Option("--dir-save", "-d", mode="w", help="directory where .jpeg images will be saved")],
               kmer: Annotated[int, typer.Option("--kmer","-k",min=1)] = 6,
               percentile_clip: Annotated[int, typer.Option("--percentile-clip", "-p", min=0, max=100, help="percentile to define upper bound to clip FCGR values")] = 0) -> None:
    
    import numpy as np
    from complexcgr import FCGR
    
    dir_save = Path(dir_save)
    fcgr = FCGR(kmer)
    
    paths = []
    with open(list_npy, "r") as fp:
        for line in fp.readlines():
            paths.append(line.replace("\n","").strip())

    for path_npy in track(paths):
        m = np.load(path_npy)

        if percentile_clip>0: 
            perc = np.percentile(m, percentile_clip)
            m[m > perc] = perc

        sampleid = Path(path_npy).stem
        batch = Path(path_npy).parent
        path_save = dir_save.joinpath(f"{sampleid}.jpeg")
        Path(path_save).parent.mkdir(exist_ok=True,parents=True)
        fcgr.save_img(m, path_save)

@app.command("from-kmer-counts",help="Create the Frequency matrix of CGR (FCGR) from k-mer counts.")
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

@app.command("from-fasta",help="Create the Frequency matrix of CGR (FCGR) from a fasta file.")
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


def jaccard_fcgr(fcgr1, fcgr2) -> float:
    "Jaccard similarity between the k-mer content of two FCGRs (each cell is a k-mer, present if count > 0)"
    import numpy as np

    assert fcgr1.shape == fcgr2.shape, "FCGRs must come from the same k-mer size to be compared"

    present1 = fcgr1 > 0
    present2 = fcgr2 > 0
    union = np.logical_or(present1, present2).sum()
    if union == 0:
        return 0.0
    intersection = np.logical_and(present1, present2).sum()
    return float(intersection) / float(union)


def ani_naive_fcgr(fcgr1, fcgr2) -> float:
    "Naive ANI estimate between two genomes: the Jaccard similarity of their FCGR k-mer content, with no evolutionary-model correction"
    return jaccard_fcgr(fcgr1, fcgr2)


def ani_mash_fcgr(fcgr1, fcgr2, kmer: int) -> float:
    "ANI estimate via the Mash equation: ANI = 1 - D, with Mash distance D = -(1/k) * ln(2J/(1+J))"
    import numpy as np

    jaccard = jaccard_fcgr(fcgr1, fcgr2)
    if jaccard == 0:
        # no shared k-mers: ln(0) is undefined, D diverges -> floor ANI at 0
        return 0.0
    return 1 + (1 / kmer) * np.log(2 * jaccard / (1 + jaccard))


@app.command("ani", help="Compute Average Nucleotide Identity (ANI) between two genomes from their FCGR (.npy files).")
def ani_from_fcgr(
        path_fcgr1: Annotated[Path, typer.Option("--path-fcgr1", "-f1", mode="r", help="path to first genome's FCGR in .npy format.")],
        path_fcgr2: Annotated[Path, typer.Option("--path-fcgr2", "-f2", mode="r", help="path to second genome's FCGR in .npy format.")],
        kmer: Annotated[int, typer.Option("--kmer", "-k", min=1, help="k-mer size used to build both FCGRs")] = 6,
    ) -> None:

    import numpy as np

    fcgr1 = np.load(path_fcgr1)
    fcgr2 = np.load(path_fcgr2)

    jaccard = jaccard_fcgr(fcgr1, fcgr2)
    ani_naive = ani_naive_fcgr(fcgr1, fcgr2)
    ani_mash = ani_mash_fcgr(fcgr1, fcgr2, kmer)

    console.print(f"Jaccard similarity: {jaccard:.6f}")
    console.print(f"ANI (naive, = Jaccard): {ani_naive:.6f}")
    console.print(f"ANI (Mash equation): {ani_mash:.6f}")


# @app.command("plot-outliers", help="Create image in jpg format for a list of FCGR")
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

