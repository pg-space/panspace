import typer 
from typing_extensions import Annotated

app = typer.Typer()

@app.command("query-index")
def query_index(path_experiment: str,
                path_fcgr: str,
                outdir: str,):
    
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

    list_paths = list(Path(DIR_FCGR).rglob("*.npy"))
    # print(list_paths)
    # 0. load index
    index = faiss.read_index(str(PATH_INDEX))

    # 1. load encoder
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
    for data in iter(index_data):
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
    neighbors = 10
    D,I = index.search(query_emb, neighbors)
    neighbors_labels= get_label(I)
    neighbors_sample_ids = get_sample_id(I)

    df = pd.DataFrame([{"sample_id_query": path.stem,} for path in list_paths])

    for n in range(neighbors):
        df[f"sample_id_{n}"] = neighbors_sample_ids[:,n]
        df[f"label_{n}"] = neighbors_labels[:,n]
        df[f"distance_to_{n}"] = D[:,n]

    # # Save results
    df.to_csv(Path(OUTDIR).joinpath("predictions-aux.csv"))

    np.save( Path(OUTDIR).joinpath("embeddings.npy") , query_emb )  
