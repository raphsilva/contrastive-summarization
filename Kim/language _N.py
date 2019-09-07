

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




# lists of negation words
negation_words = {
    #'portuguese': ["jamais", "nada", "nem", "nenhum", "ninguém", "nunca", "não", "tampouco", "nao", "ñ", "ninguem", "longe"],
    'portuguese': ["sem", "jamais", "nada", "nem", "nenhum", "ninguém", "nunca", "não", "tampouco", "nao", "ñ", "ninguem", "longe", "evitar", "impedir", "perder", "tirar"],
    'english': ["never", "neither", "nobody", "no", "none", "nor", "nothing", "nowhere", "not", 'n\'t']
}

LANGUAGE_DIR = 'language'


stopwords = []
from setup import LANGUAGE

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







def process_sentence(sentence):
    # simplifying the sentence
    r = simplify_characters(sentence)

    # tokenize the sentence
    r = nltk.word_tokenize(r, language=LANGUAGE)
    
    if len(r) == 0:
        return r
    
    s = nlpnet_POSTagger.tag_tokens(r, return_tokens=True)                
    
    # removing stopwords from the sentence                
    r = [token for (token, tag) in nlpnet_POSTagger.tag_tokens(r, return_tokens=True) if (tag == 'ADJ' or tag == 'N' or tag == 'V')]
    r = [word for word in r if (word not in stopwords)]

    # Stemmer
    r = [stemmer[LANGUAGE].stem(i) for i in r] 
    
    return r
