import typer 
from typing_extensions import Annotated
from pathlib import Path 

from rich.progress import track
from rich import print 
from rich.console import Console

console=Console()
app = typer.Typer(help="Create and query index. Utilities to test index.")

@app.command("create",help="Create a faiss Index with the embeddings produced by the Encoder.")
def create_index(
        # path_experiment: Annotated[Path, typer.Option("--path-experiment","-p", help="path to experiment with a trained model")],
        files_to_index: Annotated[Path, typer.Option("--files-to-index","-i", help=".txt file where the first column contains a list with paths to FCGRs in .npy format")], 
        col_labels: Annotated[int, typer.Option("--col-labels", "-l", help="column in file_to_index containing the labels")],
        path_encoder: Annotated[Path, typer.Option("--path-encoder","-pe", help="path to 'encoder.keras' model")],
        path_index: Annotated[Path, typer.Option("--path-index", "-pi", help="path to store the index. Eg: path/to/save/panspace.index")],
        latent_dim: Annotated[int, typer.Option("--latent-dim","-d", help="number of dimension in the embeddings space")],
        batch_size: Annotated[int, typer.Option("--batch-size","-b", help="batch size for inference with encoder")] = 32,
        ) -> None:
    import json
    import faiss
    import numpy as np
    import tensorflow as tf

    from pathlib import Path
    from .dnn.loaders.VARdataloader import DataLoaderVAR as DataLoader
        
    # PATH_EXP=path_experiment
    LATENT_DIM=latent_dim
    PATH_INDEX=path_index#Path(PATH_EXP).joinpath("faiss-embeddings/panspace.index")
    PATH_INDEX.parent.mkdir(exist_ok=True, parents=True)

    # 1. load encoder
    console.print(":dna: loading encoder...")
    encoder =tf.keras.models.load_model(path_encoder) # f"{PATH_EXP}/models/encoder.keras"

    # 2. load dataset to add in the index (train+val)
    console.print(":dna: loading list of files to index (train+val)")
    
    # # TODO: change this, load a txt file with path in the first column and metadata in the others, separated by \t
    # with open(f"{PATH_EXP}/split-train-val-test.json","r") as fp:
    #     datasets = json.load(fp)

    # list_train = datasets["id_labels"]["train"]
    # list_val   = datasets["id_labels"]["val"]

    # load paths and labels
    index_paths, index_labels = [],[]

    with open(files_to_index, "r") as fp:
        for line in fp.readlines():
            info = line.replace("\n","").split("\t")
            path = info[0]
            label = info[col_labels]
            index_paths.append(path)
            index_labels.append(label)
            
    # 3. create embeddings
    # preprocessing of each FCGR to feed the model 
    preprocessing = lambda x: x / x.max() 

    # compute embeddings
    index_data = DataLoader(
        list_paths=index_paths,
        batch_size=batch_size,
        shuffle=False,
        preprocessing=preprocessing,
        inference_mode=True
    )

    # embeddings train+val
    embeddings = []
    n_batches = len(index_data)
    for data in track(iter(index_data), description=f"Creating embeddings | total in index = {len(index_paths)}", total = n_batches):
        encoded_imgs = encoder(data).numpy()
        embeddings.append(encoded_imgs)

    all_emb = np.concatenate(embeddings, axis=0)

    path_emb = PATH_INDEX.parent
    # path_emb = Path(f"{PATH_EXP}/faiss-embeddings")
    path_emb.mkdir(exist_ok=True, parents=True)
    np.save(file=path_emb.joinpath("embeddings.npy"), arr=all_emb)
    with open(path_emb.joinpath("id_embeddings.json"), "w") as fp:
        json.dump({j: str(p) for j,p in enumerate(index_paths)}, fp, indent=4)

    # 4. create faiss index
    # build the index
    index = faiss.IndexFlatL2(LATENT_DIM)
    console.print(f":info: index is trained {index.is_trained}")

    # add vectors to the index
    index.add(all_emb)                  
    console.print(f":info: vectors in the index (train+val): {index.ntotal}")

    # 5. save index
    console.print(f":floppy_disk: saving index at {str(PATH_INDEX)}")
    faiss.write_index(index, str(PATH_INDEX))

