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

    def get_all_utterances_for_speaker(self,name : str, until_utterance_index : int = None) -> List[str]:

        result : List[str] = []

        for n,utterance in enumerate(self.utterances):

            if until_utterance_index != None and n == until_utterance_index:
                break

            if utterance.speaker == name:
                result.append(utterance.content)

        return result

    def __len__(self) -> int:
        return len(self.utterances)

    def __str__(self) -> str:

        s : str = ''

        for utterance in self.utterances:
            s += utterance.speaker + '\t' + utterance.content + '\n'

        s += '#toxic ' + ' '.join([speaker for speaker,label in self.speakers_with_labels.items() if label == 1])

        return s + '\n'