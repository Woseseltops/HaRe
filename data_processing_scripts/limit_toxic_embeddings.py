WORK_LOCATION = '/home/wessel/temp/'

TOXIC_EMBEDDING_FILE = '/home/wessel/hare/datasets/LoL/toxic_embeddings'
most_frequent_items = [line.strip() for line in open(WORK_LOCATION+'labels.tsv')]

embedding_output = open(WORK_LOCATION+'toxic_embeddings.tsv','w')
label_output = open(WORK_LOCATION+'toxic_labels.tsv','w')

for line in open(TOXIC_EMBEDDING_FILE,encoding='latin-1'):

    line = line.strip().split()

    if line[0] in most_frequent_items:

        label_output.write(line[0] + '\n')
        embedding_output.write('\t'.join(line[1:]) + '\n')
