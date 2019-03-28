from typing import List, Dict, Optional, Any
from os import mkdir
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

class BiGruBrain(AbstractBrain):

    def __init__(self) -> None:

        super().__init__()

        self.dependencies = ['tensorflow']
        self.embedding_location : str = ''

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

    def classify(self,text : str) -> float:

        vectorized_text : str = self.vectorize_texts([text])

        if self.model is not None:
            return float(self.model.predict_proba(vectorized_text)[0])
        else:
            raise UntrainedBrainError

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

    def train(self, texts : List[str],target : List[int]) -> None:

        from tensorflow.python.keras.models import Sequential #type: ignore
        from tensorflow.python.keras.layers import Embedding, Dropout, GRU, Dense, Bidirectional, GlobalMaxPool1D #type: ignore
        from tensorflow.keras.optimizers import Adam #type: ignore
        from tensorflow.keras.callbacks import History #type: ignore

        if self.downsampling:
            texts, target = downsample(texts,target,0.5)

        if self.verbose:
            print('1. Vectorizing texts')

        NUMBER_OF_FEATURES : int = 20000
        self.tokenizer = text.Tokenizer(num_words=NUMBER_OF_FEATURES)
        self.tokenizer.fit_on_texts(texts)
        vocabulary : Dict[str,int] = self.tokenizer.word_index

        if self._max_sequence_length == 0:
            self._max_sequence_length = len(max(texts, key=len))

        vectorized_texts : array = self.vectorize_texts(texts)

        #========== temp =============
        #for n, (t,vector) in enumerate(zip(texts,vectorized_texts)):
        #    open('/vol/tensusers2/wstoop/HaRe/tmp/' + str(n) + '_' + str(target[n]), 'w').write(t+'\n\n'+str(vector))
        #=============================

        if self.embedding_location == '':
            if self.verbose:
                print('2. Skip (no embeddings)')
                print('3. Skip (no embeddings)')
        else:
            if self.verbose:
                print('2. Loading word embeddings')

            embedding_dictionary : Dict[str,List[float]] = load_embedding_dictionary(self.embedding_location)
            nr_of_embedding_features: int = len(list(embedding_dictionary.values())[0])  # Check how many values we have for the first word

            if self.verbose:
                print('3. Creating embedding matrix')

            embedding_matrix : array = create_embedding_matrix_for_vocabulary(embedding_dictionary,vocabulary)

        if self.verbose:
            print('4. Building up model')

        #Define a simple BiGru model with a pretrained embedding layer
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

        model.add(Bidirectional(GRU(16, activation='tanh', return_sequences=True)))
        model.add(Bidirectional(GRU(16, activation='tanh', return_sequences=True)))
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
        metadata : Dict[str,Any] = {'brainType':'BiGru','maxSequenceLength':self._max_sequence_length}
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