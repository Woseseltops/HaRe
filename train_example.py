from hare import Hare, Conversation
from hare.brain import BiGruBrain

brain : BiGruBrain = BiGruBrain()
brain.embedding_location = '/vol/bigdata/word_embeddings/glove/glove.6B.50d.txt'
brain.verbose = True

hare = Hare()
hare.brain = brain

convo = Conversation()
convo.add_utterance(speaker='a',content='hate you')
convo.add_utterance(speaker='b',content='i love you')
convo.label_speaker('a',1)

hare.add_conversation(convo)

hare.train()
hare.save('/vol/tensusers2/wstoop/HaRe/hare/pretrained/simple')

hare.update_status_history_for_conversation()
hare.visualize_history_for_conversation()