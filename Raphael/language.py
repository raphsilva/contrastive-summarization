from writefiles import get_variable_from_file
from writefiles import underwrite_file

# lists of negation words
negation_words = ["sem", "jamais", "nada", "nem", "nenhum", "ninguém", "nunca", "não", "tampouco", "nao", "ñ",
                  "ninguem", "longe", "evitar", "impedir", "perder", "tirar"]

LANGUAGE_DIR = 'language'

stopwords = []

LANGUAGE = 'portuguese'


def setLanguage(language):
    global LANGUAGE
    global stopwords

    DIR = LANGUAGE_DIR + '/' + LANGUAGE

    stopwords = open(DIR + '/' + 'stopwords.txt').read().split()


setLanguage(LANGUAGE)

got_all_lemmas = False


def readLemmaDic():
    global got_all_lemmas
    r = {}
    f = open('language/portuguese/lemmas.dic', 'r')
    for i in f:
        if len(i) == 0:
            continue
        if '#' in i:
            continue
        w = i.split(',')[0]
        s = i.split(',')[1].split('.')[0]
        r[w] = s
    got_all_lemmas = True
    return r


lemmas_dic = get_variable_from_file('cache/lemmas.cache')
if lemmas_dic == False:
    lemmas_dic = readLemmaDic()

lemmas_cache = {}

lemmas_exceptions = {}
lemmas_exceptions['bateria'] = 'bateria'
lemmas_exceptions['baterias'] = 'bateria'


def lemma(word):
    global lemmas_cache
    global lemmas_dic
    if word in lemmas_dic:
        r = lemmas_dic[word]
    else:
        if got_all_lemmas == False:
            lemmas_dic = readLemmaDic()
            return lemma(word)
        else:
            r = word
    if word in lemmas_exceptions:
        r = lemmas_exceptions[word]
    if word not in lemmas_cache:
        lemmas_cache[word] = r
        underwrite_file('cache/lemmas.cache', lemmas_cache)  # TODO fica bem mais lento, põe pra fora
    return r


from setup import POLARITY_LEXICON


def getSentimentLexicon():
    r = {}
    if POLARITY_LEXICON == 'ontopt':
        f = open('language/portuguese/OntoPT-sentic.txt', 'r')
    elif POLARITY_LEXICON == 'sqrt':
        f = open('language/portuguese/ml-sqrt.txt', 'r')
    elif POLARITY_LEXICON == 'ml':
        f = open('language/portuguese/oplexicon.txt', 'r')
    elif POLARITY_LEXICON == 'oplexicon':
        f = open('language/portuguese/oplexicon_v3_0.txt', 'r')
    elif POLARITY_LEXICON == 'sentilex':
        f = open('language/portuguese/sentilex-reduzido.txt', 'r')
    for i in f:
        w = i.split(',')[0]
        s = i.split(',')[1]
        r[w] = float(s)

    return r


def getSentimentLexicon_ontopt():
    r = {}
    f = open('language/portuguese/OntoPT-sentic.txt', 'r')
    for i in f:
        w = i.split(',')[0]
        s = i.split(',')[1]
        r[w] = float(s)

    return r


def getSentimentLexicon_sqrt():
    r = {}
    f = open('language/portuguese/ml-sqrt.txt', 'r')
    for i in f:
        w = i.split(',')[0]
        s = i.split(',')[1]
        r[w] = float(s)

    return r
