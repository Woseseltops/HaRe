from os import listdir
from collections import defaultdict
from numpy import array, asarray, zeros
from sklearn.model_selection import train_test_split
from tensorflow.python.keras.preprocessing import sequence, text
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Embedding, Dropout, SeparableConv1D, MaxPooling1D, GlobalAveragePooling1D,Dense
from tensorflow.keras.optimizers import Adam

def sequence_vectorize(train_texts, val_texts,number_of_features,max_sequence_length):

    # Create vocabulary with training texts.
    tokenizer = text.Tokenizer(num_words=number_of_features)
    tokenizer.fit_on_texts(train_texts)

    # Vectorize training and validation texts.
    x_train = tokenizer.texts_to_sequences(train_texts)
    x_val = tokenizer.texts_to_sequences(val_texts)

    # Get max sequence length.
    max_length = len(max(x_train, key=len))
    if max_length > max_sequence_length:
        max_length = max_sequence_length

    # Fix sequence length to max value. Sequences shorter than the length are
    # padded in the beginning and sequences longer are truncated
    # at the beginning.
    x_train = sequence.pad_sequences(x_train, maxlen=max_length)
    x_val = sequence.pad_sequences(x_val, maxlen=max_length)
    return x_train, x_val, tokenizer.word_index

#==== Parameters =====

#Import data
DATA_FOLDER = '../datasets/LoL/'
CLASS_NAMES = ['nontoxic','toxic']
DATA_LIMIT = 4000

#Vectorization settings
NUMBER_OF_FEATURES = 20000
MAX_SEQUENCE_LENGTH = 500

#Embedding settings
EMBEDDING_LOCATION = '/vol/bigdata/datasets/glove/glove.6B.50d.txt'
EMBEDDING_FEATURES = 50

#Neural net settings
BLOCKS = 3
DROPOUT_RATE = 0.2
KERNEL_SIZE = 30
FILTERS = 30
POOL_SIZE = 16
OUTPUT_UNITS = 1
OUTPUT_ACTIVATION = 'sigmoid'

LEARNING_RATE = 1e-3
EPOCHS = 1000
BATCH_SIZE = 512

texts = []
target = []

print('loading data')
for class_index, classname in enumerate(CLASS_NAMES):

    foldername = DATA_FOLDER+classname+'/'

    for text_index, filename in enumerate(listdir(foldername)):
        texts.append(open(foldername+filename).read())
        target.append(class_index)

        if text_index > DATA_LIMIT:
            break

train_texts, test_texts, train_target, test_target = train_test_split(texts, target, test_size = 0.1, random_state=1,
                                                                      stratify=target)
train_vectors, test_vectors, word_index = sequence_vectorize(train_texts,test_texts,NUMBER_OF_FEATURES,MAX_SEQUENCE_LENGTH)

print('loading embedding')
embeddings_index = {}
for line in open(EMBEDDING_LOCATION):
    values = line.split()
    word = values[0]
    coefs = asarray(values[1:], dtype='float32')
    embeddings_index[word] = coefs

print('creating embedding matrix based on our data')
embedding_matrix = zeros((len(word_index) + 1, EMBEDDING_FEATURES))
for word, i in word_index.items():
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        embedding_matrix[i] = embedding_vector

print('building the model')
model = Sequential()
model.add(Embedding(input_dim=len(word_index)+1,
                    output_dim=EMBEDDING_FEATURES,
                    input_length=train_vectors.shape[1],
                    weights=[embedding_matrix],
                    trainable=True))

for _ in range(BLOCKS - 1):
    model.add(Dropout(rate=DROPOUT_RATE))
    model.add(SeparableConv1D(filters=FILTERS,
                              kernel_size=KERNEL_SIZE,
                              activation='relu',
                              bias_initializer='random_uniform',
                              depthwise_initializer='random_uniform',
                              padding='same'))
    model.add(SeparableConv1D(filters=FILTERS,
                              kernel_size=KERNEL_SIZE,
                              activation='relu',
                              bias_initializer='random_uniform',
                              depthwise_initializer='random_uniform',
                              padding='same'))
    model.add(MaxPooling1D(pool_size=POOL_SIZE))

model.add(SeparableConv1D(filters=FILTERS * 2,
                          kernel_size=KERNEL_SIZE,
                          activation='relu',
                          bias_initializer='random_uniform',
                          depthwise_initializer='random_uniform',
                          padding='same'))
model.add(SeparableConv1D(filters=FILTERS * 2,
                          kernel_size=KERNEL_SIZE,
                          activation='relu',
                          bias_initializer='random_uniform',
                          depthwise_initializer='random_uniform',
                          padding='same'))

model.add(GlobalAveragePooling1D())
model.add(Dropout(rate=DROPOUT_RATE))
model.add(Dense(OUTPUT_UNITS, activation=OUTPUT_ACTIVATION))

print('compiling the model')
optimizer = Adam(lr=LEARNING_RATE)
model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['acc'])

print('training the model')
history = model.fit(
    train_vectors,
    train_target,
    epochs=EPOCHS,
    validation_data=(test_vectors, test_target),
    verbose=2,  # Logs once per epoch.
    batch_size=BATCH_SIZE)

print(history)