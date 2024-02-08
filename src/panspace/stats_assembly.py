import typer 
from typing import Union
from typing_extensions import Annotated
from pathlib import Path 


from rich.progress import track
from rich import print 
from rich.console import Console

console=Console()
app = typer.Typer(help="N50, number of contigs, avg length, total length.")

EXTENSIONS = ["fa","fasta","fna"]

@app.command("compute")
def stats_fasta(
                fasta: Annotated[Path, typer.Option("--fasta","-f",help="file or directory, extensions recognized are: .fna .fasta .fa")],
                outdir: Annotated[Path, typer.Option("--outdir","-o",help="path to a .csv file")]
                ) -> None:

    import numpy as np 
    import pandas as pd
    from Bio import SeqIO
    from collections import defaultdict
     
    list_files = []
    if Path(fasta).is_file():
        list_files.append(fasta)
    else:
        for ext in EXTENSIONS:
            list_files.extend(
                list(Path(fasta).rglob(f"*{ext}"))
            )
        
    n_files = len(list_files)
    list_stats = []
    for file in track(list_files, total=n_files):   
        n_seqs = 0
        lens = []
        stats_file = dict()
        for record in SeqIO.parse(file, "fasta"):
            n_seqs +=1
            lens.append(len(record.seq))    
            
        stats_file["path"] = file
        stats_file["n_seqs"] = n_seqs
        stats_file["tot_len"] = np.sum(lens)  
        stats_file["avg_len"] = np.mean(lens)
        stats_file["std_len"] = np.std(lens)
        
        stats_file["N50"] = calculate_N50(lens)
        list_stats.append(stats_file)

    pd.DataFrame(list_stats).to_csv(outdir, sep="\t")

def calculate_N50(list_of_lengths):
    """Calculate N50 for a sequence of numbers.
 
    Args:
        list_of_lengths (list): List of numbers.
 
    Returns:
        float: N50 value.
 
    """
    tmp = []
    for tmp_number in set(list_of_lengths):
            tmp += [tmp_number] * list_of_lengths.count(tmp_number) * tmp_number
    tmp.sort()
 
    if (len(tmp) % 2) == 0:
        median = (tmp[int(len(tmp) / 2) - 1] + tmp[int(len(tmp) / 2)]) / 2
    else:
        median = tmp[int(len(tmp) / 2)]
 
    return median