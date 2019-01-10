from os import listdir
from collections import defaultdict
from numpy import array
from sklearn.model_selection import train_test_split
from tensorflow.python.keras.preprocessing import sequence, text
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Embedding

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


def load_embedding_from_disks(glove_filename, with_indexes=True):

    """
    Read a GloVe txt file. If `with_indexes=True`, we return a tuple of two dictionnaries
    `(word_to_index_dict, index_to_embedding_array)`, otherwise we return only a direct 
    `word_to_embedding_dict` dictionnary mapping from a string to a numpy array.
    """

    if with_indexes:
        word_to_index_dict = dict()
        index_to_embedding_array = []
    else:
        word_to_embedding_dict = dict()

    with open(glove_filename, 'r') as glove_file:
        for (i, line) in enumerate(glove_file):

            split = line.split(' ')

            word = split[0]

            representation = split[1:]
            representation = array(
                [float(val) for val in representation]
            )

            if with_indexes:
                word_to_index_dict[word] = i
                index_to_embedding_array.append(representation)
            else:
                word_to_embedding_dict[word] = representation

    _WORD_NOT_FOUND = [0.0] * len(representation)  # Empty representation for unknown words.
    if with_indexes:
        _LAST_INDEX = i + 1
        word_to_index_dict = defaultdict(lambda: _LAST_INDEX, word_to_index_dict)
        index_to_embedding_array = array(index_to_embedding_array + [_WORD_NOT_FOUND])
        return word_to_index_dict, index_to_embedding_array
    else:
        word_to_embedding_dict = defaultdict(lambda: _WORD_NOT_FOUND)
        return word_to_embedding_dict

#==== Parameters =====

#Import data
DATA_FOLDER = '../datasets/LoL/'
CLASS_NAMES = ['nontoxic','toxic']
DATA_LIMIT = 40

#Vectorization settings
NUMBER_OF_FEATURES = 20000
MAX_SEQUENCE_LENGTH = 500

#Embedding settings
EMBEDDING_LOCATION = '/vol/bigdata/datasets/glove/glove.6B.50d.txt'
EMBEDDING_FEATURES = 50

texts = []
target = []

# for class_index, classname in enumerate(CLASS_NAMES):
#
#     foldername = DATA_FOLDER+classname+'/'
#
#     for text_index, filename in enumerate(listdir(foldername)):
#         texts.append(open(foldername+filename).read())
#         target.append(class_index)
#
#         if text_index > DATA_LIMIT:
#             break
#
# train_texts, test_texts, train_target, test_target = train_test_split(texts, target, test_size = 0.1, random_state=1,
#                                                                       stratify=target)
# train_vectors, test_vectors, _ = sequence_vectorize(train_texts,test_texts,NUMBER_OF_FEATURES,MAX_SEQUENCE_LENGTH)
#

word_to_index_dict, index_to_embedding_array = load_embedding_from_disks(EMBEDDING_LOCATION,True)
print(word_to_index_dict)
print(index_to_embedding_array)

model = Sequential()
model.add(Embedding(input_dim=NUMBER_OF_FEATURES,
                    output_dim=EMBEDDING_FEATURES,
                    input_length=train_vectors.shape[1:],
                    weights=embedding_matrix,
                    trainable=True))