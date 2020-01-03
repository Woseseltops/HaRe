Using neural networks to detect online harassment

Digital harassment is a problem in many corners of the internet. According to a 2016 report '47% of internet users have experienced online harassment or abuse [1], and 27% of all American internet users self-censor what they say online because they are afraid of being harassed. On a similar note, a survey by The Wikimedia Foundation (behind Wikipedia and other things) showed that 38% of the editors had encountered harassment, and over half them said this lowered their motivation to contribute in the future [2]. If we want safe and productive online platforms where users do not chase each other away, something needs to be done.

The best solution to this problem might be to use human moderators that read everything take action when somebody crosses a boundary, but this is not always feasable; for example, in popular online games hundreds of conversations are simultaneously happening all the time. At the same time, some online games are notorious for their toxic community. For example, the game League of Legends has been called "[x]". This is a typical conversation from the game:

[x] conversation

For this article, we will therefore use a dataset of conversations from this game and try to see if we can separate 'toxic' players from 'normal' players automatically. Let's take 10 conversations where 1 person misbehaves as an example, and see if we can pinpoint this 1 player, preferably early in the conversation. A first approach for an automated detector might be to use a simple list of bad words like 'fuck','suck', 'noob' and 'fag', and label a player as toxic if s/he uses it more often than a particular threshold. Below, you can slide through a conversation and see how detectors with thresholds of 1, 2, 3 and 5 bad words perform.

[first interaction]

[As you can see, the detector with the low threshold detects all toxic players already halfway during the game, but has lots of false positives]. [Another thing you might have noticed is that the average toxic player speaks a lot more than the other players... this is also something that is not picked up with a simple word list based approach.]

A better solution might be to use machine learning: we give thousands of examples of conversations with toxic players to a training algorithm and ask it to figure out how to recognize harassment by itself. The most successful algorithms in tasks like this these days are so-called neural networks. While even experts have trouble fully understanding why exactly they are so successful, there are some techniques to look under the hood and see what the network has learned. For example, you can put all the words a network has learned something about in a 3D space in such a way that words that are (according to the network) closer together are also closer in meaning.

[3d embeddings]

[We see that...]

Another thing we can look at is what the individual *neurons* do; you can think of a neuron as an individual worker that during the training phase tries to find a simple meaningful task for itself. A neural network is basically a collection of these workers, all doing simple but different tasks. What really sets a neural network apart from a simple word list based detector is that these workers are organized in *layers*. Neurons in the lower layers typically pick up a small concrete task, like recognizing particular words, while the higher layers do something increasingly more abstract, like monitoring the conversation on a higher level.

This is exactly what we see in our case. In the interactive visualization below, you can see where in the conversation which neurons activate.

[neuron vis]

We see that the neurons at the lower level have learned to activate on 1 or more words. [example] . The neurons at the higher levels, on the other hand, activate on such words but then slowly fade out, as if encountering such a word makes them more suspicious for some time.

The big question of course is whether a harassment detector using a neural network instead of word list performs better. Like with the word lists, there is a threshold we have to define beforehand, but this time it's not the number of bad words, but the 'confidence level': a number between 0 and 1 indicating how sure the network is a particular player is toxic. In the visualization below you can see the word list detector we used above (up to you which threshold to use), and three neural network based detectors, all using another threshold.

[xxx]

As you can see... [x]

Besides these technical challenges, there are a number of ethical questions too... do we only want to use this technique to study the toxicity within a community, or do we really want to put it in production and monitor conversations in real time? And if so, what does it mean for a person or a whole community have a real time watch dog robot, always looking over your shoulder? What should be done when it detects somebody? Should s/he be notified, warned, muted, banned? Related to that, the former director of Riot Games' Player Behavior Unit attributes most toxicity to 'the average person just having a bad day'... Is labeling a whole person as toxix or non-toxic not too simplistic?

 

[1]  https://www.datasociety.net/pubs/oh/Online_Harassment_2016.pdf
[2]  https://en.wikipedia.org/wiki/Wikipedia:Wikipedians#Number_of_editors
