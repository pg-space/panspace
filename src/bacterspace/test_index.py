"""
This script loads the embeddings from train and val sets into an faiss-index
The embeddings from the test set are used to query the index. 
Labels of the test embeddings and the top-k queried embeddings are returned,
the consensus label using the top-n=1,3,5,10 are computed as well.
"""
import typer
from typing_extensions import Annotated
from pathlib import Path

app = typer.Typer()

@app.command("test-index")
def main(path_experiment: Annotated[Path, typer.Option("--path-experiment","-p", help="path to experiment")]):
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

#####
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