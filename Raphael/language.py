

import re
import string

# used for: tagger for English, tokenizer, stopwords lists, stemmer
import nltk
from nltk.stem import RSLPStemmer, PorterStemmer

# used for: tagger for Portuguese
import nlpnet

# NLP variables
stemmer = dict(portuguese=RSLPStemmer(), english=PorterStemmer())
nlpnet.set_data_dir("language/portuguese")
nlpnet_POSTagger = nlpnet.POSTagger()


from writefiles import save_to_file
from writefiles import get_variable_from_file
from writefiles import underwrite_file



# lists of negation words
negation_words = ["sem", "jamais", "nada", "nem", "nenhum", "ninguém", "nunca", "não", "tampouco", "nao", "ñ", "ninguem", "longe", "evitar", "impedir", "perder", "tirar"]
#negation_words = [ "não", "nao", "ñ"]

LANGUAGE_DIR = 'language'




stopwords = []
#from setup import LANGUAGE

LANGUAGE = 'portuguese'


def setLanguage(language):
    global LANGUAGE
    global stopwords
    
    DIR = LANGUAGE_DIR+'/'+LANGUAGE

    
    stopwords = open(DIR+'/'+'stopwords.txt').read().split()
    #print(f.split())
    #exit()
    
    
    #LANGUAGE = language
    #print(LANGUAGE)    
    #stopwords = nltk.corpus.stopwords.words(LANGUAGE)
    #print(stopwords)
    #input()
   
setLanguage(LANGUAGE)   
        
got_all_lemmas = False        
def readLemmaDic():
    global got_all_lemmas
    #return []
    r = {}
    f = open('language/portuguese/lemmas.dic', 'r')
    for i in f:
        if len(i)==0:
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
        underwrite_file('cache/lemmas.cache', lemmas_cache) #TODO fica bem mais lento, põe pra fora
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
        #if w == 'bom':
            #print(w, s)
            
    return r

def getSentimentLexicon_ontopt():
    r = {}
    f = open('language/portuguese/OntoPT-sentic.txt', 'r')
    for i in f:
        w = i.split(',')[0]
        s = i.split(',')[1]
        r[w] = float(s)
        #if w == 'bom':
            #print(w, s)
            
    return r

def getSentimentLexicon_sqrt():
    r = {}
    f = open('language/portuguese/ml-sqrt.txt', 'r')
    for i in f:
        w = i.split(',')[0]
        s = i.split(',')[1]
        r[w] = float(s)
        #if w == 'bom':
            #print(w, s)
            
    return r
    


def simplify_characters(my_string):
    """
    Normalize the characters, transform characters into lowercase and remove both punctuation and special characters from a string.
    :param my_string: [str]
    :return: [str] returns a simplified string with only numbers, letters and spaces.
    """

    # normalize and transform characters into lowercase
    #normalized_string = unicodedata.normalize('NFKD', my_string.casefold())
    normalized_string = my_string.lower()

    # simplify characters in a way that ç becomes c, á becomes a, etc.
    #normalized_string = u"".join([c for c in normalized_string if not unicodedata.combining(c)])

    # remove punctuation and special characters
    return re.sub('[' + string.punctuation + ']', ' ', normalized_string)










cache_removed_negs_adjs = {}


def makecache_remove_negs_adjs(sentence): 
    
    global cache_removed_negs_adjs
    
    if len(sentence) == 0:
        return []
    
    k = process_sentence(sentence)
    
    if str(k) in cache_removed_negs_adjs:
        return 
    
    # simplifying the sentence
    s = simplify_characters(sentence)

    # tokenize the sentence
    s = nltk.word_tokenize(s, language=LANGUAGE)
    
    r = s
    
    #removing adjectives from both sentences
    if LANGUAGE == 'english':
        r = [token for (token, tag) in nltk.pos_tag(s, tagset='universal') if (tag != 'ADJ')]
    elif LANGUAGE == 'portuguese':
        r = [token for (token, tag) in nlpnet_POSTagger.tag_tokens(s, return_tokens=True) if (tag == 'N' or tag == 'V')]
        
    #removing negation words from sentence
    r = [word for word in r if (word not in negation_words[LANGUAGE])]
    
    r = [word for word in r if (word not in stopwords)]
    
    # Stemmer
    r = [stemmer[LANGUAGE].stem(i) for i in r] 
        
    cache_removed_negs_adjs[str(k)] = r
    
    return r





def removeNegsAndAdjs(sentence_proc):
    return cache_removed_negs_adjs[str(sentence_proc)] # This cache is made right when data is loaded




def stem(word, language=LANGUAGE):
    return stemmer[language].stem(word)
    


def process_sentence(sentence, STEM=True):
    # simplifying the sentence
    r = simplify_characters(sentence)

    # tokenize the sentence
    r = nltk.word_tokenize(r, language=LANGUAGE)
    
    if len(r) == 0:
        return r
    
    s = nlpnet_POSTagger.tag_tokens(r, return_tokens=True)                
    
    # removing stopwords from the sentence                
    r = [token for (token, tag) in nlpnet_POSTagger.tag_tokens(r, return_tokens=True) if (tag == 'ADJ' or tag == 'N' or tag == 'V' or token in negation_words)]
    
    r = [word for word in r if (word not in stopwords or word in negation_words)]
    

    # Stemmer
    if STEM:
        r = [lemma(i) for i in r] 
        
    r = [word for word in r if (word not in stopwords or word in negation_words)]
    r = [word for word in r if not word.isdigit()]
    
    return r
