# -*- coding: utf-8 -*-
"""NLP HW2 - PostRnn.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OuVLwldhT1rgA9RqF0TRWmRniicusHs6
"""

#===============================================================================
# Emily Chen (exc160630)
# CS 6320 Natural Language Processing
# Homework 2: Recurrent Neural Networks (RNNs)
# Goal: Design and implement a part-of-speech tagger (POST) using
#   a recurrent neural network. 
#===============================================================================
# install necessary packages using pip
!pip install keras numpy wget
!pip install np_utils

import tensorflow as tf
from tensorflow import keras
import pandas as pd
import numpy as np  # you may need this to convert lists to np arrays before returning them
import os
import io
import sys

from collections import defaultdict
from keras.utils.np_utils import to_categorical

# To incorpoate the training data
# Upload training zip file, then run this code to unzip.
!unzip train.zip

def load_corpus(path):

    # Check if the path is a directory.
    if not os.path.isdir(path):
        sys.exit("Input path is not a directory")
    
    # TODO: Your code goes here 
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 2000)

    num_files = 0
    num_sentences = 0
    total_tuplelist = []

    for filename in os.listdir(path):
      filename = os.path.join(path, filename)
      try:
        reader = io.open(filename)

        # Open the file, read corpus as input
        num_files += 1
        for line in reader:
          if not line.strip():
            continue
          else:
            tuplelist = []      # List of word-key pairings for a particular sentence

            # Convert the sentence into a list separated by whitespace
            linesplit = line.split() 

            # Split & pair into (word, key) tuples
            #print(linesplit)  ##
            for corpus_pair in linesplit:go
              temp_list = corpus_pair.split('/')
              temp_list[0] = temp_list[0].lower()
              tuplelist.append(tuple(temp_list))
            #print(tuplelist)  ##

            total_tuplelist.append(tuplelist)
            num_sentences += 1
    
      except IOError:
        sys.exit("Cannot read file")

    #print("There are " + str(num_files) + " files in the corpus.")
    #print("There are " + str(num_sentences) + " sentences in total.")

    #print("total_tuplelist")  ##
    #print(total_tuplelist[0:10])  ##

    return(total_tuplelist)

# test the function here:
path = "/content/modified_brown"
data = load_corpus(path)
#print(data[6])

# Creates the dataset with train_X (words) and train_y (tag).
def create_dataset(sentences):
    # Defines the relevant lists.
    train_X, train_y = list(), list()
    word_list, tag_list = [], []
    temp1, temp2 = [], []

    unique_words_tags = {"PAD": 0,
                         "NOUN": 1, 
                         "PRONOUN": 2, 
                         "VERB": 3, 
                         "ADJECTIVE": 4, 
                         "ADVERB": 5, 
                         "CONJUNCTION": 6, 
                         "PREPOSITION": 7, 
                         "DETERMINER": 8, 
                         "NUMBER": 9, 
                         "PUNCT":10, 
                         "X": 11, 
                         "NA": 12}
    identifier = 13

    # TODO: Your code goes here
    # Keep track of unique words, unique tokens
    for sentence in sentences:
      for corpus_pair in sentence:
        if corpus_pair[0] in unique_words_tags:
          continue
        else:
          unique_words_tags[corpus_pair[0]] = identifier
          identifier += 1

    #print(unique_words_tags)

    # Split dataset into a list of words and tags by identifier
    # train_X is a list of lists of words in a sentence as unique integer identifier
    # train_y list of lists of tags in a sentence as unique integer
    for sentence in sentences:
      temp1 = []
      temp2 = []
      for token_pair in sentence:
        temp1.append(unique_words_tags[token_pair[0]])
        temp2.append(unique_words_tags[token_pair[1]])
      train_X.append(temp1)
      train_y.append(temp2)
      

    return np.asarray(train_X), np.asarray(train_y), unique_words_tags

# Test the function here
# Call create_dataset()
train_X, train_y, unique_words_tags = create_dataset(data)
#print(train_X[0])
#print(train_y[0])
#print(len(unique_words_tags))

from keras.preprocessing.sequence import pad_sequences as pad

# Pad the sequences with 0s to the max length.
def pad_sequences(train_X, train_y):
    # Use MAX_LENGTH to record length of longest sequence 
    # TODO: Your code goes here

    MAX_LENGTH = 0
    for i in train_X:
      if len(train_X[i]) > MAX_LENGTH:
        MAX_LENGTH = len(train_X[i])

    # Pad_sequences()
    train_X = pad(train_X, padding='post')
    train_y = pad(train_y, padding='post')

    return train_X, train_y, MAX_LENGTH

# Test the function
train_X, train_y, MAX_LENGTH = pad_sequences(train_X, train_y)
train_X = np.asarray(train_X)
train_y = np.asarray(train_y)

#print(train_X[0])
#print(train_y[0])
#print(MAX_LENGTH)

