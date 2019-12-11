from typing import List, Dict, Set, Optional
from collections import Counter

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

    def remove_speaker(self,speaker_to_remove : str):

        clean_utterances : List[Utterance] = [utterance for utterance in self.utterances if utterance.speaker != speaker_to_remove]
        self.utterances = clean_utterances

    def calculate_activity_per_speaker(self):

        nr_of_utterances : int = len(self.utterances)
        return {speaker: freq/nr_of_utterances for speaker,freq in Counter([utterance.speaker for utterance in self.utterances]).most_common()}

    def as_single_str(self,separator : str = 'LINEBREAK'):
        separator : str = ' ' + separator + ' '
        return separator.join([utterance.content for utterance in self.utterances])

    def __len__(self) -> int:
        return len(self.utterances)

    def __str__(self) -> str:

        s : str = ''

        for utterance in self.utterances:
            s += utterance.speaker + '\t' + utterance.content + '\n'

        s += '#toxic ' + ' '.join([speaker for speaker,label in self.speakers_with_labels.items() if label == 1])

        return s + '\n'

def import_conversations(filename : str, cutoff_point : Optional[int] = None) -> List[Conversation]:

    conversations : List[Conversation] = []
    current_conversation : Conversation = Conversation()

    line : str

    for line in open(filename):

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

        speaker : str
        content : str

        speaker, content = line.split('\t')

        if cutoff_point is None or len(current_conversation.utterances) < int(cutoff_point):
            current_conversation.add_utterance(speaker, content)

    return conversations