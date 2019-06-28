from hare import Hare, Conversation
from hare.conversation import import_conversations

from sklearn.metrics import fbeta_score

from os import mkdir
from shutil import rmtree
from json import loads, dumps

def true_positives(true, predicted):

    result = 0

    for a,b in zip(true,predicted):
        if b == 1 and a == 1:
            result += 1

    return result


def false_positives(true, predicted):
    result = 0

    for a, b in zip(true, predicted):
        if b == 1 and a == 0:
            result += 1

    return result

#General settings
HARE_ROOT = '/vol/tensusers2/wstoop/HaRe/'
ESSAY_ROOT = HARE_ROOT+'publications/essay/'

CONV_HISTORY_FOLDER = ESSAY_ROOT+'results/small_experiments/'
CONVERSATION_HISTORY_FILES_WITH_THRESHOLDS = {'moba_dic_100':[1,2,3,4,5,6,7,8,9,10]}

BETA_VALUES = [0.001,0.01,0.1,1,10,100,1000]

CONVERSATIONS_FILE = HARE_ROOT+'/datasets/LoL/heldout_conversations_anon.txt'
CONVERSATION_LENGTH = 200
NR_OF_CONVERSATIONS = 10

OUTPUT_FOLDER = ESSAY_ROOT+'precalculated_data/'

#From all heldout conversations, load the first 10
conversations = import_conversations(CONVERSATIONS_FILE, cutoff_point=CONVERSATION_LENGTH)[:NR_OF_CONVERSATIONS]

#Cut away utterances by some speakers

#Save the true target data
open(OUTPUT_FOLDER+'target.js','w').write(dumps([conversation.speakers_with_labels for conversation in conversations]))

#Go through all detectors, with all thresholds
hares = []

for conv_hist_file, thresholds in CONVERSATION_HISTORY_FILES_WITH_THRESHOLDS.items():

    #For each conversation, read the status at every point during the conversation
    status_per_conversation = []

    for n, line in enumerate(open(CONV_HISTORY_FOLDER+conv_hist_file)):
        if n == NR_OF_CONVERSATIONS:
            break

        status_per_conversation.append(loads(line))

    #Cut away utterances by some speakers

    # to do met conversation.remove_speaker()

    #Create a hare object for each threshold
    for threshold in thresholds:

        detector_name = conv_hist_file+'@'+str(threshold)
        folder_name = OUTPUT_FOLDER+detector_name+'/'

        try:
            rmtree(folder_name)
        except FileNotFoundError:
            pass

        mkdir(folder_name)

        h = Hare(name=detector_name)
        h.status_per_conversation = status_per_conversation
        h.cut_off_value = threshold

        for conversation in conversations:
            h.add_conversation(conversation)
            hares.append(h)

        per_player = []
        tp = []
        fp = []
        beta = {b:[] for b in BETA_VALUES}

        #Calculate metrics for this detector/threshold combi
        for utterance_index in range(CONVERSATION_LENGTH):

            for conversation_index in range(NR_OF_CONVERSATIONS):

                try:
                    current_status = h.status_per_conversation[conversation_index][utterance_index]
                except IndexError:
                    continue

                speakers = h.conversations[conversation_index].all_speakers
                per_player.append({speaker:current_status[speaker] >= threshold if speaker in current_status.keys() else False for speaker in speakers})

            true, predicted = h.get_true_and_predicted_scores_at_utterance_index(utterance_index,categorize_predicted_scores=True)
            tp.append(true_positives(true,predicted))
            fp.append(false_positives(true,predicted))

            for b in BETA_VALUES:
                beta[b].append(fbeta_score(true,predicted,b))

        open(folder_name+'per_player.js','w').write(dumps(per_player))
        open(folder_name+'tp.js','w').write(dumps(tp))
        open(folder_name+'fp.js','w').write(dumps(fp))

        for b in BETA_VALUES:
            open(folder_name+'f@'+str(b)+'.js','w').write(dumps(beta[b]))