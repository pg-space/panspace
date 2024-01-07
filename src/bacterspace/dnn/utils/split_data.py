"""
Select train, validation and test sets
"""
import random
from collections import namedtuple
from collections import Counter
from typing import List, Union, Optional, Tuple, Dict,NamedTuple
from sklearn.model_selection import train_test_split

# namedtuple to reorder datasets based on 'exlusive_on' attribute
VarIdSet = namedtuple("VarIdSet", ["var","id","set"])

class TrainValTestSplit:
    """Get train, val and test sets"""
    def __init__(self,
                    id_labels: List[Union[str,int]], 
                    labels: List[Union[str,int]],
                    seed: Optional[int] = None,
                    id_as_string: bool = True,
                ):
        self._id = range(len(labels))
        self.id_labels  = id_labels
        self.id_as_string = id_as_string
        self.labels = labels
        self.datasets = {}
        if seed: 
            random.seed(seed)

    def __call__(self, 
                    train_size: float = 0.8,
                    test_size: float = None,
                    balanced_on: Optional[List[Union[str,int]]] = None,
                    print_summary: bool = True,
                    ):
        print("Generating train, validation and test sets...")
        # Generate train, val and test sets
        self.train_val_test_split(train_size, test_size, balanced_on)

        # Assing id_labels and  labels to train, test and val sets
        self.__update_datasets()
        print("Datasets successfully generated. See 'datasets' attribute.")
        
        # Print summary of labels if desired
        print(self.get_summary_labels()) if print_summary else None

    def train_val_test_split(self, 
                                train_size: float = 0.7, 
                                test_size: Optional[float] = None, 
                                balanced_on: List[Union[str,int]] = None,
                            ):
        """Get indexes for train, val and test sets"""
        X_dataset = self.id_labels if self.id_labels else self._id
        X = self._id
        y = self.labels if balanced_on is None else balanced_on
        test_size = test_size if test_size else (1 - train_size) / 2
        
        # train+val and test sets
        X_train_val, X_test, y_train_val, y_test = self.__split_dataset(X, y, test_size, balanced_on)
        # split train and val
        balanced_on = y_train_val if balanced_on else None
        X_train, X_val, y_train, y_val = self.__split_dataset(X_train_val, y_train_val, test_size / (1-test_size), balanced_on)
        
        # distribution of indexes in train, val and test sets
        self._id_datasets = {
            "train": [self._id[idx] for idx in X_train],
            "val"  : [self._id[idx] for idx in X_val],
            "test" : [self._id[idx] for idx in X_test]
        }

    def __split_dataset(self, 
                            X: List[Optional[Union[str,int]]], 
                            y: List[Optional[Union[str,int]]], 
                            perc: float, 
                            balanced_on: List[Optional[Union[str,int]]] = None
                        ) -> Tuple:
        """Split one dataset in 2 independent datasets
        Used in train_val_test_split function"""
        X1, X2, y1, y2 = train_test_split(X, y, 
                                        test_size = perc, 
                                        stratify=balanced_on
                                        )
        return X1, X2, y1, y2

    def __count_labels_on(self, labels: List[Union[int,str]]) -> Dict:
        """Count frequency of each label in a list"""
        return dict(Counter(labels))
    
    def get_summary_labels(self,):
        """Count frequency of labels in each dataset"""
        return self._get_summary_var(self.labels)

    def _split_var_on_datasets(self, list_var: List[Union[str,int]]) -> Dict[str,List]:
        """Split a list of variables into train, val and test sets
            using the order obtained in attribute _id_datasets.
        """
        datasets_var = {}
        for name, list_idx in self._id_datasets.items():
            if self.id_as_string is True:
                datasets_var[name] = [str(list_var[idx]) for idx in list_idx]
            else:
                datasets_var[name] = [list_var[idx] for idx in list_idx]
        return datasets_var

    def _get_summary_var(self, list_var: List[Union[str,int]]):
        """Count frequency of labels in each dataset"""
        new_dict = self._split_var_on_datasets(list_var)
        return {ds: self.__count_labels_on(new_dict.get(ds)) 
                    for ds in ["train","val","test"]
                }

    def load_id_datasets(self, _id_datasets: Dict[str, List[int]]):
        """Cargar los id de los datasets desde un diccionario
        Util para reordenar una asignacion ya hecha.
        _id_datasets debe contener las llaves "train", "val" y "test"
        """
        assert all([set_ in ["train","test","val"] for set_ in _id_datasets.keys()])
        self._id_datasets = _id_datasets
        
        # Assing id_labels and  labels to train, test and val sets
        self.__update_datasets()

    def __update_datasets(self,):
        """Assing id_labels and labels to train, test and val sets
        based on attribute _id_datasets"""
        # id_labels and labels distributed in train, val and test sets
        self.datasets["id_labels"] = self._split_var_on_datasets(self.id_labels)
        self.datasets["labels"]    = self._split_var_on_datasets(self.labels)