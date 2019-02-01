from os import listdir
from collections import Counter
from numpy import array, asarray, zeros

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score

from tensorflow.python.keras.preprocessing import sequence, text
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Embedding, Dropout, SeparableConv1D, MaxPooling1D, GlobalAveragePooling1D,Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import backend

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

def precision(y_true, y_pred):
    '''Calculates the precision, a metric for multi-label classification of
    how many selected items are relevant.
    '''
    true_positives = backend.sum(backend.round(backend.clip(y_true * y_pred, 0, 1)))
    predicted_positives = backend.sum(backend.round(backend.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + backend.epsilon())
    return precision


def recall(y_true, y_pred):
    '''Calculates the recall, a metric for multi-label classification of
    how many relevant items are selected.
    '''
    true_positives = backend.sum(backend.round(backend.clip(y_true * y_pred, 0, 1)))
    possible_positives = backend.sum(backend.round(backend.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + backend.epsilon())
    return recall

def set_dataset_balance(data,target,balance):

    #Assumes balances >= 0.5

    frequencies = Counter(target).most_common()
    largest_class_label, largest_class_frequency = frequencies[0]
    smallest_class_label, smallest_class_frequency = frequencies[-1]

    desired_frequencies = {smallest_class_label:smallest_class_frequency,
                           largest_class_label: round((smallest_class_frequency/balance)*(1-balance))}

    balanced_data = []
    balanced_target = []

    nr_of_labels_in_balanced_set = {smallest_class_label: 0 , largest_class_label: 0}

    for item, true_class in zip(data,target):

        #If this is something we still needed, add it
        if nr_of_labels_in_balanced_set[true_class] < desired_frequencies[true_class]:
            balanced_data.append(item)
            balanced_target.append(true_class)
            nr_of_labels_in_balanced_set[true_class] += 1

            #Check if we're done
            if nr_of_labels_in_balanced_set[smallest_class_label] == desired_frequencies[smallest_class_label] and \
                nr_of_labels_in_balanced_set[largest_class_label] == desired_frequencies[largest_class_label]:
                break

    return balanced_data, balanced_target

#==== Parameters =====

#Import data
DATA_FOLDER = '../datasets/LoL/'
CLASS_NAMES = ['nontoxic','toxic']
DATA_LIMIT = 30000
DOWNSAMPLING_RATE = 0.5

#Vectorization settings
NUMBER_OF_FEATURES = 20000
MAX_SEQUENCE_LENGTH = 500

#Embedding settings
EMBEDDING_FEATURES = 50
EMBEDDING_LOCATION = '/vol/bigdata/datasets/glove/glove.6B.'+str(EMBEDDING_FEATURES)+'d.txt'

#Neural net settings
BLOCKS = 3
DROPOUT_RATE = 0.2
KERNEL_SIZE = 30
FILTERS = 30
POOL_SIZE = 3
OUTPUT_UNITS = 1
OUTPUT_ACTIVATION = 'sigmoid'

LEARNING_RATE = 1e-3
EPOCHS = 20
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

print('loaded',len(texts),'texts, balance',sum(target)/len(target))

train_texts, test_texts, train_target, test_target = train_test_split(texts, target, test_size = 0.1, random_state=1,
                                                                      stratify=target)

train_texts, train_target = set_dataset_balance(train_texts,train_target,DOWNSAMPLING_RATE)
test_texts, test_target = set_dataset_balance(test_texts,test_target,DOWNSAMPLING_RATE)

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

model.add(Dense(300))
model.add(Dense(300))

model.add(Dense(OUTPUT_UNITS, activation=OUTPUT_ACTIVATION))

print('compiling the model')
optimizer = Adam(lr=LEARNING_RATE)
model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['acc',precision,recall])

print('training the model')
history = model.fit(
    train_vectors,
    train_target,
    epochs=EPOCHS,
    validation_data=(test_vectors, test_target),
    verbose=2,  # Logs once per epoch.
    batch_size=BATCH_SIZE)

results = [x[0] for x in model.predict_proba(test_vectors)]

print('roc_auc',roc_auc_score(test_target,results))