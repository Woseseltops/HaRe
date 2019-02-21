from hare import load_pretrained, load_example_conversations
from hare.visualize import visualize_retrospective_precision_and_recall

from hare import Hare
from hare.brain import DictBasedBrain

moba_hare = Hare()
moba_hare.brain = DictBasedBrain()

for conversation in load_example_conversations():
    moba_hare.add_conversation(conversation)

THRESHOLDS = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

visualize_retrospective_precision_and_recall(moba_hare)
