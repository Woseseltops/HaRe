from gensim.models.keyedvectors import KeyedVectors

print('loading')
model = KeyedVectors.load_word2vec_format('/vol/bigdata/word_embeddings/google_news/GoogleNews-vectors-negative300.bin', binary=True)
print('saving')
model.save_word2vec_format('/vol/bigdata/word_embeddings/google_news/GoogleNews-vectors-negative300.txt', binary=False)