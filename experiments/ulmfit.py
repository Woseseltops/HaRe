from pandas import DataFrame
from fastai.text import URLs
from fastai.text import TextLMDataBunch, TextClasDataBunch, language_model_learner, text_classifier_learner
from sklearn.model_selection import train_test_split

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
        for word, replacement in APOSTROPHE_REPLACEMENTS.items():
            s = s.replace(word,replacement)

    for hero in HERO_NAMES:
        s = s.replace(hero,'hero')

    return s

DATA_FOLDER = '../datasets/LoL/'
CLASS_NAMES = ['nontoxic','toxic']
SAMPLES_PER_CLASS = 12500

print('loading data')
texts = []
target = []

for class_index, classname in enumerate(CLASS_NAMES):

    for n, line in enumerate(open(DATA_FOLDER+classname+'.txt')):

        texts.append(preprocess_string(line,False))
        target.append(class_index)

        if n > SAMPLES_PER_CLASS:
            break

df = DataFrame({'label':target,'text':texts})
df_train, df_val = train_test_split(df, stratify = df['label'], test_size = 0.4, random_state = 12)

data_lm = TextLMDataBunch.from_df(train_df = df_train, valid_df = df_val, path = "")
data_clas = TextClasDataBunch.from_df(path = "", train_df = df_train, valid_df = df_val, vocab=data_lm.train_ds.vocab, bs=32)

learn = language_model_learner(data_lm, pretrained_model=URLs.WT103, drop_mult=0.7)
learn.fit_one_cycle(1, 1e-2)
learn.save_encoder('ft_enc')

learn = text_classifier_learner(data_clas, drop_mult=0.7)
learn.load_encoder('ft_enc')
learn.fit_one_cycle(1, 1e-2)

