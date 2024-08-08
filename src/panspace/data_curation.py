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


@app.command("utils-ani")
def utils_ani(path_cv, 
              path_most_abundant,
              path_reference_by_accession,
              path_metadata_references,
              ):
    
    from pathlib import Path
    import numpy as np
    import pandas as pd

    from collections import defaultdict

    path_cv = Path(path_cv)

    kfold_test = list( path_cv.glob("test*") )
    kfold_test.sort()

    paths_fcgr = []
    labels = []

    for kfold in kfold_test:

        with open(kfold) as fp:
            for line in fp.readlines():
                path_fcgr, label = line.strip().split("\t")

                # if path_fcgr not in df_outliers.path:
                labels.append(label)
                paths_fcgr.append(path_fcgr)

    df_labels = pd.DataFrame({
        "path_fcgr": paths_fcgr,
        "label": labels
    })
    df_labels["sample_id"] = df_labels.path_fcgr.apply(lambda s: Path(s).stem)
    df_labels["tarfile"] = df_labels.path_fcgr.apply(lambda s: Path(s).parent.stem)
    df_labels.head()

    # get mapping integer label -> species label
    unique_labels = list(df_labels.label.unique())
    unique_labels.sort()
    dict_int2label = {idx: label for idx, label in enumerate(unique_labels)}

    # label issues
    path_cf = path_cv.joinpath("confident-learning")
    int_labels = np.load( path_cf.joinpath("labels.npy") )  # integer labels
    labels = [dict_int2label[int(x)] for x in int_labels]   # species name labels
    len(labels)

    pred_probs = np.load( path_cf.joinpath("pred_probs.npy") )
    preds = [dict_int2label[int(x)] for x in pred_probs.argmax(axis=1) ]
    df_labels["pred"] = preds
    len(preds)

    label_issues = np.load( path_cf.joinpath("label_issues.npy") ) 
    df_labels_issues = df_labels.loc[label_issues].copy()
    df_labels_issues

    # Compare against most abundant species
    df_most_abundant = pd.read_csv(path_most_abundant,sep="\t")
    df_most_abundant.rename({
        "V2": "species1",
        "V3": "abundancy1",
        "V4": "species2",
        "V5": "abundancy2",
        "V6": "species3",
        "V7": "abundancy3",
    }, inplace=True, axis=1)

    for feat in ["species1","species2","species3"]:
        df_most_abundant[feat] = df_most_abundant[feat].apply(lambda x: str(x).lower().strip().replace(" ","_"))

    issues = pd.merge(left=df_labels_issues, right=df_most_abundant ,how="left", on="sample_id")

    path_references = pd.read_csv(path_reference_by_accession, sep=" ", header=None)
    path_references.rename({0:"Assembly Accession", 1:"path"}, inplace=True, axis=1)
    metadata_references = pd.read_csv(path_metadata_references, sep="\t")
    df_references = pd.merge(metadata_references, path_references, on="Assembly Accession")
    
    label2refpath = {l:p for l,p in zip(df_references.label, df_references.path)}

    # For each sequence with label issue, create a txt file with 4 rows:
    # - path to reference of the prediction
    # - path to reference of the most abundant species (ground truth label)
    # - path to reference of the second most abundant species
    # - path to reference of the third most abundant species
    path_save = path_cv.joinpath("confident-learning/lists-ANI")
    path_save.mkdir(exist_ok=True, parents=True)

    fastas_by_tarfile = defaultdict(list)
    for d in issues.to_dict("records"):

        ref_paths=[]
        for l in ["pred","species1"]:#,"species2","species3"]:
            path = label2refpath.get(d[l])
            if path:
                ref_paths.append(path)

        if len(ref_paths)>1:
            with open(path_save.joinpath(f"{d['sample_id']}.txt"), "w") as fp:
                for path in ref_paths:
                    fp.write(path)
                    fp.write("\n")

            tarfile=d["tarfile"]
            sample_id=d["sample_id"]
            fastas_by_tarfile[tarfile].append(f"{tarfile}/{sample_id}.fa")
            

    # # fastas_by_tarfile = defaultdict(list)
    # for tarfile, sample_id in zip(issues.tarfile, issues.sample_id):
    #     fastas_by_tarfile[tarfile].append(
    #                                     f"{tarfile}/{sample_id}.fa"
    #                                     )

    path_save = path_cv.joinpath("confident-learning/lists-by-tar")
    path_save.mkdir(exist_ok=True, parents=True)

    for tarfile, list_files in fastas_by_tarfile.items():
        
        with open(path_save.joinpath(f"{tarfile}.txt"), "w") as fp:
            
            for l in list_files:
                fp.write(l)
                fp.write("\n")

    issues.to_csv(path_cv.joinpath("confident-learning/metadata_issues.tsv"), sep="\t")

@app.command("consolidate-ani")
def consolidate_ani(path_cv,
                    path_reference_by_accession,
                    path_metadata_references):

    from pathlib import Path
    import pandas as pd

    not_empty=[]
    for path in Path(path_cv).joinpath("confident-learning/ani-results").glob("*txt"):
        
        with open(path,"r") as fp:
            x=fp.read()

        if x:
            not_empty.append(pd.read_csv(path,sep="\t", header=None))

    df = pd.concat(not_empty, axis=0, ignore_index=True)
    df.rename({0:"path_ebi",
           1:"path_ref",
           2:"ani",
           }, axis=1, inplace=True)


    path_references = pd.read_csv(path_reference_by_accession, sep=" ", header=None)
    path_references.rename({0:"Assembly Accession", 1:"path"}, inplace=True, axis=1)
    metadata_references = pd.read_csv(path_metadata_references, sep="\t")
    df_references = pd.merge(metadata_references, path_references, on="Assembly Accession")

    # create dictionary to map label to the reference path
    label2refpath = {l:p for l,p in zip(df_references.label, df_references.path)}
    refpath2label = {p:l for l,p in zip(df_references.label, df_references.path)}

    metadata_issues = pd.read_csv(Path(path_cv).joinpath("confident-learning/metadata_issues.tsv"), sep="\t")

    sampleid2label = {sid: l for sid, l in zip(metadata_issues.sample_id, metadata_issues.label)}

    df["label_ref"] = df["path_ref"].apply(lambda p: refpath2label[p])
    df["sample_id"] =df["path_ebi"].apply(lambda p: Path(p).stem)
    df["label_ebi"] =df["sample_id"].apply(lambda sid: sampleid2label[sid])

    df.to_csv(Path(path_cv).joinpath("confident-learning/ani.tsv"),sep="\t")