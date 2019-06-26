Detecting harassment as conversations develop

Intro
* We see many papers in this field approach the task as pure text classification. In a real life gaming context this is useless, because the conversations are rated by players themselves.
* The focus is less on rating individual comments (an individual swear word or insult does not indicate harassment per se), but on detecting *players* that consistently and knowingly harass team mates and/or opponents.
* This requires a different approach, where conversation participants are ...

* The amount of information we have on a single player grows during the conversation, allowing for better classification.
* Applying text classification to everything a participant has said after every turn in the conversation gives an estimate of the temperature of each participant so far.
* But you can also apply this idea at larger scale, to evaluate classifier during conversations.

Previous work
* Zhang 2018

Dataset
* Lol: longer conversations of short utterances
* Conversations gone awry?

Method
* HaRe
* BiGRU
* Our approach to classify beginning conversations is to make no difference

Results
* You need different thresholds at different points in the conversation, a 'sliding threshold'.
* You can select the optimathreshold per turn and plot this. It shows you need to increase the threshold over time
* How fast to increase the threshold during a conversation is not a given: it interacts with training size. The larger the training material, to slower you can turn up the threshold.
* Also with distribution ratio?

Discussion
* Less applicable to news sections

Conclusion