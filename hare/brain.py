from typing import List

class AbstractBrain():

    def __init__(self) -> None:
        self.dependencies : List[str] = []

    def classify(self,text) -> float:
        return 0

class RandomBrain(AbstractBrain):

    def classify(self,text) -> float:

        from random import uniform
        return uniform(0,1)

class BiGruBrain(AbstractBrain):

    def __init__(self) -> None:

        self.dependencies = ['tensorflow']
