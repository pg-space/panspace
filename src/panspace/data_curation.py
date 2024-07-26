import typer 
from typing_extensions import Annotated
from pathlib import Path 
from typing import List

from rich.progress import track
from rich import print 
from rich.console import Console

console=Console()
app = typer.Typer(help="Find outliers and mislabaled samples.")

@app.command("ood", help="Detect outliers from embeddings.")
def outlier_detection(
        path_index: Annotated[Path, typer.Option("--path-index","-pi",help="path to panspace.index")],
        path_train_embeddings: Annotated[Path, typer.Option("--path-train-embeddings", help="path to .npy file with embeddings in the index.")],
        # path_train_metadata: Annotated[Path, typer.Option("--path-train-metadata", help="path to .txt file with metadata.")],
        path_test_embeddings: Annotated[Path, typer.Option("--path-test-embeddings", help="path to .npy file with embeddings to be analyzed as ood.")],
        path_test_metadata: Annotated[Path, typer.Option("--path-test-metadata", help="path to .txt file with metadata (path to source files and label).")],
        outdir: Annotated[Path, typer.Option("--outdir","-o", help="output directory to save results")],
        neighbors: Annotated[int, typer.Option("--neighbors","-n", min=1, help="number of neighbors to compute average distance to n nearest neighbors.")] = 10,
        percentile: Annotated[float, typer.Option("--percentile","-p", help="percentil of the average distance to n nearest neighbors in the index")] = 0.95 ,
    ):

    import pandas as pd
    import numpy as np 
    import faiss 
    import json

    outdir = Path(outdir)
    outdir.mkdir(exist_ok=True, parents=True)

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

    console.print(f":dna: computing {percentile}th percentil of average distances")  
    threshold_dist = np.percentile(avg_dist, percentile)

    # query index with test set
    D_query, I_query = index.search(test_emb, k=neighbors)
    avg_dist_query = D_query.mean(axis=1)
    np.save(outdir.joinpath(f"train_avg_dist.npy"), avg_dist)

    # df_train = pd.read_csv(path_train_metadata, sep="\t")
    df_test = pd.read_csv(path_test_metadata, sep="\t", header=None)#[:100]
    console.print(df_test.shape)
    
    df_test.columns = ["path","label"]
    console.print(len(avg_dist_query))
    df_test["avg_dist"] = avg_dist_query
    np.save(outdir.joinpath(f"test_avg_dist.py"), avg_dist_query)

    # save results, return flagged outliers
    outdir = Path(outdir)
    outdir.mkdir(exist_ok=True, parents=True)
    path_outliers = outdir.joinpath(f"outliers_avg_dist_percentile.csv")
    df_test.query(f"avg_dist > {threshold_dist}").sort_values(by="avg_dist",ascending=False).to_csv(path_outliers, sep="\t")

    with open(outdir.joinpath("percentile_threshold.json"),"w") as fp: 
        json.dump({
            "threshold":threshold_dist,
            "percentile":percentile,
        }, fp, indent=1)

