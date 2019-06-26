from hare import load_pretrained, Conversation

CONVERSATIONS_FILE = 'datasets/LoL/single_conversation.txt'

current_conversation = Conversation()

print('loading conversation')

for line in open(CONVERSATIONS_FILE):

    line = line.strip()

    if len(line) == 0:
        continue

    elif line[0] == '#':
        break

    speaker,content = line.split('\t')
    current_conversation.add_utterance(speaker,content)

print('loading pretrained moba')

moba_hare = load_pretrained('hare/pretrained/moba')

print('adding conversation')

moba_hare.add_conversation(current_conversation)

print('visualizing convo')

moba_hare.visualize_history_for_conversation()