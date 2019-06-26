from hare import Hare, Conversation
from hare.conversation import import_conversations
from hare.visualize import visualize_precision_during_conversations, visualize_recall_during_conversations, visualize_auc_during_conversations, visualize_fscore_during_conversations, visualize_accuracy_during_conversations, visualize_true_positives_during_conversations, visualize_false_positives_during_conversations

from json import loads

#General settings
CONV_HISTORY_FOLDER = 'small_experiments/'
CONVERSATION_HISTORY_FILES_WITH_THRESHOLDS = {'moba_dic_100':[1,3],
                                             'moba_lstm_long_training_100':[0.01,0.1],
                                             'moba_bigru_100':[0.01,0.1],
                                             'moba_bigru_embeddings_100': [0.01,0.1]
                                              }

#CONVERSATION_HISTORY_FILES_WITH_THRESHOLDS = {'moba_dic': [1,3],
#                                              'moba_lstm':[0.01,0.1],
#                                              'moba_lstm_embeddings':[0.01,0.1],}

CONVERSATIONS_FILE = '../datasets/LoL/heldout_conversations_anon.txt'
CONVERSATION_LENGTH = 200

#Add the precalculated conversation history to hare objects
hares = []

for conv_hist_file, thresholds in CONVERSATION_HISTORY_FILES_WITH_THRESHOLDS.items():

    status_per_conversation = []

    for n, line in enumerate(open(CONV_HISTORY_FOLDER+conv_hist_file)):
        status_per_conversation.append(loads(line)[:CONVERSATION_LENGTH])

        if n%100 == 0:
            print(conv_hist_file,n)

    for threshold in thresholds:
        h = Hare(name=conv_hist_file+str(threshold))
        h.status_per_conversation = status_per_conversation
        h.cut_off_value = threshold

        hares.append(h)

#Load the conversations
conversations = import_conversations(CONVERSATIONS_FILE, cutoff_point=CONVERSATION_LENGTH)[:100]

#Add the conversations to hare
print('Adding conversations')
for conversation in conversations:
    for h in hares:
        h.add_conversation(conversation)

#Visualize the result
print('Making true positive visualization')
visualize_true_positives_during_conversations(hares,save_with_filename='true_positives.png')

print('Making false positive visualization')
visualize_false_positives_during_conversations(hares,save_with_filename='false_positives.png')

print('Making f1 visualization')
visualize_fscore_during_conversations(hares,beta=0.1,save_with_filename='f0.1score.png')
visualize_fscore_during_conversations(hares,beta=0.5,save_with_filename='f0.5score.png')
visualize_fscore_during_conversations(hares,beta=1,save_with_filename='f1score.png')
visualize_fscore_during_conversations(hares,beta=2,save_with_filename='f2score.png')
visualize_fscore_during_conversations(hares,beta=10,save_with_filename='f10score.png')

print('Making accuracy visualization')
visualize_accuracy_during_conversations(hares,save_with_filename='accuracy.png')

print('Making precision visualization')
visualize_precision_during_conversations(hares,save_with_filename='precision.png')

print('Making recall visualization')
visualize_recall_during_conversations(hares,save_with_filename='recall.png')

print('Making AUC visualization')
visualize_auc_during_conversations(hares,save_with_filename='auc.png')
