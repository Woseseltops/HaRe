from os import listdir
from hare import Hare, load_pretrained
from hare.brain import DictBasedBrain
from hare.conversation import import_conversations

#This scripts checks if we have results for all conversations for all specified detectors, and if not starts adding them

ROOT = '../../'
CONVERSATIONS_FILE = ROOT+'datasets/LoL/heldout_conversations_anon.txt'
PRETRAINED_MODELS_LOCATION = ROOT+'hare/pretrained/'

RESULTS_ROOT = 'results/'
DETECTOR_LIST = RESULTS_ROOT+'detectors.config'
RESULT_LOCATION = RESULTS_ROOT+'full_results/'

conversations = []

while True:

    all_detectors = {detector.split()[1].strip(): detector.split()[0] for detector in open(DETECTOR_LIST)}
    all_result_files = set(listdir(RESULT_LOCATION))
    todo = set(all_detectors.keys()) - all_result_files

    if len(todo) == 0:
        print('There are result files for all detectors. Stopping')
        break

    print('Detectors without result files:',', '.join(todo))
    detector = list(todo)[0]

    print('Doing',detector)

    if len(conversations) == 0:
        print('Importing conversations')
        conversations = import_conversations(CONVERSATIONS_FILE)

    print('Loading pretrained model')
    if detector in ['m04']:
        exp_hare = Hare(name='dict_based')
        exp_hare.brain = DictBasedBrain()
        exp_hare.brain.bad_words = ['fuck', 'fck', 'fuk', 'shit', 'stfu', 'wtf', 'suck', 'noob', 'newb', 'n00b', 'fag',
                                    'loser']
    else:
        exp_hare = load_pretrained(PRETRAINED_MODELS_LOCATION+all_detectors[detector])

    result_file = open(RESULT_LOCATION+detector,'w')

    for n, conversation in enumerate(conversations):

        print('Detector',detector,'is processing conv',n)
        exp_hare.add_conversation(conversation)
        exp_hare.save_history_for_conversation(result_file,n)

    print()