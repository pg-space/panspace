import json
import tensorflow as tf
import numpy as np
import faiss

from faiss import write_index, read_index

from pathlib import Path
from dnn.loaders.VARdataloader import DataLoaderVAR as DataLoader

def main(args):
        
    PATH_EXP=args.path_exp #""
    LATENT_DIM=args.latent_dim # 100
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
    for data in iter(index_data):
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
    write_index(index, str(PATH_INDEX))


if __name__ == "__main__":
    import argparse
    from rich_argparse import RichHelpFormatter
    
    ## Parser
    parser = argparse.ArgumentParser(
                description="Create Index with train and validation sets", 
                prog="Faiss-Index", 
                formatter_class=RichHelpFormatter
                )
    parser.add_argument("--path-exp", dest="path_exp", type=str, default=None, required=True,
                        help="path to experiment"
                        )
                    
    parser.add_argument("--latent-dim", help="dimension of the embedding", dest="latent_dim", type=int, required=True,
                        )

    args = parser.parse_args()

    main(args)