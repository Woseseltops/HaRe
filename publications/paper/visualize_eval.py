from hare import Hare, Conversation
from hare.visualize import visualize_precision_during_conversations, visualize_recall_during_conversations, visualize_auc_during_conversations, visualize_fscore_during_conversations

from json import loads

#General settings
#CONVERSATION_HISTORY_FILES = ['moba_0.5_125','moba_0.5_250','moba_0.5_500','moba_0.5_1000','moba_0.5_2000','moba_0.5_4000']
CONVERSATION_HISTORY_FILES = ['moba_0.5_4000']#,'moba_0.4_4000','moba_0.3_4000','moba_0.2_4000','moba_0.1_4000']

CONVERSATIONS_FILE = '../datasets/LoL/heldout_conversations_anon.txt'

#THRESHOLDS = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
#THRESHOLDS = [0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1]
THRESHOLDS = [0.01,0.025,0.05,0.075,0.1,0.25]

CONVERSATION_LENGTH = 200

#Add the precalculated conversation history to hare objects
hares = []

for conv_hist_file in CONVERSATION_HISTORY_FILES:

    status_per_conversation = []

    for n, line in enumerate(open(conv_hist_file)):
        status_per_conversation.append(loads(line)[:CONVERSATION_LENGTH])

        if n%100 == 0:
            print(conv_hist_file,n)

    for threshold in THRESHOLDS:
        h = Hare(name=threshold)
        h.status_per_conversation = status_per_conversation
        h.cut_off_value = threshold

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

#Visualize the result
print('Making precision visualization')
visualize_precision_during_conversations(hares,save_with_filename='precision.png')

print('Making recall visualization')
visualize_recall_during_conversations(hares,save_with_filename='recall.png')

print('Making fscore visualization')
visualize_fscore_during_conversations(hares,save_with_filename='fscore.png')

print('Making AUC visualization')
visualize_auc_during_conversations(hares,save_with_filename='auc.png')
