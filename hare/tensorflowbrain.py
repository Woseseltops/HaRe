from typing import List, Dict, Tuple, Optional, Any
from os import mkdir
from re import split
from collections import Counter
from numpy import array # type: ignore
from hare.brain import AbstractBrain, UntrainedBrainError
from hare.embedding import load_embedding_dictionary, create_embedding_matrix_for_vocabulary
from hare.downsample import downsample

try:
    from tensorflow.python.framework.ops import Tensor  # type: ignore
    from tensorflow.python.keras.models import Sequential # type: ignore
    from tensorflow.python.keras.preprocessing import sequence, text  # type: ignore
except ImportError:
    pass

class TensorFlowBrain(AbstractBrain):

    def __init__(self) -> None:

        super().__init__()

        self.dependencies = ['tensorflow']
        self.brain_type : str = 'TensorFlow'

        self.embedding_location : str = ''

        self.include_casing_information = False
        self.bidirectional = True

        self.learning_rate : float = 1e-3
        self.learning_epochs : int = 3
        self.learning_batch_size : int = 512

        self.tokenizer: Optional[text.Tokenizer] = None
        self.model : Optional[Sequential] = None

        self._max_sequence_length : int = 0

    def vectorize_texts(self,texts : List[str]) -> array:

        if self.tokenizer is not None:
            vectorized_texts : List[List[int]] = self.tokenizer.texts_to_sequences(texts)
        else:
            raise UntrainedBrainError

        padded_vectors : array = sequence.pad_sequences(vectorized_texts, maxlen=self._max_sequence_length)

        return padded_vectors

    def texts_to_casing_information(self,texts : List[str]) -> array:

        casing_vectors : List[List[float]] = []

        for text in texts:

            current_vector : List[List[int]] = []

            for word in split(r' |!|"|#|\$|%|&|\(|\)|\*|\+|,|-|\.|/|:|;|<|=|>|\?|@|\[|\|\]|\^|_|`|{|\||}|~|\t|\n',text):
                try:
                    current_vector.append([sum([1 for letter in word if letter.isupper()])/len(word)])
                except ZeroDivisionError:
                    current_vector.append([0])

            casing_vectors.append(current_vector)

        padded_vectors : array = sequence.pad_sequences(casing_vectors, maxlen=self._max_sequence_length,dtype='float32')

        return padded_vectors

    def classify(self,text : str) -> float:

        vectorized_text : str = self.vectorize_texts([text])

        if self.model is not None:
            return float(self.model.predict_proba(vectorized_text)[0])
        else:
            raise UntrainedBrainError

    def classify_multiple(self,texts : List[str]) -> List[float]:

        #Go from text to one or more inputs for the model
        vectorized_texts: array = self.vectorize_texts(texts)

        if self.include_casing_information:
            casing_information : array = self.texts_to_casing_information(texts)
            inp = [vectorized_texts,casing_information]
        else:
            inp = vectorized_texts

        #Do the actual predictions
        if self.model is not None:

            return [float(i[0]) for i in self.model.predict(inp)]

            #This was what we used before the functional API
            # return [float(i[0]) for i in self.model.predict_proba(vectorized_texts)]
        else:
            raise UntrainedBrainError

    def determine_impact_of_words(self,text : str) -> List[Tuple[str,float]]:

        words : List[str] = text.split()
        all_text_to_classify : List[str] = [text]

        for i in range(len(words)):
            words_for_this_iteration : List[str] = words[:i]+['[UNK]']+words[i+1:]
            all_text_to_classify.append(' '.join(words_for_this_iteration))

        scores : List[float] = self.classify_multiple(all_text_to_classify)
        impacts : List[Tuple[str,float]] = [(word,scores[0]-score) for word,score in zip(words,scores[1:])]

        return impacts

    def precision(self, y_true, y_pred) -> Tensor:
        '''Calculates the precision, a metric for multi-label classification of
        how many selected items are relevant.
        '''

        from tensorflow.keras import backend #type: ignore

        true_positives : Tensor = backend.sum(backend.round(backend.clip(y_true * y_pred, 0, 1)))
        predicted_positives : Tensor = backend.sum(backend.round(backend.clip(y_pred, 0, 1)))
        precision : Tensor = true_positives / (predicted_positives + backend.epsilon())
        return precision

    def recall(self, y_true, y_pred) -> Tensor:
        '''Calculates the recall, a metric for multi-label classification of
        how many relevant items are selected.
        '''

        from tensorflow.keras import backend #type: ignore

        true_positives : Tensor = backend.sum(backend.round(backend.clip(y_true * y_pred, 0, 1)))
        possible_positives : Tensor= backend.sum(backend.round(backend.clip(y_true, 0, 1)))
        recall : Tensor = true_positives / (possible_positives + backend.epsilon())
        return recall


    def save(self,location : str):

        import json
        import pickle
        from tensorflow.keras.models import save_model #type: ignore

        if location[-1] != '/':
            location += '/'

        try:
            mkdir(location)
        except FileExistsError:
            pass

        #Save metadata
        metadata : Dict[str,Any] = {'brainType':self.brain_type,
                                    'maxSequenceLength':self._max_sequence_length,
                                    'includeCasingInformation':self.include_casing_information,
                                    'bidirectional':self.bidirectional}
        json.dump(metadata,open(location+'metadata.json','w'))

        #Save tokenizer
        pickle.dump(self.tokenizer,open(location+'tokenizer.pickle','wb'))

        #Save model
        save_model(self.model,location+'model')

    def load(self,location : str):

        import json
        import pickle
        from tensorflow.keras.models import load_model #type: ignore

        from warnings import filterwarnings
        filterwarnings('ignore')

        if location[-1] != '/':
            location += '/'

        #Load metadata
        self._max_sequence_length = json.load(open(location+'metadata.json'))['maxSequenceLength']

        #Load tokenizer
        self.tokenizer = pickle.load(open(location+'tokenizer.pickle','rb'))

        #Load model
        self.model = load_model(open(location+'model','rb'))

    def get_embeddings(self,limit : int = 1000) -> Tuple[List[str],List[List[float]]]:

        if self.tokenizer is not None and self.model is not None:
            return list(self.tokenizer.word_index.keys())[:limit], self.model.layers[0].get_weights()[0][:limit]
        else:
            raise UntrainedBrainError

    def visualize_neuron_specializations(self,layer_index : int, texts : List[str], list_length : int = 5):

        from tensorflow.keras.models import Model

        VISUALIZE : bool = False

        if self.model is not None:
            intermediate_output_model : Model = Model(inputs=self.model.input, outputs=self.model.layers[layer_index].output)
        else:
            raise UntrainedBrainError

        word_scores_per_neuron : List[List[Tuple[str,float]]] = []

        #For now only processes the first text
        for text in self.vectorize_texts(texts):

            text = array([text])

            for word_index, activations in zip(text[0], intermediate_output_model.predict(text)[0]):

                try:
                    if self.tokenizer is not None:
                        current_word : str = self.tokenizer.index_word[word_index]
                    else:
                        raise UntrainedBrainError
                except KeyError:
                    continue

                for neuron_index, neuron_activation in enumerate(activations):

                    if len(word_scores_per_neuron) <= neuron_index:
                        word_scores_per_neuron.append([])

                    word_scores_per_neuron[neuron_index].append((current_word,neuron_activation))

        if VISUALIZE: #This should be moved elsewhere

            for neuron_scores in word_scores_per_neuron:

                sorted_words : List[Tuple[str,float]] = sorted(neuron_scores,key=lambda x:x[1])

                lowest_words : List[str] = []
                highest_words: List[str] = []

                for word,activation in sorted_words:
                    lowest_words.append(word)

                    if len(set(lowest_words)) > list_length:
                        break

                for word, activation in reversed(sorted_words):
                    highest_words.append(word)

                    if len(set(highest_words)) > list_length:
                        break

                low_word_str = ''
                high_word_str = ''

                for word in set(lowest_words):
                    low_word_str += word + ' (' + str(lowest_words.count(word)) + ')\t'

                for word in set(highest_words):
                    high_word_str += word + ' (' + str(highest_words.count(word)) + ')\t'

                print(low_word_str+'\t-\t'+high_word_str)

        return word_scores_per_neuron

