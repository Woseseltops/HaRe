# HaRe
HaRe (Harassment Recognizer) is a command line tool and Python library to automatically detect harassment as it happens (real-time) with the help of machine learning techniques.

[plaatje]

## Using HaRe as command line tool

## Using HaRe as Python library

### Basic usage

The easiest way to use HaRe is by simply loading a pretrained HaRe model included with this repo, like the one named 'moba':

```
from hare import load_pretrained

moba_hare = load_pretrained('moba')
```

You can then use this object to monitor conversations in progress:

```
moba_hare.start_conversation(conversation_id='example_convo')
moba_hare.add_utterance(speaker='a',content='hello')
moba_hare.add_utterance(speaker='b',content='hi everyone')
```

You can also add multiple sentences at once; for example a whole conversation if it has already finished.

```
from hare import Utterance

moba_hare.add_utterances([Utterance(speaker='a',content='good luck'),
                          Utterance(speaker='c',content='ur all n00bs')])
```

At any point in time, you can then request the current status of the conversation according to this HaRe model:

```
moba_hare.get_status()
```

You can also request this status at each point in the conversation so far:

```
moba_hare.get_status_history()
```

If you want to reuse this HaRe model for another conversation, make sure to create a new conversation before you start adding utterances:

```
moba_hare.start_conversation(conversation_id='second_convo')
```

You can switch between conversations that are currently active if needed:

```
moba_hare.switch_conversation(conversation_id='example_convo')
```

You can list the currently active conversations like this:

```
moba_hare.all_conversation_ids
```

### Evaluating

If you have a labeled dataset (that is: for each conversation an indication which participants are considered toxic), HaRe can calculate to what extent its judgments match the labels. A label can range from the default 0 (not toxic at all) to 1 (maximally toxic). Let's label speaker `c`: 

```
moba_hare.label_speaker('c',0.9)
```

There are several evaluation metrics, depending on what is important to you (detecting ALL harassment, detecting harassment quickly, no false positives, etc):

```
moba_hare.calculate_accuracy()
```

These metrics are calculated on the basis on all conversations the HaRe object is aware of that have at least 1 labeled participant. If you want to exclude a label from evaluation, simply add it to the `conversations_excluded_for_evaluation` list:

```
moba_hare.conversations_excluded_for_evaluation = ['example_convo']
```

### Training

At some point, you might want to do some training yourself. This can for example be the case because you are applying HaRe in another domain than the pretrained models, and harassment looks slightly different there, or because you even want to detect something different than harassment. Whatever your goals are, it is probably most effective to repurpose the existing HaRe models ('transfer learning'). 

To achieve this, simply load the pretrained model that best matches your goal, add some conversations and label them, like we have done above. If you want to exclude conversations from training, add them to the `conversations_excluded_for_training` list:

```
moba_hare.conversations_excluded_for_training = ['']
```

# Todo

Maybe not mention every command here, this is not the docs.