from keras.models import Sequential
from keras.layers import InputLayer, Activation
from keras.layers import Dense, LSTM, InputLayer, Bidirectional, TimeDistributed, Embedding
from tensorflow.keras.optimizers import Adam

# Define the Keras model.
    # embedding
    # bidirectional LSTM
    # timedistributed dense
    # Activation('softmax')
    # model.compile(tf.keras.optimizers.Adam(), LossFunction)

def define_model(MAX_LENGTH, vocab_length):  
    
    # Define 'model' here
    model = keras.Sequential()
    
    # Add embedding layer
    model.add(keras.layers.Embedding(vocab_length, 128, input_length = MAX_LENGTH))

    # Add bidirectional LSTM layer
    model.add(keras.layers.Bidirectional(keras.layers.LSTM(256, return_sequences = True)))

    # Add timedistributed dense LSTM layer 
    # Softmax activation for categorical output
    model.add(keras.layers.TimeDistributed(keras.layers.Dense(12, activation='softmax')))
    
    print (model.summary())
    # Compiles model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    return model

# Call the function here
model = define_model(MAX_LENGTH, len(unique_words_tags) + 1)

# Returns the one-hot encoding of the sequence.
# Transform sequences of tags to sequences of One-Hot Encoded tags as this is what the fully connected layer outputs
def to_categorical(train_y, num_tags = 12):
    #TODO: Write code here
    one_hot = []
    temp = []
    new_train_y = []
  
    #print(train_y[0])

    for sentence in train_y:
      temp = []
      for id in sentence:
        one_hot = np.zeros((num_tags), dtype=int)   # [0 0 0 0 0 0 0 0 0 0 0 0]
        one_hot[id] = 1     # 1 -> [1 0 0 0 0 0 0 0 0 0 0 0]  # postreview, meant to do one_hot[id-1] = 1 ?
        temp.append(one_hot)

      new_train_y.append(temp)

    return np.asarray(new_train_y)
        

# Call the function as to_categorical(train_y, categories = len(tag2idx))
pd.set_option('display.max_colwidth',1000)
#print(train_y[0])
train_y = to_categorical(train_y, 12)
#print(train_y[0])

tf.config.run_functions_eagerly(True)

# Trains the model.
def train(model, train_X, train_y):

    # Fit the data into the Keras model, through 40 passes (epochs) using model.fit()
    # Set the batch size to 128, no. of iterations to 40 and validation split to 0.2.
    model.fit(train_X, train_y, batch_size = 128, epochs = 5, validation_split = 0.2)

    # Return the model.
    return model

# call function here
model = train(model, train_X, train_y)

tf.data.experimental.enable_debug_mode()

# Test a sentence using the given model.
#To evaluate the model, give a sentence i.e. list of words as input the model and predict its POS tags. 
def test(model, unique_words_tags, MAX_LENGTH, sentence):
    # TODO: Write your code here
    test_list = []
    taggers = []
    temp = []
    id = 0
    tag = ""

    if type(sentence) != list:
      sentence = sentence.split()
    #print(sentence)

    # Convert sentence into list of unique integers first
    for word in sentence:
      if word in unique_words_tags:
        test_list.append(unique_words_tags[word]) # identifier for word in the dictionary
      else:
        test_list.append(unique_words_tags["NA"])  # word N/A identifier
    #print(test_list)

    # Don't forget to pad
    N = MAX_LENGTH - len(test_list)
    test_list = np.pad(test_list, (0, N), 'constant')
    #print(test_list)

    # Perform inference on test data
    # Model outputs list of logits 
    #print("Prediction logits list")
    predictions = model.predict(test_list)
    #print(predictions)  # nan
    
    # Convert list of logits into probability
    for logit_list in predictions:  # Logit seq for each word 
      #print("logit")
      #print(logit_list)

      #print("probability")
      prediction = tf.nn.softmax(logit_list)
      #print(prediction)

      #print("max")
      #print(np.argmax(prediction))
      temp.append(np.argmax(prediction))

    #print("tagger values list")
    #print(temp)

    # Convert one-hot encoding list to list of identifiers (make reverse of to_categorical)
    # Convert list of identifiers to tags
    # List out keys and values separately to get key that mirrors value in dict
    key_list = list(unique_words_tags.keys())
    val_list = list(unique_words_tags.values())

    for x in temp:
      index = val_list.index(x)  
      tag = key_list[index]
      taggers.append(tag)

    return taggers[0:len(sentence)]


# For the first evaluation sentence.
testString1 = "the planet jupiter and its moons are in effect a mini solar system ."
# call test() to print tags
print(testString1)
print(test(model, unique_words_tags, MAX_LENGTH, testString1))

print("===================================================")

# For the second evaluation sentence.
testString2 = "computers process programs accurately ."
# call test() to print tags
print(testString2)
print(test(model, unique_words_tags, MAX_LENGTH, testString2))