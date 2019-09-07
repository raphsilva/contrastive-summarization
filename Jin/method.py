

import math

from probability import *

import structure as struct
import output_format as out


from setup import ALPHA
from setup import MAXPOLARITY 
from setup import POLARITY_ATTRIBUTION 

import re, string

#from language import stem
from language import lemma
from language import getSentimentLexicon
from language import negation_words

from writefiles import underwrite_file
from writefiles import get_variable_from_file

from language import getSentimentLexicon_ontopt
from language import getSentimentLexicon_sqrt



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
        possible_aspects.append(lemma(k))

            



sentiment_lexicon = getSentimentLexicon()


sentiment_lexicon_ontopt = getSentimentLexicon_ontopt()
sentiment_lexicon_sqrt = getSentimentLexicon_sqrt()


def pol_ontopt(term):
    if term in possible_aspects:
        return 0
    if term in sentiment_lexicon_ontopt:
        return sentiment_lexicon_ontopt[term]
    return 0

def pol_sqrt(term):
    if term in possible_aspects:
        return 0
    if term in sentiment_lexicon_sqrt:
        return sentiment_lexicon_sqrt[term]
    return 0


ww = {}

def lex_sent(term):
    #if term == 'smartphone':
        #return 0
    #if term == 'moto':
        #return 0
    #if term == 'samsung':
        #return 0
    #if term == 'melhor':
        #return 0
    #if term in ['aparelho', 'celular', 'comprar']:
        #return 0
    #if term == 'uso':
        #return 1
    #if term == 'usar':
        #return 1
    #if term == 'não':
        #return -1
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

        
    #if abs(pol_ontopt(term) - pol_sqrt(term)) >=  0.25:
        ##print(term)
        ##print(pol_sqrt(term))
        ##print(pol_ontopt(term))
        ##print()
        #if term not in ww:
            #ww[term] = 0
        #ww[term] += 1
        #sorted_x = sorted(ww.items(), key=lambda kv: kv[1], reverse=True)
        ##if len(ww) > 10:
            ##for y in range(10):
                ##print (sorted_x[y][1], '  ', sorted_x[y][0], pol_sqrt(sorted_x[y][0]), pol_ontopt(sorted_x[y][0]))
        ##print()
        
        
        #input()
    
    #print('  ', term, r)
    return MAXPOLARITY*r


def find_polarities(words):
    
    if POLARITY_ATTRIBUTION != 'complex':
        
        return [(i, lex_sent(i)) for i in words]

    elif POLARITY_ATTRIBUTION == 'complex':
    
        neg_pos = []
        if any(i in negation_words for i in words):
        
            l = []
            
            
            
            for i in range(len(words)):
                if words[i] in negation_words:
                    neg_pos.append(i)
                
            for i in range(len(words)):
                if i in neg_pos:
                    continue # won't keep negation words
                if any(i-j <= 3 and i-j > 0 for j in neg_pos):
                    l.append((words[i],-lex_sent(words[i])))
                    
                else:
                    l.append((words[i],lex_sent(words[i])))
            
        #
        
        
        
        else:    
            l = [(i, lex_sent(i)) for i in words]
            
        return l



def sent (words_polarities):
    
    a = 0
    b = 0
    
    for i in words_polarities:
        a += i[1]
        b += abs(i[1])
    
    sent = MAXPOLARITY*a/(b+ALPHA)
    sent_rounded = float('%.2g' % (sent)) # Rounded to 2 significant digits (to optimize use of cache)

    return sent_rounded


    
    
    
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

