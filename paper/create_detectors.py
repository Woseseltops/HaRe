from hare import Hare, Conversation
from hare.bigrubrain import BiGruBrain

#Load the conversations
CONVERSATIONS_FILE = '../datasets/LoL/conversations_anon.txt'
NR_OF_CONVERSATIONS = 5000
TRAINING_SIZES = [125,250,500,1000,2000,4000]
DOWNSAMPLE_RATIOS = [0.5,0.4,0.3,0.2,0.1]

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
for downsample_ratio in DOWNSAMPLE_RATIOS:
    for training_size in TRAINING_SIZES:

        print('===','training',downsample_ratio,training_size,'===')

        exp_hare = Hare()
        for conversation in conversations[:training_size]:
            exp_hare.add_conversation(conversation)

        exp_hare.brain = BiGruBrain()
        exp_hare.brain.downsampling = True
        exp_hare.brain.downsampling_ratio = downsample_ratio
        exp_hare.brain._max_sequence_length = 500

        exp_hare.train()
        exp_hare.save('moba_'+str(downsample_ratio)+'_'+str(training_size))