from sys import argv

from hare import load_pretrained, Conversation

#TRAINING_SIZES = [125,250,500,1000,2000,4000]
#DOWNSAMPLE_RATIOS = [0.5,0.4,0.3,0.2,0.1]

CONVERSATIONS_FILE = '../datasets/LoL/conversations_anon.txt'
LOAD_NR_OF_CONVERSATIONS = 5000
START_AT_CONVERSATION = 4000

training_size = argv[1]
downsample_ratio = argv[2]

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

        if len(conversations) == LOAD_NR_OF_CONVERSATIONS:
            break

        continue

    speaker,content = line.split('\t')
    current_conversation.add_utterance(speaker,content)

conversations = conversations[START_AT_CONVERSATION:]

exp_hare = load_pretrained('../hare/pretrained/moba_'+str(downsample_ratio)+'_'+str(training_size))
result_file = open('moba_'+str(downsample_ratio)+'_'+str(training_size),'w')

for n, conversation in enumerate(conversations):

    print('training size',training_size,'downsample ratio',downsample_ratio,'processing conversation',n)
    exp_hare.add_conversation(conversation)
    exp_hare.save_history_for_conversation(result_file,n)