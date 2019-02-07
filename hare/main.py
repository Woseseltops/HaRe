from copy import copy
from json import load
from typing import Dict, List

from hare.brain import AbstractBrain, BiGruBrain
from hare.conversation import Conversation

class Hare():

    def __init__(self) -> None:
        self.brain : AbstractBrain = AbstractBrain()

        self.conversations : List[Conversation] = []
        self.status_per_conversation : List[List[Dict[str,float]]] = []

        self.conversations_excluded_from_training : List[int] = []
        self.conversations_excluded_from_evaluation : List[int] = []

        self.cut_off_value : float = 0.5

    def add_conversation(self,conversation : Conversation) -> None:
        self.conversations.append(conversation)
        self.status_per_conversation.append([])

    def get_status(self,id : int =0) -> Dict:
        conversation : Conversation = self.conversations[id]
        status_history : List[Dict[str,float]] = self.status_per_conversation[id]

        #This is where the real work gets done: a status is requested that isn't there yet
        if len(status_history) < len(conversation.utterances):
            self.update_status_history_for_conversation(id)

        #Return the last = latest status history, so the current one
        return status_history[-1]

    def update_status_history_for_conversation(self,id : int =0):

        conversation : Conversation = self.conversations[id]
        status_history : List[Dict[str,float]] = self.status_per_conversation[id]

        new_status: Dict[str, float]

        for n, utterance in enumerate(conversation.utterances[len(status_history):]):

            try:
                new_status = copy(status_history[-1])
            except IndexError:
                new_status = {}

            speaker : str = utterance.speaker
            text_so_far : List[str] = conversation.get_all_utterances_for_speaker(speaker)[:n+1]

            score: float = self.brain.classify(' LINEBREAK '.join(text_so_far))
            new_status[speaker] = score
            status_history.append(new_status)

    def visualize_history_for_conversation(self,id=0):

        conversation : Conversation = self.conversations[id]
        status_history : List[Dict[str,int]] = self.status_per_conversation[id]

        for utterance, status in zip(conversation.utterances,status_history):

            print(utterance)
            print(status)
            print('---')
            print()

    def train(self):

        texts : List[str] = []
        target : List[int] = []

        for n, conversation in enumerate(self.conversations):

            if n in self.conversations_excluded_from_training:
                continue

            for speaker,label in conversation.speakers_with_labels.items():
                texts.append(' LINEBREAK '.join(conversation.get_all_utterances_for_speaker(speaker)))
                target.append(label)

        self.brain.train(texts,target)

    def save(self, location : str):
        self.brain.save(location)

    def calculate_retrospective_accuracy(self) -> float:

        accurately_labeled_speakers : int = 0
        total_speakers : int = 0

        for n, conversation in enumerate(self.conversations):
            status : Dict[str,float] = self.get_status(n)

            for speaker, label in conversation.speakers_with_labels.items():

                if (label > self.cut_off_value and status[speaker] > self.cut_off_value) or (label < self.cut_off_value and status[speaker] < self.cut_off_value):
                   accurately_labeled_speakers += 1

                total_speakers += 1

        return accurately_labeled_speakers/total_speakers

def load_pretrained(location : str) -> Hare:

    if location[-1] != '/':
        location += '/'

    if load(open(location+'metadata.json'))['brainType'] == 'BiGru':

        brain: BiGruBrain = BiGruBrain()
        brain.load(location)
        brain.verbose = True

    hare : Hare = Hare()
    hare.brain = brain

    return hare