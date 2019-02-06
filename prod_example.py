from hare import Hare, Conversation
from hare.brain import RandomBrain

random_hare = Hare()
random_hare.brain = RandomBrain()

convo = Conversation()
random_hare.add_conversation(convo)

convo.add_utterance(speaker='a',content='hello')
convo.add_utterance(speaker='b',content='hello')
convo.add_utterance(speaker='a',content='how is everyone doing?')

random_hare.update_status_history_for_conversation(0)
print(random_hare.status_per_conversation[0])

convo.label_speaker('b',0.9)
acc = random_hare.calculate_retrospective_accuracy()

print(acc)