import typer 
from typing_extensions import Annotated
from pathlib import Path 

from rich.progress import track
from rich import print 
from rich.console import Console

console=Console()
app = typer.Typer(help="Find outliers and mislabaled samples.")

@app.command("find-outliers", help="Detect outliers from embeddings.")
def outlier_detection(
        path_index: Annotated[Path, typer.Option("--path-index","-pi",help="path to panspace.index")],
        path_train_embeddings: Annotated[Path, typer.Option("--path-train-embeddings", help="path to .npy file with embeddings.")],
        path_train_metadata: Annotated[Path, typer.Option("--path-train-metadata", help="path to .txt file with metadata.")],
        path_test_embeddings: Annotated[Path, typer.Option("--path-test-embeddings", help="path to .npy file with embeddings.")],
        path_test_metadata: Annotated[Path, typer.Option("--path-test-metadata", help="path to .txt file with metadata.")],
        outdir: Annotated[Path, typer.Option("--outdir","-o", help="output directory to save results")],
        neighbors: Annotated[int, typer.Option("--neighbors","-n", min=1, help="number of neighbors to compute average distance to n nearest neighbors.")] = 10,
        threshold: Annotated[float, typer.Option("--threshold","-t", help="percentil of average distance to n nearest neighbors in the index")] = 0.99 ,
    ):

    import pandas as pd
    import numpy as np 
    import faiss 
    import json

    # load embeddings
    train_emb = np.load(path_train_embeddings).astype("float32")#[:1000]
    test_emb = np.load(path_test_embeddings).astype("float32")#[:100]
    
    # load index
    console.print(":dna: loading index")
    index = faiss.read_index(str(path_index))

    # query index with train set to find threshold
    console.print(":dna: querying index to find threshold") 
    D_index, I_index = index.search(train_emb, k=neighbors)
    console.print(f":dna: {len(D_index)}") 
    
    avg_dist = D_index.mean(axis=1)

    console.print(f":dna: computing threshold {threshold}th percentil of average distances")  
    percentile = np.percentile(avg_dist, threshold)

    # query index with test set
    D_query, I_query = index.search(test_emb, k=neighbors)
    avg_dist_query = D_query.mean(axis=1)

    # df_train = pd.read_csv(path_train_metadata, sep="\t")
    df_test = pd.read_csv(path_test_metadata, sep="\t", header=None)#[:100]
    console.print(df_test.shape)
    df_test.columns = ["path","label"]
    console.print(len(avg_dist_query))
    df_test["avg_dist"] = avg_dist_query

    # save results, return flagged outliers
    outdir = Path(outdir)
    outdir.mkdir(exist_ok=True, parents=True)
    path_outliers = outdir.joinpath(f"outliers_avg_dist_percentile.csv")
    df_test.query(f"avg_dist > {percentile}").sort_values(by="avg_dist",ascending=False).to_csv(path_outliers, sep="\t")

    with open(outdir.joinpath("percentile_threshold.json"),"w") as fp: 
        json.dump({
            "threshold":threshold,
            "percentile":percentile,
        }, fp, indent=1)

@app.command("mislabels", help="Identify mislabeled from predicted scores")
def mislabeled_identification():
    pass