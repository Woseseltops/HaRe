from sys import argv

from hare import Hare
from hare.brain import DictBasedBrain
from hare.conversation import import_conversations

THRESHOLDS = [0.01,0.025,0.05,0.075,0.1,0.25,0.5,0.75]
CONVERSATIONS_FILE = '../datasets/LoL/heldout_conversations_anon.txt'
NR_OF_CONVERSATIONS = 1000

print('Importing conversations')
conversations = import_conversations(CONVERSATIONS_FILE)[:NR_OF_CONVERSATIONS]

print('Loading pretrained model')

exp_hare = Hare(name='dict_based')
exp_hare.brain = DictBasedBrain()
exp_hare.brain.bad_words = ['fuck','fck','fuk','shit','stfu','wtf','suck', 'noob','newb','n00b','fag','loser']

result_file = open('moba_dic','w')

for n, conversation in enumerate(conversations):

    print('Processing conv',n)
    exp_hare.add_conversation(conversation)
    exp_hare.save_history_for_conversation(result_file,n)