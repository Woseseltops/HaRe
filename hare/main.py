from copy import copy

from typing import Dict, List

from hare.brain import AbstractBrain
from hare.conversation import Conversation

class Hare():

    def __init__(self) -> None:
        self.brain : AbstractBrain = AbstractBrain()

        self.conversations : List[Conversation] = []
        self.status_per_conversation : List[List[Dict[str,float]]] = []

        self.conversations_excluded_from_training : List[int] = []
        self.conversations_excluded_from_evaluation : List[int] = []

        self.cut_off_value : float = 0.5

    def add_conversation(self,conversation) -> None:
        self.conversations.append(conversation)
        self.status_per_conversation.append([])

    def get_status(self,id=0) -> Dict:
        conversation = self.conversations[id]
        status_history = self.status_per_conversation[id]

        #This is where the real work gets done: a status is requested that isn't there yet
        if len(status_history) < len(conversation.utterances):
            for utterance in conversation.utterances[len(status_history):]:

                try:
                    new_status = copy(status_history[-1])
                except IndexError:
                    new_status = {}

                score = self.brain.classify(utterance.content)
                new_status[utterance.speaker] = score
                status_history.append(new_status)

        #Return the last = latest status history, so the current one
        return status_history[-1]

    def calculate_retrospective_accuracy(self) -> float:

        accurately_labeled_speakers = 0
        total_speakers = 0

        for n, conversation in enumerate(self.conversations):
            status = self.get_status(n)

            for speaker, label in conversation.speakers_with_labels.items():

                if (label > self.cut_off_value and status[speaker] > self.cut_off_value) or (label < self.cut_off_value and status[speaker] < self.cut_off_value):
                   accurately_labeled_speakers += 1

                total_speakers += 1

        return accurately_labeled_speakers/total_speakers