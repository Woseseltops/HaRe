from hare import Hare, Conversation
from hare.visualize import visualize_toxicity_for_one_conversation

from json import loads

CONVERSATION_HISTORY_FILES = ['moba_0.5_4000']

CONVERSATIONS_FILE = '../datasets/LoL/heldout_conversations_anon.txt'

CONVERSATION_LENGTH = 200

#Add the precalculated conversation history to hare objects
hares = []

for conv_hist_file in CONVERSATION_HISTORY_FILES:

    status_per_conversation = []

    for n, line in enumerate(open(conv_hist_file)):
        status_per_conversation.append(loads(line)[:CONVERSATION_LENGTH])

        if n%100 == 0:
            print(conv_hist_file,n)

    h = Hare(name=conv_hist_file)
    h.status_per_conversation = status_per_conversation

    hares.append(h)

#Load the conversations
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

        current_conversation.utterances = current_conversation.utterances[:CONVERSATION_LENGTH]
        conversations.append(current_conversation)
        current_conversation = Conversation()

        if len(conversations)%100 == 0:
            print(len(conversations))

        continue

    speaker,content = line.split('\t')
    current_conversation.add_utterance(speaker,content)

#Add the conversations to hare
print('Adding conversations')
for conversation in conversations:
    for h in hares:
        h.add_conversation(conversation)

visualize_toxicity_for_one_conversation(hares[0])