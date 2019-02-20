from copy import copy
from json import load
from typing import Dict, List, Tuple

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

        self.update_status_history_for_conversation(id)

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

    def get_true_and_predicted_scores_at_utterance_index(self,utterance_index : int,
                                                         categorize_true_scores : bool = True,
                                                         categorize_predicted_scores : bool = False) -> Tuple[List[float],List[float]]:

        true_scores : List[int] = []
        predicted_scores : List[float] = []

        for n, conversation in enumerate(self.conversations):

            if n in self.conversations_excluded_from_evaluation:
                continue

            status: Dict[str, float] = self.status_per_conversation[n][utterance_index]

            for speaker, label in conversation.speakers_with_labels.items():

                if categorize_true_scores:

                    if label > self.cut_off_value:
                        true_scores.append(1)
                    else:
                        true_scores.append(0)
                else:
                    true_scores.append(label)

                try:

                    if categorize_predicted_scores:
                        if status[speaker] > self.cut_off_value:
                            predicted_scores.append(1.0)
                        else:
                            predicted_scores.append(0.0)
                    else:
                        predicted_scores.append(status[speaker])

                except KeyError:
                    predicted_scores.append(0.0)

        return (true_scores,predicted_scores)

    def calculate_retrospective_accuracy(self) -> float:
        from sklearn.metrics import accuracy_score #type: ignore

        true_scores : List[int]
        predicted_scores : List[float]

        true_scores, predicted_scores = self.get_true_and_predicted_scores_at_utterance_index(-1,categorize_predicted_scores=True)
        return accuracy_score(true_scores,predicted_scores)

    def calculate_accuracy_at_utterance(self,utterance_index : int) -> float:
        from sklearn.metrics import accuracy_score #type: ignore

        true_scores : List[int]
        predicted_scores : List[float]

        true_scores,predicted_scores = self.get_true_and_predicted_scores_at_utterance_index(utterance_index,categorize_predicted_scores=True)

        return accuracy_score(true_scores,predicted_scores)

    def calculate_auc_at_utterance(self,utterance_index : int) -> float:
        from sklearn.metrics import roc_auc_score #type: ignore

        true_scores : List[int]
        predicted_scores : List[float]

        true_scores, predicted_scores = self.get_true_and_predicted_scores_at_utterance_index(utterance_index)
        return roc_auc_score(true_scores,predicted_scores)

def load_pretrained(location : str) -> Hare:

    if location[-1] != '/':
        location += '/'

    if load(open(location+'metadata.json'))['brainType'] == 'BiGru':

        from hare.bigrubrain import BiGruBrain

        brain: BiGruBrain = BiGruBrain()
        brain.load(location)
        brain.verbose = True

    hare : Hare = Hare()
    hare.brain = brain

    return hare

def load_example_conversations() -> List[Conversation]:

    CONVERSATIONS_FILE : str = dirname(abspath(__file__))+'/example_conversations/001.txt'

    conversations : List[Conversation] = []
    current_conversation : Conversation = Conversation()

    for line in open(CONVERSATIONS_FILE):

        line = line.strip()

        if len(line) == 0:
            continue
        elif line[0] == '#':
            try:
                current_conversation.label_speaker(line.split()[1], 1)
            except IndexError:
                continue

            conversations.append(current_conversation)
            current_conversation = Conversation()

            continue

        speaker, content = line.split('\t')
        current_conversation.add_utterance(speaker, content)

    return conversations