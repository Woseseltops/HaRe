from sys import argv

from hare import load_pretrained
from hare.conversation import import_conversations

THRESHOLDS = [0.01,0.025,0.05,0.075,0.1,0.25,0.5,0.75]
CONVERSATIONS_FILE = '../datasets/LoL/heldout_conversations_anon.txt'

print('Importing conversations')
conversations = import_conversations(CONVERSATIONS_FILE)

print('Loading pretrained model')
exp_hare = load_pretrained('../hare/pretrained/moba_lstm_embeddings')
result_file = open('moba_lstm_embeddings','w')

for n, conversation in enumerate(conversations):

    print('Processing conv',n)
    exp_hare.add_conversation(conversation)
    exp_hare.save_history_for_conversation(result_file,n)