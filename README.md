# NLP Projects
The following is a list of my various natural language processing projects. 
Most of them were programmed by hand, without the usage of popular NLP libraries like NLTK, Textblob, or Polyglot.

At the moment, further documentation needs to be done for more thorough guides, and the datasets used have not yet been uploaded.
Please stay tuned for more developments!


## Bigram Language Model
Language model that predicts the likelihood of a set of words/sentence to occur in a text given a particular corpus.
This bigram N-Gram model approximates probability of the next word occuring based on previous (N-1) words and incorporates no smoothing and add-one smoothing versioning.

Colab link: https://colab.research.google.com/drive/18TBRHIf98riIppxosGB8dYVWhmjz0YSq?usp=sharing


## HMM Parts-of-Speech Tagger
Parts-of-Speech (POST) tagger that tags words in a sentence as "NOUN", "PRONOUN", "VERB", "ADJECTIVE", "ADVERB", "CONJUNCTION", "PREPOSITION", "DETERMINER", "NUMBER", "PUNCT" or "X". for other. This Hidden Markov Model (HMM) approximates the most likely tag by utilizing the Viterbi algorithm of calculating initial/emission/transmition probability tables.

Colab link: https://colab.research.google.com/drive/1jZLRXqjpg_waJyb34cXlAb0baxCoX-pW?usp=sharing


## RNN Parts-of-Speech Tagger
Same as the HMM POST Tagger, tags words in a sentence as "NOUN", "PRONOUN", "VERB", "ADJECTIVE", "ADVERB", "CONJUNCTION", "PREPOSITION", "DETERMINER", "NUMBER", "PUNCT" or "X". for other. However, this tagger was created using a Recurrent Neural Network (RNN) instead of an HMM. 
This RNN tags a word by training a Keras sequential nerual network to classify a word tag based on teaining data.

Colab link: https://colab.research.google.com/drive/1OuVLwldhT1rgA9RqF0TRWmRniicusHs6?usp=sharing


## Bi-LSTM Semantic Relation Classifier
Given a sentence and two tagged entities, the classifier determines a relation label to apply ("Cause-Effect(e1,e2)", "Cause-Effect(e2,e1)", "Component-Whole(e1,e2)", "Component-Whole(e2,e1)", "Entity-Destination(e1,e2)", "Entity-Destination(e2,e1)","Entity-Origin(e1,e2)", "Entity-Origin(e2,e1)", or "Other-Relation"). 
This Bi-LSTM model was created using Keras and minimized with Nesterov-accelerated Adaptive Moment Estimation (NAdam) loss function to classify two sentences with a relation label based on confidence. The model incorporates Bidirectional LSTM layers with dropout to improve classification performance and accuracy.

Colab link: https://colab.research.google.com/drive/16foHudxkUtJFqamVHYlxdku_JFwfY8xI?usp=sharing
