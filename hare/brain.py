from typing import List, Dict, Optional, Any
from os import mkdir
from numpy import array # type: ignore
from hare.embedding import load_embedding_dictionary, create_embedding_matrix_for_vocabulary

class UntrainedBrainError(Exception):
    pass

class AbstractBrain():

    def __init__(self) -> None:
        self.dependencies : List[str] = []
        self.verbose : bool = False

    def train(self,texts : List[str],target : List[int]) -> None:
        raise NotImplementedError

    def classify(self,text : str) -> float:
        return 0

    def save(self, location : str) -> None:
        raise NotImplementedError

class RandomBrain(AbstractBrain):

    def classify(self,text : str) -> float:

        from random import uniform
        return uniform(0,1)