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

class DictBasedBrain(AbstractBrain):

    bad_words : List[str] = ['fuck','fck','fuk',
                             'noob','newb','n00b',
                             'gay', 'fag',
                             'shit','stfu',
                             'suck','loser']

    maximum_nr_of_bad_words_needed : int = 4

    def classify(self,text : str) -> float:

        nr_of_bad_words : int = 0

        for bad_word in self.bad_words:
            nr_of_bad_words += text.lower().count(bad_word)

        score : float = nr_of_bad_words/self.maximum_nr_of_bad_words_needed

        if score > 1:
            return 1.0
        else:
            return score