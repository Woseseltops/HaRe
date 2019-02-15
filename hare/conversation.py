from typing import List, Dict, Set

class Utterance():

    def __init__(self,speaker : str ='anonymous',content : str= '') -> None:

        self.speaker : str = speaker
        self.content : str = content

    def __repr__(self):
        return self.speaker+': '+self.content

class Conversation():

    def __init__(self) -> None:

        self.utterances : List[Utterance] = []
        self.all_speakers : Set[str] = set()
        self.speakers_with_labels : Dict[str,float] = {}

    def add_utterance(self,speaker : str ='anonymous',content : str ='') -> None:

        self.add_utterance_object(Utterance(speaker=speaker,content=content))

    def add_utterances(self,utterances : List[Utterance]) -> None:

        for utterance in utterances:
            self.add_utterance_object(utterance)

    def add_utterance_object(self,utterance : Utterance) -> None:

        self.utterances.append(utterance)
        self.all_speakers.add(utterance.speaker)

        if utterance.speaker not in self.speakers_with_labels.keys():
            self.speakers_with_labels[utterance.speaker] = 0

    def label_speaker(self,speaker : str,label : float) -> None:
        self.speakers_with_labels[speaker] = label

    def get_all_utterances_for_speaker(self,name : str) -> List[str]:

        return [utterance.content for utterance in self.utterances if utterance.speaker == name]