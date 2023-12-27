"""
This script loads the embeddings from train and val sets into an faiss-index
The embeddings from the test set are used to query the index. 
Labels of the test embeddings and the top-k queried embeddings are returned,
the consensus label using the top-n=1,3,5,10 are computed as well.
"""

import json
import tensorflow as tf
import numpy as np
import faiss
import pandas as pd

from collections import Counter
from faiss import write_index, read_index

from pathlib import Path
from dnn.loaders.VARdataloader import DataLoaderVAR as DataLoader

def main(args):
        
    PATH_EXP=args.path_exp #""
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


if __name__ == "__main__":
    import argparse
    from rich_argparse import RichHelpFormatter
    
    ## Parser
    parser = argparse.ArgumentParser(
                description="Test: query Faiss Index with test set", 
                prog="Query", 
                formatter_class=RichHelpFormatter
                )
    parser.add_argument("--path-exp", dest="path_exp", type=str, default=None, required=True,
                        help="path to experiment"
                        )
                    
    # parser.add_argument("--latent-dim", help="dimension of the embedding", dest="latent_dim", type=int, required=True,
    #                     )

    args = parser.parse_args()

    main(args)


#####
           


# from collections import Counter
# from pathlib import Path
# import faiss
# import json 
# import yaml
# import numpy as np
# import pandas as pd

# ## Params
# with open("params.yaml") as fp:
#     params = yaml.load(fp, Loader=yaml.FullLoader)
# dim = params["train"]["latent_dim"] 
# OUTDIR = params["outdir"]
# KMER = params["kmer_size"]
# ARCHITECTURE = params['train']['architecture']
# OUTDIR_TRAIN=params["train"]["outdir"]
# Path(f"{OUTDIR_TRAIN}/{ARCHITECTURE}")

# # test
# PATH_TEST=Path(f"{OUTDIR_TRAIN}/test")
# PATH_TEST.mkdir(exist_ok=True, parents=True)

# # index embeddings
# # xb = np.load(f"{OUTDIR_TRAIN}/faiss-embeddings/embeddings.npy").astype("float32")
# # with open(f"{OUTDIR_TRAIN}/faiss-embeddings/id_embeddings.json") as fp:
# #     id_xb = json.load(fp)
# #     id_xb = {int(k): v for k,v in id_xb.items()}
# index = faiss.read_index(OUTDIR_TRAIN.joinpath("faiss-embeddings/bacterial.index"))

# # query embeddings
# xq = np.load(f"{OUTDIR_TRAIN}/faiss-embeddings/query_embeddings.npy").astype("float32")

# with open(f"{OUTDIR_TRAIN}/faiss-embeddings/query_embeddings.json") as fp:
#     id_query = json.load(fp)
#     id_query = {int(k): v for k,v in id_query.items()}

# # build the index
# index = faiss.IndexFlatL2(dim)
# print(index.is_trained)

# # add vectors to the index
# index.add(xb)                  
# print(index.ntotal, "vectors in the index (train+val)")

# # load labels for train+val and test
# with open(f"{OUTDIR_TRAIN}/split-train-val-test.json","r") as fp:
#     datasets = json.load(fp)
# trainval = datasets["labels"]["train"] + datasets["labels"]["val"]
# trainval_idx = {k:v for k,v in enumerate(trainval)}

# # get labels from idx
# get_label_= lambda idx: trainval_idx.get(idx)
# # vectorize version
# get_label = np.vectorize(get_label_)

# # query the index
# neighbors = 10
# D,I = index.search(xq, neighbors)
# neighbors_query = get_label(I)
# ground_truth = datasets["labels"]["test"]

# def majority_vote(list_neighbors): 
#     label, _ = Counter(list_neighbors).most_common(1)[0]
#     return label

# consensus_1  = [majority_vote(neighbors_query[j][:1]) for j in range(len(neighbors_query))]
# consensus_3  = [majority_vote(neighbors_query[j][:3]) for j in range(len(neighbors_query))]
# consensus_5  = [majority_vote(neighbors_query[j][:5]) for j in range(len(neighbors_query))]
# consensus_10 = [majority_vote(neighbors_query[j]) for j in range(len(neighbors_query))]
# df = pd.concat([ pd.DataFrame(datasets["labels"]["test"],columns=["GT"]),
#                  pd.DataFrame.from_dict({"consensus_1": consensus_1, "consensus_3": consensus_3, "consensus_5": consensus_5, "consensus_10": consensus_10}),
#                  pd.DataFrame(neighbors_query)]
#                  ,axis=1
#                  )
# df.to_csv(PATH_TEST.joinpath("test_index.tsv"),sep="\t")