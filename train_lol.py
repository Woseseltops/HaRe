from hare import Hare, Conversation
from hare.tensorflowbrain import LSTMBrain
from hare.conversation import import_conversations

#Load the conversations
CONVERSATIONS_FILE = 'datasets/LoL/train_conversations_anon.txt'
print('Importing conversations')
conversations = import_conversations(CONVERSATIONS_FILE)

#Add to a hare object
moba_hare = Hare()
for conversation in conversations:
    moba_hare.add_conversation(conversation)

moba_hare.brain = LSTMBrain()
moba_hare.brain.verbose = True
moba_hare.brain.downsampling = True
moba_hare.brain.learning_epochs = 6
moba_hare.brain._max_sequence_length = 500

moba_hare.train()
moba_hare.save('moba_lstm')