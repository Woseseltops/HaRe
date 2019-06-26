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
        self.downsampling : bool = False
        self.downsampling_ratio : float = 0.5

    def train(self,texts : List[str],target : List[int]) -> None:
        raise NotImplementedError

    def classify(self,text : str) -> float:
        return 0

    #The default is to just run self.classify multiple times, but you can decide to optimize things here
    def classify_multiple(self,texts : List[str]) -> List[float]:
        return [self.classify(text) for text in texts]

    def save(self, location : str) -> None:
        raise NotImplementedError

class RandomBrain(AbstractBrain):

    def classify(self,text : str) -> float:

        from random import uniform
        return uniform(0,1)

class DictBasedBrain(AbstractBrain):

    bad_words : List[str] = []

    def classify(self,text : str) -> float:

        nr_of_bad_words : int = 0

        for bad_word in self.bad_words:
            nr_of_bad_words += text.lower().count(bad_word)

        return nr_of_bad_words