@app.command("pred-scores", help="predicted scores from embeddings using Logistic Regression")
def preds_confident_learning(
    # paths
    path_train_embeddings: Annotated[Path, typer.Option("--path-train-embeddings", help="path to .npy file with embeddings.")],
    path_train_labels: Annotated[Path, typer.Option("--path-train-labels", help="path to txt file with path and labels.")],
    path_test_embeddings: Annotated[Path, typer.Option("--path-test-embeddings", help="path to .npy file with embeddings.")],
    path_test_labels: Annotated[Path, typer.Option("--path-test-labels", help="path to txt file with path and labels.")],
    outdir: Annotated[Path, typer.Option("--outdir","-o", help="output directory to save results")],
    order_labels: Annotated[Path, typer.Option("--order-labels","-ol", help="txt file with all unique labels, one label per row")] = None,
    ):
    
    import json
    import numpy as np 
    import pandas as pd 
    import tensorflow as tf

    from cleanlab.filter import find_label_issues
    from sklearn.linear_model import LogisticRegression

    from .dnn.callbacks import CSVTimeHistory
    
    outdir = Path(outdir)
    outdir.mkdir(exist_ok=True, parents=True)

    X_train = np.load(path_train_embeddings) 
    labels_train = []
    with open(path_train_labels) as fp:
        for line in fp.readlines():
            label = line.strip().split("\t")[-1]
            labels_train.append(label)

    labels_test = []
    with open(path_test_labels) as fp:
        for line in fp.readlines():
            label = line.strip().split("\t")[-1]
            labels_test.append(label)

    if order_labels is None:
        unique_labels = list(set(labels_train).union(labels_test))
        unique_labels.sort()
        dict_labels = {label: idx for idx, label in enumerate(unique_labels)}
    else:
        dict_labels = {label: idx for idx, label in enumerate(unique_labels)}
    
    y_train = np.array([dict_labels[label] for label in labels_train])
    

    # # # #
    # clf = LogisticRegression(random_state=42).fit(X_train, y_train)
    # Model parameters
    num_classes = len(unique_labels)
    input_shape = (X_train.shape[1],)

    model = tf.keras.Sequential(
        [
            tf.keras.layers.Input(shape=input_shape),
            tf.keras.layers.Dense(64, activation="relu"),
            tf.keras.layers.Dense(32, activation="relu"),
            tf.keras.layers.Dense(num_classes, activation="softmax"),
        ]
    )

    model.compile(
        loss=tf.keras.losses.SparseCategoricalCrossentropy(),
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        metrics=[
            tf.keras.metrics.SparseCategoricalAccuracy(name="acc"),
        ],
    )

    Path(f"{outdir}/checkpoints").mkdir(exist_ok=True, parents=True)
    cb_checkpoint = tf.keras.callbacks.ModelCheckpoint(
        filepath=f'{outdir}/checkpoints/weights-mlp.keras',
        monitor='val_loss',
        mode='min',
        save_best_only=True,
        verbose=1
    )

    cb_reducelr = tf.keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        mode='min',
        factor=0.1,
        patience=20,
        verbose=1,
        min_lr=0.00001
    )


    # stop training if
    cb_earlystop = tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',
        mode='min',
        min_delta=0.001,
        patience=50,
        verbose=1
    )
    # save history of training
    cb_csvlogger = tf.keras.callbacks.CSVLogger(
        filename=f'{outdir}/training_log.csv',
        separator='\t',
        append=False
    )

    # save time by epoch
    cb_csvtime = CSVTimeHistory(
        filename=f'{outdir}/time_log.csv',
        separator='\t',
        append=False
    )

    callbacks = [
        cb_checkpoint,
        cb_reducelr,
        cb_earlystop,
        cb_csvlogger,
        cb_csvtime,
    ]

    model.fit(
        X_train,
        y_train,
        batch_size=256,
        epochs=200,
        validation_split=0.2,
        callbacks=callbacks,
    )

    # get prediction on test set
    X_test = np.load(path_test_embeddings) 
    y_test = np.array([dict_labels[label] for label in labels_test])
    pred_probs = model.predict(X_test)
    np.save(file=outdir.joinpath("pred_probs.npy"), arr=pred_probs)
    np.save(file=outdir.joinpath("labels.npy"), arr=y_test)


@app.command("utils-join-npy")
def join_npy(
    files: List[Path], 
    path_save: Annotated[Path, typer.Option("--path-save", "-o", help="output file")]="output-test.npy"
    ):

    import numpy as np
    import pandas as pd
    from pathlib import Path

    path_save = Path(path_save)
    path_save.parent.mkdir(exist_ok=True, parents=True)

    array = np.concatenate([ np.load(path) for path in files ], axis=0)
    console.print(array.shape)
    np.save(file=path_save, arr=array)


@app.command("utils-join-df")
def join_df(
    files: List[Path],
    path_save: Annotated[Path, typer.Option("--path-save", "-o", help="output file")]="output-test.csv"
    ):

    import pandas as pd
    from pathlib import Path

    path_save = Path(path_save)
    path_save.parent.mkdir(exist_ok=True, parents=True)

    df = pd.concat([ pd.read_csv(path, index_col=False) for path in files ], axis=0)
    console.print(df.shape)
    df.to_csv(path_save, index=False)


@app.command("confident-learning", help="Identify mislabeled data from predicted scores")
def confident_learning(
    pred_scores: Annotated[Path, typer.Option("--path-pred-scores", help="path to npy with predicted scores.")]=None,
    labels: Annotated[Path, typer.Option("--path-labels", help="path to npy file with labels (numeric).")]=None,
    outdir: Annotated[Path, typer.Option("--outdir", "-o", help="output directory to save results with potential mislabeled assemblies")]="output-test"
    ):

    import numpy as np
    import pandas as pd
    from pathlib import Path
    
    from cleanlab.filter import find_label_issues

    outdir = Path(outdir)
    outdir.mkdir(exist_ok=True, parents=True)

    label_issues = find_label_issues(
        labels=np.load(labels),
        pred_probs= np.load(pred_scores),
    )

    np.save(file=outdir.joinpath("label_issues.npy"), arr=label_issues)

