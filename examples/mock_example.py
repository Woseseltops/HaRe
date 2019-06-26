from hare import Hare, Conversation
from hare.tensorflowbrain import BiGruBrain

mockhare = Hare()
mockhare.brain = BiGruBrain()

for i in range(10000):
    convo = Conversation()
    convo.add_utterance(speaker='a', content='c c c c c')
    convo.add_utterance(speaker='b', content='c c c c c')
    convo.add_utterance(speaker='b', content='c c c c b')
    convo.add_utterance(speaker='a', content='c c c c a')
    convo.label_speaker('b', 1)

    mockhare.add_conversation(convo)

mockhare.train()
mockhare.visualize_history_for_conversation()