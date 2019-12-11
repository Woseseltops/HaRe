from hare import Hare
from hare.conversation import import_conversations
from json import loads
from sklearn.metrics import fbeta_score

def find_optimal_conversation(main_detector,other_detector,all_scores):

    best_conversations_per_threshold = {}

    for threshold, scores_per_threshold in all_scores[main_detector].items():

        best_conversations_per_threshold[threshold] = []

        for convo_index, conversation_scores in enumerate(scores_per_threshold):

            cumulative_score_main = sum(conversation_scores)
            all_scores_other_detector = [sum(all_scores[other_detector][t][convo_index]) for t in range(1,10)]

            best_conversations_per_threshold[threshold].append({'cumulative_score':cumulative_score_main,'cumulative_other_score':max(all_scores_other_detector),'convo_index':convo_index})

        best_conversations_per_threshold[threshold] = sorted(best_conversations_per_threshold[threshold],reverse=True,key= lambda x: x['cumulative_score']-x['cumulative_other_score'])

    return best_conversations_per_threshold

ROOT = '../../'
CONVERSATION_HISTORY_FOLDER = 'results/full_results/'
CONVERSATIONS_FILE = ROOT+'datasets/LoL/heldout_conversations_anon.txt'
CONVERSATION_LENGTH = 200
PRINT_OUTPUT = False

INTERESTING_POINTS_IN_CONVERSATION = [10,50,100,150]
DETECTOR_THRESHOLDS = {'m02':[0.001,0.01,0.05,0.075,0.1,0.25,0.5,1],'m04':[1,2,3,4,5,6,7,8,9,10]}
open_conversation_history_files = {}
all_scores = {}

conversations = import_conversations(CONVERSATIONS_FILE, cutoff_point=CONVERSATION_LENGTH)

for detector in DETECTOR_THRESHOLDS.keys():
    open_conversation_history_files[detector] = open(CONVERSATION_HISTORY_FOLDER+detector)
    all_scores[detector] = {}

headers = []

for convo_index, conversation in enumerate(conversations):

    #For this conversation, we want to know the conversation history for every detector
    for detector, thresholds in DETECTOR_THRESHOLDS.items():
        conversation_history = loads(open_conversation_history_files[detector].readline())

        scores_for_this_conversation = []

        #We check what scores this means for every threshold
        for threshold in thresholds:

            if threshold not in all_scores[detector].keys():
                all_scores[detector][threshold] = []

            h = Hare()
            h.add_conversation(conversation)
            h.status_per_conversation = [conversation_history]
            h.cut_off_value = threshold

            for point_in_conversation in INTERESTING_POINTS_IN_CONVERSATION:
                true, predicted = h.get_true_and_predicted_scores_at_utterance_index(point_in_conversation,categorize_predicted_scores=True)
                score = fbeta_score(true, predicted, 1)

                scores_for_this_conversation.append(score)

                if convo_index == 0:
                    headers.append(detector+':'+str(threshold)+':'+str(point_in_conversation))

            all_scores[detector][threshold].append(scores_for_this_conversation[-len(INTERESTING_POINTS_IN_CONVERSATION):])

    if PRINT_OUTPUT:

        if convo_index == 0 and PRINT_OUTPUT:
            print('convo_id',' '.join(headers))

        print(convo_index,' '.join([str(s) for s in scores_for_this_conversation]))

    if convo_index > 0 and convo_index%100 == 0:
        print(convo_index)
        find_optimal_conversation('m02','m04',all_scores)
