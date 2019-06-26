from hare import Conversation

CONVERSATIONS_FILE = '../datasets/LoL/conversations_anon.txt'
HELDOUT_CONVERSATIONS = (4000,5000)
GOAL_FILE_LOCATION = '../datasets/LoL/conversations_anon_excl_heldout.txt'

conversations = []
current_conversation = Conversation()
goal_file = open(GOAL_FILE_LOCATION,'w')

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
        continue

    speaker,content = line.split('\t')
    current_conversation.add_utterance(speaker,content)

print('all',len(conversations))
conversations = conversations[:HELDOUT_CONVERSATIONS[0]] + conversations[HELDOUT_CONVERSATIONS[1]:]
print('excl heldout',len(conversations))

for conversation in conversations:
    goal_file.write(str(conversation) + '\n')

