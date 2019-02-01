from typing import List, Dict

class Conversation():

    def __init__(self) -> None:

        self.utterances : List[Utterance] = []
        self.speakers_with_labels : Dict[str,float] = {}

    def add_utterance(self,speaker='anonymous',content=None) -> None:

        self.add_utterance_object(Utterance(speaker=speaker,content=content))

    def add_utterances(self,utterances) -> None:

        for utterance in utterances:
            self.add_utterance_object(utterance)

    def add_utterance_object(self,utterance) -> None:

        self.utterances.append(utterance)

        if utterance.speaker not in self.speakers_with_labels.keys():
            self.speakers_with_labels[utterance.speaker] = 0

    def label_speaker(self,speaker,label) -> None:
        self.speakers_with_labels[speaker] = label

class Utterance():

    def __init__(self,speaker='anonymous',content=None) -> None:

        self.speaker : str = speaker
        self.content : str = content