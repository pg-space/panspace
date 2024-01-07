import typer 
from typing_extensions import Annotated

app = typer.Typer()

@app.command("test")
def main(args):
    
    import json
    import pandas as pd

    from pathlib import Path
    from collections import Counter, namedtuple, defaultdict

    from sklearn.metrics import (
        precision_score, 
        recall_score,
        accuracy_score, 
        balanced_accuracy_score
        )

    N_NEIGHBORS=args.n_neighbors # 3 # 1 3 5 10 
    PATH_EXP=args.path_exp #Path("/data/bacteria/experiments/autoencoders/6mer/26122023-2")

    # load labels for train+val and test
    with open(f"{PATH_EXP}/split-train-val-test.json","r") as fp:
        datasets = json.load(fp)

    # collect info in a dataframe
    InfoLabels = namedtuple("InfoLabels",["label","dataset","count"])
    counts = dict()
    data = []
    for ds in ["train","val","test"]:
        count = Counter(datasets["labels"][ds])
        for specie, count in count.items():
            data.append(
                InfoLabels(specie, ds, count)
            )

    df_infolabels = pd.DataFrame(data)

    # get dict with count for the test set for later evaluation
    counts_test = dict()
    for idx, sp, ds, count in df_infolabels.query("dataset == 'test'").to_records("record"):
        counts_test[sp] = count

    counts_train = defaultdict(int)
    for idx, sp, ds, count in df_infolabels.query("dataset != 'test'").to_records("record"):
        counts_train[sp] += count

    df = pd.read_csv(Path(PATH_EXP).joinpath("test/test_index.tsv"),sep="\t", index_col=0)
    df.head(5)

    classes = df.GT.unique()
    classes = sorted(classes)
    y_true, y_pred = df.GT, df[f"consensus_{N_NEIGHBORS}"]

    accuracy_score(y_true, y_pred), balanced_accuracy_score(y_true, y_pred), len(classes)

    precision = precision_score(y_true, y_pred, average=None, labels=classes)
    recall = recall_score(y_true, y_pred, average=None, labels=classes)

    data_metrics = []
    Metrics = namedtuple("Metrics", ["label","n_queries", "n_index", "precision","recall"])
    for sp, prec, rec in zip(classes, precision, recall):
        n_queries= counts_test[sp]
        n_index = counts_train[sp]
        data_metrics.append(
            Metrics(sp, n_queries, n_index, prec, rec)
        )

    pd.DataFrame(data_metrics).sort_values(by="precision").to_csv(Path(PATH_EXP).joinpath(f"test/precision_recall_consensus_{N_NEIGHBORS}.csv"),sep="\t")


# if __name__ == "__main__":
#     import argparse
#     from rich_argparse import RichHelpFormatter
    
#     ## Parser
#     parser = argparse.ArgumentParser(
#                 description="Metrics Test: query Faiss Index with test set", 
#                 prog="Metrics Query", 
#                 formatter_class=RichHelpFormatter
#                 )
    
#     parser.add_argument("--n-neighbors", dest="n_neighbors", type=int, default=1, required=True, choices=[1,3,5,10],
#                         help="number of neighbors to decide the consensus label to the query sequence"
#                         )
    
#     parser.add_argument("--path-exp", dest="path_exp", type=str, default=None, required=True,
#                         help="path to experiment"
#                         )
                    
#     # parser.add_argument("--latent-dim", help="dimension of the embedding", dest="latent_dim", type=int, required=True,
#     #                     )

#     args = parser.parse_args()

#     main(args)
