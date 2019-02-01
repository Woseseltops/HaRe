from sys import argv
from collections import Counter
from numpy import array, asarray, zeros

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score

from tensorflow.python.keras.preprocessing import sequence, text
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Embedding, Dropout, GRU ,Dense, Bidirectional, GlobalMaxPool1D
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

    #Assumes balances =< 0.5

    counter = Counter(target)
    frequencies = counter.most_common()
    largest_class_label, largest_class_frequency = frequencies[0]
    smallest_class_label, smallest_class_frequency = frequencies[-1]

    desired_frequencies = {0: counter[0], 1: balance*(counter[0]/(1-balance))}

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
                print('break')
                break

    print(desired_frequencies,nr_of_labels_in_balanced_set, largest_class_label, smallest_class_label)

    return balanced_data, balanced_target

def preprocess_string(s,replace_apostrophes=True):

    APOSTROPHE_REPLACEMENTS = {'you\'re':'you \'re',
                               'i\'m':'i \'m',
                               'don\'t': 'do n\'t',
                               'it\'s': 'it \'s',
                               'that\'s': 'that \'s',
                               'can\'t': 'can n\'t',
                               'didn\'t': 'did n\'t',
                               }

    WORD_REPLACEMENTS = {'linebreak':'newline',
                         'lmao': 'haha',
                         'noobs': 'newbies',
                         'rofl': 'haha',
                         'fking': 'fucking',
                         'fcking': 'fucking',
                         }
    HERO_NAMES = ['teemo','nasus','ahri','udyr','ryze','kayle','rengar','shaco','aatrox','zyra','taric','trynd','amumu']

    s = s.lower().strip()

    for word, replacement in WORD_REPLACEMENTS.items():
        s = s.replace(word,replacement)

    if replace_apostrophes:
        for word, replacement in APOSTROPHE_REPLACEMENTS_REPLACEMENTS.items():
            s = s.replace(word,replacement)

    for hero in HERO_NAMES:
        s = s.replace(hero,'hero')

    return s

#==== Parameters =====

#Import data
DATA_FOLDER = '../datasets/LoL/'
CLASS_NAMES = ['nontoxic','toxic']
SAMPLES_PER_CLASS = 100000 #12500
TRAIN_BALANCE = 0.5
TEST_BALANCE = 0.5

#Vectorization settings
NUMBER_OF_FEATURES = 20000
MAX_SEQUENCE_LENGTH = 500

#Embedding settings
USE_PRETRAINED_EMBEDDINGS = True
CALCULATE_EMBEDDING_MATCH = False
EMBEDDING_FEATURES = 300
EMBEDDING_TRAINING_SIZE = 42
EMBEDDING_LOCATION = '/vol/bigdata/word_embeddings/glove/glove.'+str(EMBEDDING_TRAINING_SIZE)+'B.'+str(EMBEDDING_FEATURES)+'d.txt'

#Neural net settings
DROPOUT_RATE = 0.2
OUTPUT_UNITS = 1
OUTPUT_ACTIVATION = 'sigmoid'

LEARNING_RATE = 1e-3
EPOCHS = 20
BATCH_SIZE = 512

DROPOUT_LAYERS = 0

texts = []
target = []

#Interpret any arguments
for n, arg in enumerate(argv):

    if arg == 'train_balance':
        TRAIN_BALANCE = float(argv[n+1])
    elif arg == 'test_balance':
        TEST_BALANCE = float(argv[n+1])
    elif arg == 'embedding_features':
        EMBEDDING_FEATURES = int(argv[n+1])
    elif arg == 'embedding_training_size':
        EMBEDDING_TRAINING_SIZE = int(argv[n+1])
    elif arg == 'samples_per_class':
        SAMPLES_PER_CLASS = int(argv[n+1])
    elif arg == 'dropout_layers':
        DROPOUT_LAYERS = int(argv[n+1])

EMBEDDING_LOCATION = '/vol/bigdata/word_embeddings/glove/glove.'+str(EMBEDDING_TRAINING_SIZE)+'B.'+str(EMBEDDING_FEATURES)+'d.txt'

print('loading data')
for class_index, classname in enumerate(CLASS_NAMES):

    for n, line in enumerate(open(DATA_FOLDER+classname+'.txt')):

        texts.append(preprocess_string(line,False))
        target.append(class_index)

        if n > SAMPLES_PER_CLASS:
            break

print('* loaded',len(texts),'texts, balance',sum(target)/len(target))

train_texts, test_texts, train_target, test_target = train_test_split(texts, target, test_size = 0.1, random_state=1,
                                                                      stratify=target)

train_texts, train_target = set_dataset_balance(train_texts,train_target,TRAIN_BALANCE)
test_texts, test_target = set_dataset_balance(test_texts,test_target,TEST_BALANCE)

print('* train',len(train_texts),'texts, balance',sum(train_target)/len(train_target))
print('* test',len(test_texts),'texts, balance',sum(test_target)/len(test_target))

print('vectorizing texts')
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

if CALCULATE_EMBEDDING_MATCH:
    print('calculating word embedding vocabulary match')
    inverse_word_index = {v: k for k, v in word_index.items()}
    word_frequency_in_vocabulary = Counter()
    word_frequency_out_of_vocabulary = Counter()

    for train_vector in train_vectors:
        for index_of_current_word in train_vector:

            if index_of_current_word == 0:
                continue

            current_word = inverse_word_index[index_of_current_word]

            if embeddings_index.get(current_word) is not None:
               word_frequency_in_vocabulary[current_word] += 1
            else:
                word_frequency_out_of_vocabulary[current_word] += 1

    print('* in vocab',word_frequency_in_vocabulary.most_common(50))
    print('* out of vocab',word_frequency_out_of_vocabulary.most_common(50))
    print('* mismatch',sum(word_frequency_out_of_vocabulary.values())/(sum(word_frequency_out_of_vocabulary.values())+sum(word_frequency_in_vocabulary.values())))

print('building the model')
model = Sequential()

if USE_PRETRAINED_EMBEDDINGS:
    model.add(Embedding(input_dim=len(word_index)+1,
                       output_dim=EMBEDDING_FEATURES,
                       input_length=train_vectors.shape[1],
                       weights=[embedding_matrix],
                       trainable=False))
else:
    model.add(Embedding(len(word_index)+1,200))

model.add(Bidirectional(GRU(16, activation='tanh', return_sequences=True)))

if DROPOUT_LAYERS > 0:
    model.add(Dropout(0.15))

model.add(Bidirectional(GRU(16, activation='tanh', return_sequences=True)))

model.add(GlobalMaxPool1D())

if DROPOUT_LAYERS > 1:
    model.add(Dropout(0.15))

model.add(Dense(256))
model.add(Dense(256))

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
    verbose=1,  # Logs once per epoch.
    batch_size=BATCH_SIZE)

for score in zip(history.history['val_acc'],history.history['val_loss'],history.history['val_precision'],history.history['val_recall']):
    print('\t'.join([str(s) for s in score]))

# ================ Interpret the results ======================
# RESULT_DIR = 'error_analysis/'
#
# results = [x[0] for x in model.predict_proba(test_vectors)]
#
# for result,true,text in zip(results,test_target,test_texts):
#     open(RESULT_DIR+str(result)+'_'+str(true)+'.txt','w').write(text)

#print('roc_auc',roc_auc_score(test_target,results))