class BiGruBrain(TensorFlowBrain):

    def __init__(self) -> None:

        super().__init__()
        self.brain_type = 'BiGru'

    def train(self, texts : List[str],target : List[int]) -> None:

        from tensorflow.python.keras.models import Model #type: ignore
        from tensorflow.python.keras.layers import Input, Embedding, GRU, Dense, Bidirectional, GlobalMaxPool1D,concatenate #type: ignore
        from tensorflow.keras.optimizers import Adam #type: ignore
        from tensorflow.keras.callbacks import History #type: ignore

        if self.downsampling:
            texts, target = downsample(texts,target,self.downsampling_ratio)

        if self.verbose:
            print('1. Vectorizing texts')

        NUMBER_OF_FEATURES : int = 20000
        self.tokenizer = text.Tokenizer(num_words=NUMBER_OF_FEATURES)
        self.tokenizer.fit_on_texts(texts)
        vocabulary : Dict[str,int] = self.tokenizer.word_index

        if self._max_sequence_length == 0:
            self._max_sequence_length = len(max(texts, key=len))

        vectorized_texts : array = self.vectorize_texts(texts)

        if self.include_casing_information:
            casing_information : array = self.texts_to_casing_information(texts)

        if self.embedding_location == '':
            if self.verbose:
                print('2. Skip (no embeddings)')
                print('3. Skip (no embeddings)')
        else:
            if self.verbose:
                print('2. Loading word embeddings')

            embedding_dictionary : Dict[str,List[float]] = load_embedding_dictionary(self.embedding_location)
            nr_of_embedding_features: int = len(list(embedding_dictionary.values())[1])  # Check how many values we have for the first word

            if self.verbose:
                print('3. Creating embedding matrix')

            embedding_matrix : array = create_embedding_matrix_for_vocabulary(embedding_dictionary,vocabulary)

        if self.verbose:
            print('4. Building up model')

        #Define a simple BiGru model with a pretrained embedding layer
        word_input : Input = Input(shape=(self._max_sequence_length,))

        if self.embedding_location == '':
            #Add an empty embedding layer if we have no pretrained embeddings
            EMPTY_EMBEDDING_LAYER_SIZE : int = 300
            layers = Embedding(len(vocabulary)+1,EMPTY_EMBEDDING_LAYER_SIZE)(word_input)

        else:
            layers = Embedding(input_dim=len(vocabulary)+1,
                               output_dim=nr_of_embedding_features,
                               input_length=vectorized_texts.shape[1],
                               weights=[embedding_matrix],
                               trainable=False)(word_input)

        #Add a separate 'entrance' for the casing information
        if self.include_casing_information:
            word_model : Model = Model(inputs=word_input, outputs=layers)

            casing_input : Input = Input(shape=(self._max_sequence_length,1))

            casing_model : Model = Model(inputs=casing_input, outputs=casing_input)
            layers = concatenate([word_model.output, casing_model.output])

        if self.bidirectional:
            layers = Bidirectional(GRU(16, activation='tanh', return_sequences=True))(layers)
            layers = Bidirectional(GRU(16, activation='tanh', return_sequences=True))(layers)
        else:
            layers = GRU(16, activation='tanh', return_sequences=True)(layers)
            layers = GRU(16, activation='tanh', return_sequences=True)(layers)

        layers = GlobalMaxPool1D()(layers)

        layers = Dense(256)(layers)
        layers = Dense(256)(layers)

        layers = Dense(1, activation='sigmoid')(layers)

        if self.include_casing_information:
            model : Model  = Model([word_model.input,casing_model.input], layers)
        else:
            model : Model = Model(word_input, layers)

        #Compile the model
        optimizer : Adam = Adam(lr=self.learning_rate)
        model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['acc'])

        if self.verbose:
            print('5. training the model')

        if self.include_casing_information:

            input = [vectorized_texts,casing_information]

        else:

            input = vectorized_texts

        history : History = model.fit(input,
            target,
            epochs=self.learning_epochs,
            #validation_data=(test_vectors, test_target),
            verbose=1,  # Logs once per epoch.
            batch_size=self.learning_batch_size)

        self.model = model

