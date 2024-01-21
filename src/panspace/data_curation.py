import typer 
from typing_extensions import Annotated
from pathlib import Path 

from rich.progress import track
from rich import print 
from rich.console import Console

console=Console()
app = typer.Typer(help="Find outliers and mislabaled samples.")

@app.command("outliers", help="Detect outliers from embeddings.")
def outlier_detection(
        path_train_embeddings: Annotated[Path, typer.Option("--path-fcgr","-p", help="path to folder with the query FCGR in .npy format, or .txt file with paths in its first column.")],
        path_test_embeddings: Annotated[Path, typer.Option("--path-encoder","-pe", help="path to 'encoder.keras' model")],
        outdir: Annotated[Path, typer.Option("--outdir","-o", help="output directory to save results")]
    ):
    
    import numpy as np 
    from cleanlab.outlier import OutOfDistribution   
    from cleanlab.rank import find_top_issues

    # load embeddings
    train_feature_embeddings = np.load(path_train_embeddings)
    test_feature_embeddings = np.load(path_test_embeddings)
    
    ood = OutOfDistribution()

    # To get outlier scores for train_data using feature matrix train_feature_embeddings
    ood_train_feature_scores = ood.fit_score(features=train_feature_embeddings)

    # To get outlier scores for additional test_data using feature matrix test_feature_embeddings
    ood_test_feature_scores = ood.score(features=test_feature_embeddings)

@app.command("mislabels", help="Identify mislabeled from predicted scores")
def mislabeled_identification():
    pass