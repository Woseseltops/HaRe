from numpy import array
from sklearn.manifold import TSNE
from json import dumps

EMBEDDING_FILE_LOCATON = '../../datasets/LoL/toxic_embeddings_for_visualizer.tsv'
LABEL_FILE_LOCATION = '../../datasets/LoL/toxic_labels_for_visualizer.tsv'
OUTPUT_FILE_LOCATION = 'embedding_tsne.js'

labels = open(LABEL_FILE_LOCATION).readlines()
points = []

for line in open(EMBEDDING_FILE_LOCATON):
	items = line.split()
	weights = array([float(item) for item in items])
	points.append(weights)

points = array(points)

outcome = TSNE(n_components=3, perplexity=8, learning_rate=10).fit_transform(points)
open(OUTPUT_FILE_LOCATION,'w').write('var tsne_x = '+dumps(outcome[:,0].tolist())+';var tsne_y = '+dumps(outcome[:,1].tolist())+';var tsne_z = '+dumps(outcome[:,2].tolist())+';var labels = '+dumps(labels)+';')