def SAM (source, candidate):
    
    global cache_distance, cache_SAM 
    
    key_SAM = repr(source)+repr(candidate)
    
    if key_SAM in cache_SAM:
        return cache_SAM[key_SAM]

        
    score = 0
    debug_score = {}
        
    for aspect in candidate:
        
        c_mean = candidate[aspect]['mean']
        c_std = candidate[aspect]['std']
        c_prob = candidate[aspect]['prob']
                
        if aspect not in source: 
            key_distance = repr([0, 0, 0, c_mean, c_std, c_prob])
            if key_distance in cache_distance: # acess entropy cache
                distance = cache_distance[key_distance]
                
            else: 
                normalSource = normal_distribution_zero
                normalCandid = normalDistribution (c_mean, c_std, c_prob) 
                distance =  -divergence_measure (normalCandid, normalSource) # calculate entropy
                cache_distance[key_distance] = distance # save entropy to cache
            score += distance # add up entropy to make the score
            debug_score[aspect] = distance
            
            
            
            
        else: 
            
            s_mean = source[aspect]['mean']
            s_std = source[aspect]['std']
            s_prob = source[aspect]['prob']
            
            key_distance = repr([s_mean, s_std, s_prob, c_mean, c_std, c_prob])
        
            if key_distance in cache_distance: # acess entropy cache
                distance = cache_distance[key_distance]
            
            else:        
                normalSource = normalDistribution (s_mean, s_std, s_prob)
                normalCandid = normalDistribution (c_mean, c_std, c_prob)
                distance = -divergence_measure (normalCandid, normalSource) # calculate entropy
                cache_distance[key_distance] = distance # save entropy to cache
            score += distance # add up entropy to make the score
            debug_score[aspect] = distance
        
        #divPerAspect[aspect] = round(distance,2)
        
        #out.printdebug
        
        
    for aspect in source: 
        if aspect not in candidate : 
            
            s_mean = source[aspect]['mean']
            s_std = source[aspect]['std']
            s_prob = source[aspect]['prob']
            
            key_distance = repr([s_mean, s_std, s_prob, 0, 0, 0])
            
            if  key_distance in cache_distance: 
                distance = cache_distance[key_distance] # acess entropy cache
                
            else: 
                normalSource = normalDistribution (s_mean, s_std, s_prob)
                normalCandid = normal_distribution_zero
                distance =  -divergence_measure (normalCandid, normalSource)  # calculate entropy 
                cache_distance[key_distance] = distance # save entropy to cache
            score += distance # add up entropy to make the score
            debug_score[aspect] = distance
            
    #pprint(debug_score)
    #print()
            
    score = float('%.4g' % (score))
        
    cache_SAM[key_SAM] = score
    return score



def get_topics(source):
    t = []
    for i in source:
        for o in source[i]:
            if o not in t:
                t.append(o)
    return t
    



def similarity (op1, op2):
    t1 = []
    t2 = []
    for i in op1:
        if i not in t1:
            t1.append(i)
    for i in op2:
        if i not in t2:
            t2.append(i)
    
    #pprint(op1)
    #pprint(op2)
    #pprint(t1)
    #pprint(t2)
    
    intersection = [i for i in t1 if i in t2]
    union = list(set(t1 + t2))
    
    #print()
    #pprint(union)
    
    #CONSIDER CONTRASTIVE 
    #for i in reversed(range(len(intersection))):
        #aspect = intersection[i]
        #if aspect in op1 and aspect in op2:
            #if op1[aspect] * op2[aspect] <= 0:
                #del intersection[i]
            
    #pprint(union)
    #print()
    
    r = len(intersection)/len(union)
    
    #print(r)
    
    #input()
    
    #return 0
    
    return r
            


def score_C (source1, source2, summ1, summ2):
    r = 0
    #for p in source1:
        #for q in summ2:
            #r += similarity(p, q)
    for p in summ1:
        for q in summ2:
            r += similarity(summ1[p], summ2[q])
    return r
    
    

def score_R (source1, source2, summ1, summ2):
    r = 0
    for p in source1:
        for q in summ2:
            r += similarity(source1[p], summ2[q])
    for p in source2:
        for q in summ1:
            r += similarity(source2[p], summ1[q])
    return r

    
def score_D (source1, source2, summ1, summ2):
    r = 0
    for i in range(len(summ1)):
        for j in range(len(summ1)):
            if i != j:
                r -= similarity(summ1[p], summ1[q])
    for i in range(len(summ2)):
        for j in range(len(summ2)):
            if i != j:
                r -= similarity(summ2[p], summ2[q])
    return r





def eval_C(summ1, summ2):
    
    s = 0
    k = min(len(summ1), len(summ2))
    for i in range(k):
        s += similarity(summ1[i]['sent']['corpus'], summ2[i]['sent']['corpus'])
    return s/k

def eval_R(source1, source2, summ1, summ2):
    t_e1 = get_topics(source1)
    t_e2 = get_topics(source2)
    t_r1 = get_topics(summ1)
    t_r2 = get_topics(summ2)
    
    union_E = list(set(t_e1 + t_e2))
    union_R = list(set(t_r1 + t_r2))
    
    return len(union_R)/len(union_E)
    
