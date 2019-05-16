from hare import load_pretrained, Conversation, load_example_conversations
from hare.tensorflowbrain import BiGruBrain

simple_hare = load_pretrained('hare/pretrained/moba')

print(simple_hare.brain.determine_impact_of_words('well played noob'))

convo = Conversation()
convo.add_utterance(speaker='a',content='i am nice')
convo.add_utterance(speaker='b',content='FCK U YOU SUCK')
convo.add_utterance(speaker='b',content='YOU ARE LOSERS')
convo.add_utterance(speaker='a',content='well done')
convo.add_utterance(speaker='b',content='noobs fuckheads')
convo.add_utterance(speaker='a',content='no problem')
convo.label_speaker('b',1)

simple_hare.add_conversation(convo)

simple_hare.update_status_history_for_conversation()
simple_hare.visualize_history_for_conversation()

for n, conversation in enumerate(load_example_conversations()):
    simple_hare.add_conversation(conversation)
    simple_hare.visualize_history_for_conversation(n+1)