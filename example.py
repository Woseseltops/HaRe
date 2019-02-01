from hare import Hare, Conversation
from hare.brain import RandomBrain

random_hare = Hare()
random_hare.brain = RandomBrain()

convo = Conversation()
random_hare.add_conversation(convo)

convo.add_utterance(speaker='a',content='hello')
status = random_hare.get_status()

convo.add_utterance(speaker='b',content='hi everyone')
status = random_hare.get_status()

convo.label_speaker('b',0.9)
acc = random_hare.calculate_retrospective_accuracy()

print(acc)