def eval_D(summ1, summ2):
    s1 = 0
    s2 = 0
    c1 = 0
    c2 = 0
    for i in summ1:
        for j in summ1:
            if i == j:
                continue
            s1 += similarity(summ1[i]['sent']['corpus'], summ1[j]['sent']['corpus'])
            c1 += 1
    for i in summ2:
        for j in summ2:
            if i == j:
                continue
            s2 += similarity(summ2[i]['sent']['corpus'], summ2[j]['sent']['corpus'])
            c2 += 1
    
    return 1 - 0.5*(s1/c1 + s2/c2)
        
    
    
                       





import random



def _OLD__rank_R(source1_stats, source2_stats):
    
    scores = {}
    for i in source1_stats:
        for j in source2_stats: 
            scores[(i,j)] = similarity(source1_stats[i], source2_stats[j])
            
    
    
    rank = sorted(scores.keys(), key=lambda i: scores[i] + random.uniform(-0.001,0.001), reverse=True)
    
    return rank


def rank_R(source1_stats, source2_stats):
    
    scores_1 = {}
    scores_2 = {}
    
    for i in source1_stats:
        s = 0
        for j in source1_stats:
            if j == i:
                continue
            s += similarity(source1_stats[i], source1_stats[j])
        scores_1[i] = s
            
    for i in source2_stats:
        s = 0
        for j in source2_stats:
            if j == i:
                continue
            s += similarity(source2_stats[i], source2_stats[j])
        scores_2[i] = s

            
    
    
    rank_1 = sorted(scores_1.keys(), key=lambda i: scores_1[i] + random.uniform(-0.001,0.001), reverse=True)
    rank_2 = sorted(scores_2.keys(), key=lambda i: scores_2[i] + random.uniform(-0.001,0.001), reverse=True)
    
    return rank_1, rank_2


def rank_D(source1_stats, source2_stats):
    
    scores_1 = {}
    scores_2 = {}
    
    for i in source1_stats:
        s = 0
        for j in source1_stats:
            if j == i:
                continue
            s -= similarity(source1_stats[i], source1_stats[j])
        scores_1[i] = s
            
    for i in source2_stats:
        s = 0
        for j in source2_stats:
            if j == i:
                continue
            s -= similarity(source2_stats[i], source2_stats[j])
        scores_2[i] = s

            
    
    
    rank_1 = sorted(scores_1.keys(), key=lambda i: scores_1[i] + random.uniform(-0.001,0.001), reverse=True)
    rank_2 = sorted(scores_2.keys(), key=lambda i: scores_2[i] + random.uniform(-0.001,0.001), reverse=True)
    
    return rank_1, rank_2




def rank_C(source1_stats, source2_stats):
    
    scores = {}
    for i in source1_stats:
        for j in source2_stats: 
            scores[(i,j)] = similarity(source1_stats[i], source2_stats[j])
            
    
    
    rank = sorted(scores.keys(), key=lambda i: scores[i] + random.uniform(-0.001,0.001), reverse=True)

            
    #sss = sorted(scores.items(), key=lambda i: scores[i[0]] + random.uniform(-0.001,0.001), reverse=True)
    
    #sss = [i for i in sss if i[1] > 0]

            
    #pprint(sss)
    
    
    
    rank_1 = [i[0] for i in rank]
    rank_2 = [i[1] for i in rank]
    
    return rank_1, rank_2






    
    

def score (source1, source2, summ1, summ2, method='R'):
    if method == 'C':
        return score_C (source1, source2, summ1, summ2)
    if method == 'R':
        return score_R (source1, source2, summ1, summ2)


    
    
    
def SAM_contrastive (original_stats_1, original_stats_2, stats_cand_1, stats_cand_2):
    
    
    return None
    
    
    #key_SAM = repr(original_stats_1)+repr(original_stats_2)+repr(stats_cand_1)+repr(stats_cand_2)
    
    #if key_SAM in cache_SAM:
        #return cache_SAM[key_SAM]
    
    score11 = +SAM(original_stats_1, stats_cand_1)
    score22 = +SAM(original_stats_2, stats_cand_2)
    score12 = -SAM(original_stats_1, stats_cand_2)
    score21 = -SAM(original_stats_2, stats_cand_1)

    

    score = (score11 + score12 + score21 + score22)/4      # Using average instead of sum (doesn't affect anything, only makes it prettier)
    
    score = float('%.4g' % (score))
    #cache_SAM[key_SAM] = score
    
    return score
    
    
        
        




def save_caches():
    underwrite_file('cache/SAM.cache', cache_SAM)
    underwrite_file('cache/distance.cache', cache_distance)


    
