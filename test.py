from hare import load_pretrained, load_example_conversations
from hare.visualize import visualize_accuracy_during_conversations, visualize_auc_during_conversations, \
    visualize_fscore_during_conversations

moba_hare = load_pretrained('hare/pretrained/simple')
for conversation in load_example_conversations():
    moba_hare.add_conversation(conversation)

visualize_accuracy_during_conversations(moba_hare)
visualize_auc_during_conversations(moba_hare)
visualize_fscore_during_conversations(moba_hare)