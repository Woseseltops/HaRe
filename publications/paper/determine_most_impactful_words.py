from collections import Counter
from hare import load_pretrained, import_conversations

CONVERSATION_FILE = '../datasets/LoL/heldout_conversations_anon.txt'

moba_brain = load_pretrained('../hare/pretrained/moba').brain
conversations = import_conversations(CONVERSATION_FILE)

for utterance_index in [0,1,2,100,101,102,290,291,292]:

    utterances = []

    for conversation in conversations:

        try:
            utterance_of_interest = conversation.utterances[utterance_index]

            if conversation.speakers_with_labels[utterance_of_interest.speaker] == 1:
               utterances.append(utterance_of_interest.content)

        except IndexError:
            continue

    c = Counter()

    for utterance in utterances:
        most_impactful_word = max(moba_brain.determine_impact_of_words(utterance),key=lambda x:x[1])[0]
        c[most_impactful_word] += 1

    print(utterance_index,c.most_common(5))
