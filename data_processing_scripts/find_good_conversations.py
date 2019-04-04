from hare import Conversation

CONVERSATIONS_FILE = '../datasets/LoL/conversations.txt'
NR_OF_CONVERSATIONS = 600
conversations = []
current_conversation = Conversation()


for line in open(CONVERSATIONS_FILE):

    line = line.strip()

    if len(line) == 0:
        continue
    elif line[0] == '#':
        try:
            current_conversation.label_speaker(line.split()[1],1)
        except IndexError:
            continue

        conversations.append(current_conversation)
        current_conversation = Conversation()

        if len(conversations)%100 == 0:
            print(len(conversations))

        if len(conversations) == NR_OF_CONVERSATIONS:
            break

        continue

    speaker,content = line.split('\t')
    current_conversation.add_utterance(speaker,content)

# for n, conversation in enumerate(conversations):
#
#     if len(conversation.utterances) < 100:
#
#         labeled_speaker = list(conversation.speakers_with_labels.keys())[0]
#         print(n,conversation.get_all_utterances_for_speaker(labeled_speaker))

for convo_id in [62,116,242,273,412,459,537]:

    c = conversations[convo_id]
    pseudonyms = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    translated_names = {speaker: pseudonyms[n] for n, speaker in enumerate(c.all_speakers)}

    for utterance in c.utterances:
        print(translated_names[utterance.speaker]+'\t'+utterance.content)

    toxic_player = translated_names[list(c.speakers_with_labels.keys())[0]]
    print('#toxic',toxic_player)
    print()
