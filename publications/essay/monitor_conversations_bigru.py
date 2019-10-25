from sys import argv

from hare import load_pretrained
from hare.conversation import import_conversations

ROOT = '../../'
CONVERSATIONS_FILE = ROOT+'datasets/LoL/heldout_conversations_anon.txt'

print('Importing conversations')
conversations = import_conversations(CONVERSATIONS_FILE)

print('Loading pretrained model')
exp_hare = load_pretrained(ROOT+'hare/pretrained/moba_bigru_01')
result_file = open('results/small_experiments/moba_bigru_01','w')

for n, conversation in enumerate(conversations[:100]):

    print('Processing conv',n)
    exp_hare.add_conversation(conversation)
    exp_hare.save_history_for_conversation(result_file,n)