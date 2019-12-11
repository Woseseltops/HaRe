from hare import load_pretrained
from hare.conversation import import_conversations

from json import dumps

ROOT = '../../'
CONVERSATIONS_FILE = ROOT+'datasets/LoL/heldout_conversations_anon.txt'
PRETRAINED_MODELS_LOCATION = ROOT+'hare/pretrained/'
OUTPUT_FILENAME = 'activations.js'
BRAIN_NAME = 'moba_bigru_embedding'
LAYERS = [1,2]
NR_OF_NEURONS = 32

h = load_pretrained(PRETRAINED_MODELS_LOCATION+BRAIN_NAME)
conversations = import_conversations(CONVERSATIONS_FILE)

result = {}

for layer in LAYERS:

    print('Doing layer',layer)
    result[layer] = []

    for conversation in conversations[:1]:
        word_scores_per_neuron = h.brain.visualize_neuron_specializations(layer,['@MeghanMcCain was terrible on @TheFive yesterday. Angry and obnoxious, she will never make it on T.V. @FoxNews can do so much better!'])
        for word_index, (word, activations) in enumerate(word_scores_per_neuron[0]):

            current_row = [word]
            for neuron_index in range(NR_OF_NEURONS):
                current_row.append(float(word_scores_per_neuron[neuron_index][word_index][1]))

            result[layer].append(current_row)

open(OUTPUT_FILENAME, 'w').write('var activations = '+dumps(result))