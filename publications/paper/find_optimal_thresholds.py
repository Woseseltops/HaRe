from hare import Hare, Conversation
from json import loads

#General settings
CONVERSATION_HISTORY_FILES = ['moba_0.5_125','moba_0.5_250','moba_0.5_500','moba_0.5_1000','moba_0.5_2000']

CONVERSATIONS_FILE = '../datasets/LoL/heldout_conversations_anon.txt'
THRESHOLDS = [i/100 for i in range(1,100)]

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

#Find the optimal thresholds
for h in hares:

    optimal_thresholds_per_utterance = []

    for utterance_index in range(200):

        print(h.name,'utterance',utterance_index)

        highest_score = 0
        best_threshold = 0

        for threshold in THRESHOLDS:
            h.cut_off_value = threshold

            score = h.calculate_fscore_at_utterance(utterance_index)
            if score > highest_score:
                highest_score = score
                best_threshold = threshold

        optimal_thresholds_per_utterance.append(best_threshold)

    for i in optimal_thresholds_per_utterance:
        print(i)