class LSTMBrain(TensorFlowBrain):

    def __init__(self) -> None:

        super().__init__()
        self.brain_type = 'LSTM'

    def train(self, texts : List[str],target : List[int]) -> None:

        from tensorflow.python.keras.models import Sequential #type: ignore
        from tensorflow.python.keras.layers import Embedding, Dense, LSTM, GlobalMaxPool1D #type: ignore
        from tensorflow.keras.optimizers import Adam #type: ignore
        from tensorflow.keras.callbacks import History #type: ignore

        if self.downsampling:
            texts, target = downsample(texts,target,self.downsampling_ratio)

        if self.verbose:
            print('1. Vectorizing texts')

        NUMBER_OF_FEATURES : int = 20000
        self.tokenizer = text.Tokenizer(num_words=NUMBER_OF_FEATURES)
        self.tokenizer.fit_on_texts(texts)
        vocabulary : Dict[str,int] = self.tokenizer.word_index

        if self._max_sequence_length == 0:
            self._max_sequence_length = len(max(texts, key=len))

        vectorized_texts : array = self.vectorize_texts(texts)

        if self.embedding_location == '':
            if self.verbose:
                print('2. Skip (no embeddings)')
                print('3. Skip (no embeddings)')
        else:
            if self.verbose:
                print('2. Loading word embeddings')

            embedding_dictionary : Dict[str,List[float]] = load_embedding_dictionary(self.embedding_location)
            nr_of_embedding_features: int = len(list(embedding_dictionary.values())[1])  # Check how many values we have for the first word

            if self.verbose:
                print('3. Creating embedding matrix')

            embedding_matrix : array = create_embedding_matrix_for_vocabulary(embedding_dictionary,vocabulary)

        if self.verbose:
            print('4. Building up model')

        #Define a simple LSTM model with a pretrained embedding layer
        model : Sequential = Sequential()

        if self.embedding_location == '':
            #Add an empty embedding layer if we have no pretrained embeddings
            EMPTY_EMBEDDING_LAYER_SIZE : int = 300
            model.add(Embedding(len(vocabulary)+1,EMPTY_EMBEDDING_LAYER_SIZE))

        else:
            model.add(Embedding(input_dim=len(vocabulary)+1,
                               output_dim=nr_of_embedding_features,
                               input_length=vectorized_texts.shape[1],
                               weights=[embedding_matrix],
                               trainable=False))

        model.add(LSTM(16, return_sequences=True))
        model.add(LSTM(16, return_sequences=True))
        model.add(LSTM(16, return_sequences=True))
        model.add(GlobalMaxPool1D())

        model.add(Dense(256))
        model.add(Dense(256))

        model.add(Dense(1, activation='sigmoid'))

        #Compile the model
        optimizer : Adam = Adam(lr=self.learning_rate)
        model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['acc'])

        if self.verbose:
            print('5. training the model')

        history : History = model.fit(vectorized_texts,
            target,
            epochs=self.learning_epochs,
            #validation_data=(test_vectors, test_target),
            verbose=1,  # Logs once per epoch.
            batch_size=self.learning_batch_size)

        self.model = model