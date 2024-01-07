import typer 
from typing_extensions import Annotated
from pathlib import Path 

from rich.progress import track
from rich import print 
from rich.console import Console

console=Console()
app = typer.Typer(help="Create index")

@app.command("create",help="Create a faiss Index with the embeddings produced by the Encoder")
def create_index(
        path_experiment: Annotated[Path, typer.Option("--path-experiment","-p", help="path to experiment")],
        latent_dim: Annotated[int, typer.Option("--latent-dim","-d", help="number of dimension embeddings")]
        ):
    import json
    import faiss
    import numpy as np
    import tensorflow as tf

    from pathlib import Path
    from .dnn.loaders.VARdataloader import DataLoaderVAR as DataLoader
        
    PATH_EXP=path_experiment
    LATENT_DIM=latent_dim
    PATH_INDEX=Path(PATH_EXP).joinpath("faiss-embeddings/bacterial.index")
    PATH_INDEX.parent.mkdir(exist_ok=True, parents=True)

    # 1. load encoder
    encoder =tf.keras.models.load_model(f"{PATH_EXP}/models/encoder.keras")

    # 2. load dataset to add in the index (train+val)
    with open(f"{PATH_EXP}/split-train-val-test.json","r") as fp:
        datasets = json.load(fp)

    list_train = datasets["id_labels"]["train"]
    list_val   = datasets["id_labels"]["val"]
    index_paths = list_train + list_val

    # 3. create embeddings
    # preprocessing of each FCGR to feed the model 
    preprocessing = lambda x: x / x.max() 

    # compute embeddings
    index_data = DataLoader(
        list_paths=index_paths,
        batch_size=10,
        shuffle=False,
        preprocessing=preprocessing,
        inference_mode=True
    )

    # embeddings train+val
    embeddings = []
    for data in track(iter(index_data), description="Generating embeddings..."):
        encoded_imgs = encoder(data).numpy()
        embeddings.append(encoded_imgs)

    all_emb = np.concatenate(embeddings, axis=0)

    path_emb = Path(f"{PATH_EXP}/faiss-embeddings")
    path_emb.mkdir(exist_ok=True, parents=True)
    np.save(file=path_emb.joinpath("embeddings.npy"), arr=all_emb)
    with open(path_emb.joinpath("id_embeddings.json"), "w") as fp:
        json.dump({j: str(p) for j,p in enumerate(list_train+list_val)}, fp, indent=4)

    # 4. create faiss index
    # build the index
    index = faiss.IndexFlatL2(LATENT_DIM)
    print(index.is_trained)

    # add vectors to the index
    index.add(all_emb)                  
    print(index.ntotal, "vectors in the index (train+val)")

    # 5. save index
    faiss.write_index(index, str(PATH_INDEX))

@app.command("query", help="Query Index with FCGR from other sequences")
def query_index(path_experiment: Annotated[Path, typer.Option("--path-experiment","-p", help="path to experiment")],
                path_fcgr: Annotated[Path, typer.Option("--path-fcgr","-p", help="path to folder with FCGR in .npy format")],
                outdir: Annotated[Path, typer.Option("--outdir","-o", help="directory to save results")],
                neighbors: Annotated[int, typer.Option("--n-neighbors","-n", help="number of closest neighbors to retrieve")] = 10,
                ):
    
    import json
    import tensorflow as tf
    import faiss
    import numpy as np
    import pandas as pd

    from pathlib import Path
    from collections import Counter

    from .dnn.loaders.VARdataloader import DataLoaderVAR as DataLoader

    PATH_EXP=Path(path_experiment)
    PATH_INDEX=PATH_EXP.joinpath("faiss-embeddings/bacterial.index") # path to faiss bacterial.index 
    PATH_ENCODER=PATH_EXP.joinpath("models/encoder.keras") # path to encoder.keras model
    DIR_FCGR=Path(path_fcgr) # path to numpy files
    OUTDIR=Path(outdir)
    OUTDIR.mkdir(exist_ok=True, parents=True)

    list_paths = list(Path(DIR_FCGR).rglob("*.npy"))
    # print(list_paths)
    # 0. load index
    console.print(":dna: Loading Index...")
    index = faiss.read_index(str(PATH_INDEX))
    
    # 1. load encoder
    console.print(":dna: Loading Encoder...")
    encoder =tf.keras.models.load_model(PATH_ENCODER)#f"{PATH_EXP}/models/encoder.keras")

    # 3. create embeddings
    # preprocessing of each FCGR to feed the model 
    preprocessing = lambda x: x / x.max() 

    # create dataset to fed Encoder
    index_data = DataLoader(
        list_paths=list_paths,
        batch_size=10,
        shuffle=False,
        preprocessing=preprocessing,
        inference_mode=True
    )

    # embeddings
    embeddings = []
    for data in track(iter(index_data), description="Creating embeddings from FCGR"):
        encoded_imgs = encoder(data).numpy()
        embeddings.append(encoded_imgs)

    query_emb = np.concatenate(embeddings, axis=0)

    # TODO: load metadata index: for each position of the index, the sample id and the label.
    # (...) return labels
    from collections import namedtuple
    Metadata=namedtuple("Metadata",["sample_id","label"])
    with open(PATH_INDEX.parent.joinpath("id_embeddings.json"),"r") as fp:
        index2metadata = {int(idx): 
                        Metadata(
                            Path(path).stem, 
                            Path(path).parent.stem.split("__")[0]
                            ) 
                            for idx, path in json.load(fp).items()}

    # get labels from idx
    get_label_ = lambda idx: index2metadata.get(idx).label
    get_sample_id_ = lambda idx: index2metadata.get(idx).sample_id
    # vectorized version
    get_label = np.vectorize(get_label_)
    get_sample_id = np.vectorize(get_sample_id_)

    # query the index
    console.print(":dna: Querying index...")
    D,I = index.search(query_emb, neighbors)
    neighbors_labels= get_label(I)
    neighbors_sample_ids = get_sample_id(I)

    df = pd.DataFrame([{"sample_id_query": path.stem,} for path in list_paths])

    for n in range(neighbors):
        df[f"sample_id_{n}"] = neighbors_sample_ids[:,n]
        df[f"label_{n}"] = neighbors_labels[:,n]
        df[f"distance_to_{n}"] = D[:,n]

    # # Save results
    console.print(":dna: Saving results...")
    df.to_csv(Path(OUTDIR).joinpath("predictions-aux.csv"))

    np.save( Path(OUTDIR).joinpath("embeddings.npy") , query_emb )  
    console.print(":dna: Done!")

