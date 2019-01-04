# HaRe
HaRe (Harassment Recognizer) is a command line tool and Python library to automatically detect harassment as it happens (real-time) with the help of machine learning techniques.

![](https://imgur.com/ROmvxnE.png)

## 1. Using HaRe as command line tool

## 2. Using HaRe as Python library

### 2.1 Basic usage

The easiest way to use HaRe is by simply loading a pretrained HaRe model included with this repo in the `models` folder, like the one named 'moba':

```python
from hare import load_pretrained

moba_hare = load_pretrained('moba')
```

You can then use this object to monitor conversations in progress:

```python
moba_hare.start_conversation(conversation_id='example_convo')
moba_hare.add_utterance(speaker='a',content='hello')
moba_hare.add_utterance(speaker='b',content='hi everyone')
```

You can also add multiple sentences at once; for example a whole conversation if it has already finished.

```python
from hare import Utterance

moba_hare.add_utterances([Utterance(speaker='a',content='good luck'),
                          Utterance(speaker='c',content='ur all n00bs')])
```

At any point in time, you can then request the current status of the conversation according to this HaRe model:

```python
moba_hare.get_status()
```

If you want to reuse this HaRe model for another conversation, make sure to create a new conversation before you start adding utterances. You can later use `switch_conversation` to indicate which conversation is currently active.

```python
moba_hare.start_conversation(conversation_id='second_convo')
moba_hare.start_conversation(conversation_id='third_convo')
moba_hare.switch_conversation(conversation_id='example_convo')
```

### 2.2 Evaluating

If you have a labeled dataset (that is: for each conversation an indication which participants are considered toxic), HaRe can calculate to what extent its judgments match the labels. A label can range from the default 0 (not toxic at all) to 1 (maximally toxic). Let's label speaker `c`: 

```python
moba_hare.label_speaker('c',0.9)
```

There are several evaluation metrics, depending on what is important to you (detecting ALL harassment, detecting harassment quickly, no false positives, etc):

```python
moba_hare.calculate_accuracy()
```

These metrics are calculated on the basis on all conversations the HaRe object is aware of that have at least 1 labeled participant. If you want to exclude a label from evaluation, simply add it to the `conversations_excluded_for_evaluation` list:

```python
moba_hare.conversations_excluded_for_evaluation = ['example_convo']
```

### 2.3 Training

At some point, you might want to do some training yourself. This can for example be the case because you are applying HaRe in another domain than the pretrained models, and harassment looks slightly different there, or because you even want to detect something different than harassment.

#### 2.3.1 Recommended: transfer learning

Whatever your goals are, it is probably most effective to repurpose the existing HaRe models ('transfer learning'). To achieve this, simply load the pretrained model that best matches your goal, add some conversations and label them, like we have done above. If you want to exclude conversations from training, add them to the `conversations_excluded_for_training` list:

```python
from hare import load_pretrained, Utterance

moba_hare = load_pretrained('moba')

moba_hare.start_conversation(conversation_id='convo_001')
moba_hare.label_speaker('b',1)
moba_hare.add_utterances([Utterance(speaker='a',content='good luck'),
                          Utterance(speaker='b',content='ur all n00bs')])

moba_hare.start_conversation(conversation_id='convo_002')
moba_hare.label_speaker('b',1)
moba_hare.add_utterances([Utterance(speaker='a',content='hi'),
                          Utterance(speaker='b',content='SHUT UP!')])

moba_hare.conversations_excluded_for_training = ['convo_002']
```

Then, use the `retrain` command to take the old model and refit it to you new dataset. You can then use `save` to store it as a pretrained model in the `models` folder. You can later access this model with `load_pretrained` like the other pretrained models in that same folder.

```python
moba_hare.retrain()
moba_hare.save(name='moba_extended')
```

#### 2.3.2 Starting from scratch with word embeddings

If you don't want to use transfer learning with an existing model, you can also start from scratch. The procedure is largely the same, except that you don't use the `load_pretrained` function, and use `train` instead of `retrain`:

```python
from hare import Hare, Utterance

new_hare = Hare()

new_hare.start_conversation(conversation_id='convo_001')
new_hare.label_speaker('b',1)
new_hare.add_utterances([Utterance(speaker='a',content='good luck'),
                          Utterance(speaker='b',content='ur all n00bs')])

new_hare.start_conversation(conversation_id='convo_002')
new_hare.label_speaker('b',1)
new_hare.add_utterances([Utterance(speaker='a',content='hi'),
                          Utterance(speaker='b',content='SHUT UP!')])

new_hare.train()
```

It will probably be highly effective to use so-called word embeddings during training. You can see these embeddings as a dictionary that translates from a word's characters to an estimate of its meaning. Research has shown that classifying these 'meanings' is much more successful that classifying the raw words. [reference] . To use them, simply point your HaRe object to the embedding file in the `embeddings` folder before training:

```python
new_hare.embedding_file = 'english_large'
new_hare.train()
```

Of course, these embeddings should be in the same language as the rest of your dataset.
