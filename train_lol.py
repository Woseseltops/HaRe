from hare import Hare, Conversation
from hare.bigrubrain import BiGruBrain

#Load the conversations
CONVERSATIONS_FILE = 'datasets/LoL/conversations_anon.txt'
NR_OF_CONVERSATIONS = 5000
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

#Add to a hare object
moba_hare = Hare()
for conversation in conversations:
    moba_hare.add_conversation(conversation)

moba_hare.brain = BiGruBrain()
moba_hare.brain.downsampling = True
moba_hare.brain._max_sequence_length = 500

moba_hare.train()
moba_hare.save('moba')