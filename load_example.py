from hare import load_pretrained, Conversation
from hare.bigrubrain import BiGruBrain

simple_hare = load_pretrained('hare/pretrained/testhare')

convo = Conversation()
convo.add_utterance(speaker='a',content='hate you')
convo.add_utterance(speaker='b',content='i love you')
convo.label_speaker('a',1)

simple_hare.add_conversation(convo)

simple_hare.update_status_history_for_conversation()
simple_hare.visualize_history_for_conversation()