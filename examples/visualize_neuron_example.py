from hare.main import load_pretrained
from hare.conversation import import_conversations

CONVERSATIONS_FILE = 'datasets/LoL/heldout_conversations_anon.txt'

print('Importing conversations')
conversations = import_conversations(CONVERSATIONS_FILE)

print('Extracting texts')
texts = []
for convo in conversations:
    for speaker in convo.all_speakers:
        texts.append(' linebreak '.join(convo.get_all_utterances_for_speaker(speaker)))

print('Loading pretrained brain')
brain = load_pretrained('hare/pretrained/moba_0.5_4000').brain

print('Visualizing neurons')
brain.visualize_neuron_specializations(0,texts)
