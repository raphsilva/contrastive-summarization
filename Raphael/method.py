

import math

from probability import *

import structure as struct
import output_format as out


from setup import ALPHA
from setup import MAXPOLARITY 
from setup import POLARITY_ATTRIBUTION 
from setup import KEY_MEASURE 

import re, string

#from language import stem
#from language import lemma
from language import getSentimentLexicon
from language import negation_words

from writefiles import underwrite_file
from writefiles import get_variable_from_file


def set_ALPHA(value):
    global ALPHA
    ALPHA = value
    return ALPHA




def divergence_measure(d1, d2):
    #return integralDivergence(d1, d2)
    #return hellingerDistance(d1, d2)
    return KLdivergence(d1, d2)






#aspects_dict = get_variable_from_file('language/portuguese/aspects_clues.json')
#possible_aspects = []


#for typ in aspects_dict:
    #for k in aspects_dict[typ]:
        #if aspects_dict[typ][k] not in possible_aspects:
            #possible_aspects.append(aspects_dict[typ][k])

possible_aspects = []
aspects_list = get_variable_from_file('language/portuguese/aspects.json')
for typ in aspects_list:
    for k in aspects_list[typ]:
        possible_aspects.append(k)

            



sentiment_lexicon = getSentimentLexicon()



def lex_sent(term):
    #from language import process_sentence
    #term = process_sentence(term)[0]
    term = term.lower()
    term = re.sub('[' + string.punctuation + ']', '', term) # Remove punctuation
    if POLARITY_ATTRIBUTION == 'complex':
        if term in possible_aspects:
            return 0
    r = 0
    if term in sentiment_lexicon:
        r = sentiment_lexicon[term]
    
    #print('  ', term, r)
    return MAXPOLARITY*r


def find_polarities(words):
    
    if POLARITY_ATTRIBUTION == 'pure':
        
        return [(i, lex_sent(i)) for i in words]

    elif POLARITY_ATTRIBUTION == 'complex':
    
        if any(i in negation_words for i in words):
        
            l = []
            
            neg_pos = []
            
            for i in range(len(words)):
                if words[i] in negation_words:
                    neg_pos.append(i)
                
            for i in range(len(words)):
                if i in neg_pos:
                    continue # won't keep negation words
                if any(i-j <= 3 and i-j > 0 for j in neg_pos):
                    l.append((words[i],-lex_sent(words[i])))
                    
                    #print(neg_pos)
                    #print(words, i)
                    #print()
                    #input()
                    
                else:
                    l.append((words[i],lex_sent(words[i])))
            
        #print(l)
        
        
        
        else:    
            l = [(i, lex_sent(i)) for i in words]
        
        return l
    
    ##print('BOM', lex_sent('bom'), sentiment_lexicon['bom'])
    
    ##print(l)
    
    #pol = sum(l)
    
    ##print('\nPolaridades das palavras:')
    #intens = sum([abs(lex_sent(i)) for i in words])
    
    #sent = MAXPOLARITY*pol/(intens+ALPHA+0.00001)
    #sent_rounded = float('%.2g' % (sent)) # Rounded to 2 significant digits (to optimize use of cache)
    
    ##print()
    ##print('\"'+sentence+'\"')
    ##print()
    ##print('Avaliação automática (de -100 a +100):\n', sent_rounded)
    ##input()
    
    #return sent_rounded 
    
    






def sent (words_polarities):
    
    a = 0
    b = 0
    
    for i in words_polarities:
        a += i[1]
        b += abs(i[1])
    
    sent = MAXPOLARITY*a/(b+ALPHA)
    sent_rounded = float('%.2g' % (sent)) # Rounded to 2 significant digits (to optimize use of cache)

    return sent_rounded



def OLD_mean_summ_sent(S, info):    
    r = 0
    for i in S:
        r += sent(info[i]['sentence'])
    r = r/len(S)
    return int(r)
    
    
    
def mismatch (S, S_rating, info):    
    a = S_rating - mean_summ_sent(S, info)
    return a*a/MAXPOLARITY
        
        
def SM (source, candidate):         
    return mismatch (source, candidate)
    
  

cache_distance = get_variable_from_file('cache/distance.cache')  
cache_SAM = get_variable_from_file('cache/SAM.cache')  
  
if cache_distance == False:
    cache_distance = {}

if cache_SAM == False:
    cache_SAM = {}

normal_distribution_zero = normalDistributionZero() 





########################################################################


import evaluation.evaluation as evaluation


def score_repr_summ (source, candidate):
    return evaluation.representativiness(source, candidate, KEYMEASURE=KEY_MEASURE)
    
    
    
    
def score_comp_summ (source1, source2, candidate1, candidate2):
    r1 = evaluation.representativiness(source1, candidate1, KEYMEASURE=KEY_MEASURE)
    r2 = evaluation.representativiness(source2, candidate2, KEYMEASURE=KEY_MEASURE)
    c = evaluation.contrastiviness(source1, source2, candidate1, candidate2, KEYMEASURE=KEY_MEASURE)
    r = 0.5*(r1+r2)
    a = 2*(c*r)/(c+r)
    return a
    
    #score11 = +SAM(original_stats_1, stats_cand_1)
    #score22 = +SAM(original_stats_2, stats_cand_2)
    #score12 = -SAM(original_stats_1, stats_cand_2)
    #score21 = -SAM(original_stats_2, stats_cand_1)
    

    #score = (score11 + score12 + score21 + score22)/4      # Using average instead of sum (doesn't affect anything, only makes it prettier)
    
    #return score
    
    

def score_representativity(source1, source2, candidate1, candidate2):
    r1 = evaluation.representativiness(source1, candidate1, KEYMEASURE=KEY_MEASURE)
    r2 = evaluation.representativiness(source2, candidate2, KEYMEASURE=KEY_MEASURE)
    return (r1+r2)/2




def save_caches():
    underwrite_file('cache/SAM.cache', cache_SAM)
    underwrite_file('cache/distance.cache', cache_distance)


    