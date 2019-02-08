from hare import Conversation

CONVERSATIONS_FILE = 'datasets/LoL/conversations.txt'
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

        continue

    speaker,content = line.split('\t')
    current_conversation.add_utterance(speaker,content)

print(len(conversations))