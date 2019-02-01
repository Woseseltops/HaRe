from numpy import asarray

EMBEDDING_TRAINING_SIZE = 6
EMBEDDING_FEATURES = 200
EMBEDDING_LOCATION = '/vol/bigdata/word_embeddings/google_news/GoogleNews-vectors-negative300.txt'

print('loading embedding')
embeddings_index = {}
for line in open(EMBEDDING_LOCATION):
    values = line.split()
    word = values[0]
    coefs = asarray(values[1:], dtype='float32')
    embeddings_index[word] = coefs

print('check word')

while True:
    word = input()

    try:
        print(embeddings_index[word])
    except KeyError:
        print('nope')
