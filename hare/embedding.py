from typing import Dict, List
from numpy import array, asarray, zeros # type: ignore

def load_embedding_dictionary(location : str) -> Dict[str,List[float]]:

    embedding_dictionary : Dict[str,List[float]] = {}

    for n,line in enumerate(open(location,encoding='ISO-8859-1')):

        values : List[str] = line.split()
        word : str = values[0]
        syntax_error_at_words : List[str] = []

        try:
            coefs : array = asarray(values[1:], dtype='float32')
            embedding_dictionary[word] = coefs

        except ValueError:
            syntax_error_at_words.append(word)

    print('Embedding file syntax error at these words:',syntax_error_at_words)

    return embedding_dictionary

def create_embedding_matrix_for_vocabulary(embedding_dictionary : Dict[str,List[float]], vocabulary : Dict[str,int]) -> array:

    nr_of_embedding_features : int = len(list(embedding_dictionary.values())[1]) #Check how many values we have for the first word

    embedding_matrix : array = zeros((len(vocabulary) + 1, nr_of_embedding_features))

    for word, i in vocabulary.items():
        embedding_vector = embedding_dictionary.get(word)
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector

    return embedding_matrix