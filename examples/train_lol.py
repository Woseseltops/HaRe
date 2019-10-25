from hare import Hare, Conversation
from hare.tensorflowbrain import LSTMBrain, BiGruBrain
from hare.conversation import import_conversations

from hare.embedding import load_embedding_dictionary

#Load the conversations
DATA_ROOT = '../datasets/LoL/'
CONVERSATIONS_FILE = DATA_ROOT+'train_conversations_anon.txt'
print('Importing conversations')
conversations = import_conversations(CONVERSATIONS_FILE)

#Add to a hare object
moba_hare = Hare()
for conversation in conversations:
    moba_hare.add_conversation(conversation)

brain = BiGruBrain()
##brain.embedding_location = DATA_ROOT+'train_toxic_embeddings'
brain.verbose = True
brain.downsampling = True
brain.learning_epochs = 10
brain._max_sequence_length = 500
brain.include_casing_information = True

moba_hare.brain = brain
moba_hare.train()
moba_hare.save('moba_bigru_01')