@app.command("test", help="Test index of an experiment in the classification task")
def test_index(
    path_experiment: Annotated[Path, typer.Option("--path-experiment","-p", help="path to experiment")]
    ):

    import json
    import tensorflow as tf
    import numpy as np
    import pandas as pd

    from collections import Counter
    import faiss
    from pathlib import Path
    from .dnn.loaders.VARdataloader import DataLoaderVAR as DataLoader
        
    PATH_EXP=path_experiment #""
    # LATENT_DIM=args.latent_dim # 100
    PATH_INDEX=Path(PATH_EXP).joinpath("faiss-embeddings/bacterial.index")
    PATH_TEST=Path(PATH_EXP).joinpath("test")
    # 0. load index
    index = faiss.read_index(str(PATH_INDEX))

    # 1. load encoder
    encoder =tf.keras.models.load_model(f"{PATH_EXP}/models/encoder.keras")

    # 2. load dataset to add in the index (train+val)
    with open(f"{PATH_EXP}/split-train-val-test.json","r") as fp:
        datasets = json.load(fp)

    list_test = datasets["id_labels"]["test"]
    list_labels = datasets["labels"]["test"]
    # 3. create embeddings
    # preprocessing of each FCGR to feed the model 
    preprocessing = lambda x: x / x.max() 

    # compute embeddings
    index_data = DataLoader(
        list_paths=list_test,
        batch_size=10,
        shuffle=False,
        preprocessing=preprocessing,
        inference_mode=True
    )

    # embeddings train+val
    embeddings = []
    for data in iter(index_data):
        encoded_imgs = encoder(data).numpy()
        embeddings.append(encoded_imgs)

    query_emb = np.concatenate(embeddings, axis=0)

    path_emb = Path(f"{PATH_EXP}/faiss-embeddings")
    path_emb.mkdir(exist_ok=True, parents=True)
    np.save(file=path_emb.joinpath("query_embeddings.npy"), arr=query_emb)
    with open(path_emb.joinpath("id_query_embeddings.json"), "w") as fp:
        json.dump({j: str(p) for j,p in enumerate(list_test)}, fp, indent=4)

    trainval = datasets["labels"]["train"] + datasets["labels"]["val"]
    trainval_idx = {k:v for k,v in enumerate(trainval)}

    # get labels from idx
    get_label_= lambda idx: trainval_idx.get(idx)
    # vectorize version
    get_label = np.vectorize(get_label_)

    # query the index
    neighbors = 10
    D,I = index.search(query_emb, neighbors)
    neighbors_query = get_label(I)
    ground_truth = list_labels

    def majority_vote(list_neighbors): 
        label, _ = Counter(list_neighbors).most_common(1)[0]
        return label

    consensus_1  = [majority_vote(neighbors_query[j][:1]) for j in range(len(neighbors_query))]
    consensus_3  = [majority_vote(neighbors_query[j][:3]) for j in range(len(neighbors_query))]
    consensus_5  = [majority_vote(neighbors_query[j][:5]) for j in range(len(neighbors_query))]
    consensus_10 = [majority_vote(neighbors_query[j]) for j in range(len(neighbors_query))]

    df = pd.concat([ pd.DataFrame(ground_truth,columns=["GT"]),
                    pd.DataFrame.from_dict({
                        "consensus_1": consensus_1, 
                        "consensus_3": consensus_3, 
                        "consensus_5": consensus_5, 
                        "consensus_10": consensus_10}),
                    pd.DataFrame(neighbors_query)]
                    ,axis=1
                    )
    df.to_csv(PATH_TEST.joinpath("test_index.tsv"),sep="\t")

@app.command("metrics-test", help="Compute metrics for test", deprecated=True)
def test_index(
            path_experiment: Annotated[Path, typer.Option("--path-experiment","-p", help="path to experiment")],
            n_neighbors: Annotated[int, typer.Option("--n-neighbors","-n", min=1, help="path to experiment")],
            ):
    
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

    N_NEIGHBORS=n_neighbors # 3 # 1 3 5 10 
    PATH_EXP=path_experiment

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
