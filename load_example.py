from hare import load_pretrained, Conversation
from hare.brain import BiGruBrain

simple_hare = load_pretrained('hare/pretrained/simple')

convo = Conversation()
convo.add_utterance(speaker='a',content='hate you')
convo.add_utterance(speaker='b',content='i love you')
convo.label_speaker('a',1)

simple_hare.add_conversation(convo)

simple_hare.update_status_history_for_conversation()
print(hare.status_per_conversation)