@app.command("query", help="Query Index with FCGR from other sequences.")
def query_index(
        # path_experiment: Annotated[Path, typer.Option("--path-experiment","-p", help="path to experiment")],
        path_fcgr: Annotated[Path, typer.Option("--path-fcgr","-p", help="path to folder with the query FCGR in .npy format, or .txt file with paths in its first column.")],
        path_encoder: Annotated[Path, typer.Option("--path-encoder","-pe", help="path to 'encoder.keras' model")],
        path_index: Annotated[Path, typer.Option("--path-index", "-pi", help="path to store the index. Eg: path/to/save/panspace.index")],
        outdir: Annotated[Path, typer.Option("--outdir","-o", help="directory to save results")],
        col_labels: Annotated[int, typer.Option("--column-labels","-cl", help="column with albels in <path_fcgr>.txt")] = None,
        neighbors: Annotated[int, typer.Option("--n-neighbors","-n", help="number of closest neighbors to retrieve")] = 10,
        batch_size: Annotated[int, typer.Option("--batch-size","-b", help="batch size for inference with encoder")] = 10,
        ) -> None:
    
    import json
    import tensorflow as tf
    import faiss
    import numpy as np
    import pandas as pd

    from pathlib import Path
    from collections import Counter

    from .dnn.loaders.VARdataloader import DataLoaderVAR as DataLoader

    PATH_INDEX=path_index # path to faiss panspace.index 
    PATH_ENCODER=path_encoder # path to encoder.keras model

    assert PATH_INDEX.is_file() , f"index not found, file {str(PATH_INDEX)} does not exist"
    assert PATH_ENCODER.is_file() , f"encoder not found, file {str(PATH_ENCODER)} does not exist"
    
    PATH_FCGR=Path(path_fcgr) # path to numpy files
    OUTDIR=Path(outdir)
    OUTDIR.mkdir(exist_ok=True, parents=True)

    if Path(PATH_FCGR).is_dir():
        list_paths = list(Path(PATH_FCGR).rglob("*.npy"))
    else: 
        list_paths = []
        labels_by_sampleid = dict()
        with open(PATH_FCGR, "r") as fp:
            for line in fp.readlines():
                info = line.replace("\n","").split("\t")
                path = info[0]
                sampleid = Path(path).stem
                label = info[col_labels] if col_labels else "unknwon"
                list_paths.append(Path(path))
                labels_by_sampleid[sampleid] = label
                # index_labels.append(label)

    # 0. load index
    console.print(":dna: Loading Index...")
    index = faiss.read_index(str(PATH_INDEX))
    
    # 1. load encoder
    console.print(":dna: Loading Encoder...")
    encoder =tf.keras.models.load_model(PATH_ENCODER)

    # 3. create embeddings
    # preprocessing of each FCGR to feed the model 
    preprocessing = lambda x: x / x.max() 

    # create dataset to fed Encoder
    index_data = DataLoader(
        list_paths=list_paths,
        batch_size=batch_size,
        shuffle=False,
        preprocessing=preprocessing,
        inference_mode=True
    )

    # embeddings
    embeddings = []
    n_batches = len(index_data)
    for data in track(iter(index_data), description=f"Creating embeddings | total in query = {len(list_paths)}", total=n_batches):
        encoded_imgs = encoder(data).numpy()
        embeddings.append(encoded_imgs)

    query_emb = np.concatenate(embeddings, axis=0)

    # TODO: load metadata index: for each position of the index, the sample id and the label.
    # (...) return labels
    console.print(":dna: Loading index metadata...")
    from collections import namedtuple

    #TODO use correct labels from txt file 
    Metadata=namedtuple("Metadata",["sample_id","label"])
    with open(PATH_INDEX.parent.joinpath("id_embeddings.json"),"r") as fp:
        index2metadata = {int(idx): 
                        Metadata(
                            Path(path).stem, 
                            labels_by_sampleid[Path(path).stem]
                            ) 
                            for idx, path in json.load(fp).items()}

    # get labels from idx
    get_label_ = lambda idx: index2metadata.get(idx).label
    get_sample_id_ = lambda idx: index2metadata.get(idx).sample_id
    # vectorized version
    get_label = np.vectorize(get_label_)
    get_sample_id = np.vectorize(get_sample_id_)

    # query the index
    console.print(":dna: Querying FAISS index...")
    D,I = index.search(query_emb, neighbors)
    console.print(":dna: Query done...")
    
    console.print(":dna: Querying labels...")
    neighbors_labels= get_label(I)
    neighbors_sample_ids = get_sample_id(I)
    
    console.print(":dna: Creating CSV output...")
    df = pd.DataFrame([{"sample_id_query": path.stem,} for path in list_paths])

    console.print(":dna: Adding label and distances for each neighbor query in CSV output...")
    range_n = list(range(neighbors))
    for n in track(range_n, description=f"Adding label and distances for each neighbor query in CSV output | total neighbors = {neighbors}", total=neighbors):
        df[f"sample_id_{n}"] = neighbors_sample_ids[:,n]
        df[f"label_{n}"] = neighbors_labels[:,n]
        df[f"distance_to_{n}"] = D[:,n]

    # # Save results
    console.print(":dna: Saving results...")
    df.to_csv(Path(OUTDIR).joinpath("query_results.csv"))

    np.save( Path(OUTDIR).joinpath("embeddings.npy") , query_emb )  
    console.print(":dna: Done!")

@app.command("metrics-test", help="Compute metrics for test.", deprecated=True)
def metrics_test_index(
            path_experiment: Annotated[Path, typer.Option("--path-experiment","-p", help="path to experiment")],
            n_neighbors: Annotated[int, typer.Option("--n-neighbors","-n", min=1, help="path to experiment")],
            ) -> None:
    
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

    # load predictions
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
