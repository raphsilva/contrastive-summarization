# Functions to format output
from time import sleep
from pprint import pprint

from language import process_sentence
from language import lemma


from method import sent
from method import find_polarities

import setup 

from setup import ALPHA

MAXPOLARITY = setup.MAXPOLARITY

import random


import io
import os

from setup import MAXPOLARITY
from setup import ASPECT_DETECTION
from setup import POLARITY_ATTRIBUTION
from setup import KEY_MEASURE
from setup import BYPASS_GENERIC
#from setup import BYPASS_UNRELATAD
from setup import BYPASS_SHORT

from pprint import pprint


SENTENCE_BEGIN_INDICATOR = '::' 


polarity_scale = {'++':  1.00*MAXPOLARITY,
                  '+' :  1*MAXPOLARITY,
                  '+.':  1*MAXPOLARITY,
                  '.' :    0,                                    
                  '..':    0,                  
                  '!' :    0,                  
                  '-.': -1*MAXPOLARITY,
                  '-' : -1*MAXPOLARITY,
                  '--': -1.00*MAXPOLARITY,
                  'X' : 0,
                  'x' : 0}


def cleanExtraSpaces(sentence):
    r = sentence
    while len(r) > 0 and r[0] == ' ':
        r = r[1:]
    while len(r) > 0 and r[-1] == ' ':
        r = r[:-1]
    return r




from writefiles import get_variable_from_file


# Reads input files
def read_input (filename): 
    
    count_wrong = 0
    
    #info = getInfo(filename)['data']
    
    g = get_variable_from_file(filename)
    
    info = g['data']
    
    product_type = g['meta']['Type'].lower()
    
    aspects_clues = {}
    
    c_words = 0
    
    if ASPECT_DETECTION == 'clues':
    
        aspects_dict = get_variable_from_file('language/portuguese/aspects_clues.json')
        
        for typ in aspects_dict:
            if typ == 'GENERIC' or typ == product_type:
                for k in aspects_dict[typ]:
                    if k not in aspects_clues:
                        aspects_clues[k] = aspects_dict[typ][k]
                        aspects_clues[lemma(k)] = aspects_dict[typ][k]
                
    elif ASPECT_DETECTION == 'keywords':
        
        aspects_words = get_variable_from_file('language/portuguese/aspects.json')
        for typ in aspects_words:
            if typ == 'GENERIC' or typ == product_type:
                for w in aspects_words[typ]:
                    aspects_clues[w] = w
                    aspects_clues[lemma(w)] = w
                    
                    
    
                
        
        
    
    #pprint(aspects_clues)
    #input()
    
    r = {}
    
    
    c_rem_unrelated = 0
    c_rem_generic_short = 0
    c_noaspect = 0
    
    for i in info:
        n = {}
        n['id'] = i['id']
        n['opinions'] = []
        for o in i['opinions']:
            pol = polarity_scale[o[1]]
            asp = o[0]
            if asp == 'PRODUTO':
                asp = '_GENERIC'
            if pol != None:
                n['opinions'].append((asp, pol))
        n['opinions'] = sorted(n['opinions'])
        #for aspect in i['aspects']:
            #n['opinions'].append((aspect, i['polarity']))
        n['verbatim'] = i['sentence']
        #n['text_info'] = process_sentence(i['sentence'])
        n['word_count'] = len((n['verbatim']).split()) # number of words
        
        c_words += n['word_count'] 
        
        n['sent'] = {}
        
        n['sent']['corpus'] = opinionsToSent(n['opinions'])
        
        # Remove opinions that don't talk about the product
        
        #if BYPASS_UNRELATAD:
            #for i in reversed(range(len(n['opinions']))):
                #if n['opinions'][i][0] == 'EMPRESA':
                    #del n['opinions'][i]
        #if BYPASS_GENERIC:
            #for i in reversed(range(len(n['opinions']))):
                #if n['opinions'][i][0] == 'PRODUTO':
                    #del n['opinions'][i]
               
        
        #words = [i for i in n['verbatim'].split() if len(i) > 3] # [i[0] for i in n['opinions']]
        
        words = process_sentence(n['verbatim'], STEM=True)
        
        n['words'] = words
        
        polarities_lexicon = find_polarities(words)
        
        intensity = sum([p[1] for p in polarities_lexicon])
        
        #pprint(polarities_lexicon)
        #print(intensity)
        #input()
        
        
        sent_lex = sent(polarities_lexicon)
        
        
        #words_n = process_sentence(n['verbatim'], STEM=False)
        #sent_lex_n = find_polarities(words_n)
        
        #pprint(sent_lex_n)
        #input()
        
        #polarities_lexicon = [(lemma(i[0]), i[1]) for i in sent_lex_n]
        
        #print(n['verbatim'])
        #print(sent_lex)
        #print(sent_lex_n)
        #input()
        #print()
        
        #n['sent']['lexicon'] =  {j: sent_lex for j in words}
        #pprint(n['sent']['lexicon'])
        
        n['sent']['lexicon'] = {}
    
    
        #print(n['verbatim'])
        #print()
        
        aspects = []
        for w in words:
            if w in aspects_clues:
                aspects.append(aspects_clues[w])
                
        
        #ATTENTION
        if polarities_lexicon == []:
            polarities_lexicon = [('_NONE', 0)]
        
        #print(polarities_lexicon)
        
        
        
        for p in range(len(polarities_lexicon)):
            
            
            
            t = sum([i[1] for i in n['opinions']])
                
            a = sum([abs(i[1]) for i in n['opinions']])
        
            s = (t/(ALPHA+a))
            
            
            if len(n['opinions']) == 0:
                pol_manual = 0
                #continue 
            
            else:
                pol_manual = s
                #pol_manual = t/len(n['opinions'])
                #if pol_manual == 0:
                    #continue
                    
                #if pol_manual != 0:
                    #pol_manual = pol_manual/abs(pol_manual)
                
                pol_manual *= MAXPOLARITY 
            
            
            if POLARITY_ATTRIBUTION == 'manual':
                
                    
                n['sent']['lexicon'][polarities_lexicon[p][0]] = pol_manual
                
                #s = sent(polarities_lexicon)
                
                #if s*pol_manual <= 0:
                
                    #n['sent']['lexicon'][polarities_lexicon[p][0]] = -s
                    
                #else:
                    #n['sent']['lexicon'][polarities_lexicon[p][0]] = s
                

                
                #print(t, a, s)
                
            
            elif POLARITY_ATTRIBUTION == 'complex':
                a = max(p-4,0)
                b = min(p+5, len(polarities_lexicon))
                
                neighbours = polarities_lexicon[a:p] + polarities_lexicon[p+1:b]
                
                #while a-b == 0 or max([abs(q[1]) for q in polarities_lexicon[a:b]]) <= MAXPOLARITY*0.5: 
                    #if ((b-a)%2 == 1 or a == 0) and b != len(polarities_lexicon):
                        
                        #b = min(b+1, len(polarities_lexicon))
                        
                    #else:
                        #a = max(a-1,0)
                        
                    ##print(a,b)
                    #if a == 0 and b == len(polarities_lexicon):
                        #break
                    
                    #if b-a > 6:
                        #break
                    
                neighbours = polarities_lexicon[a:p] + polarities_lexicon[p+1:b]
                
                
                #print(polarities_lexicon[p])
                #pprint(neighbours)
                #print(sent(neighbours))
                #print()
                
                #print(b-a)
       
                n['sent']['lexicon'][polarities_lexicon[p][0]] = sent(neighbours)
                
                
                
                
        
            
                
            elif POLARITY_ATTRIBUTION == 'pure':
                n['sent']['lexicon'][polarities_lexicon[p][0]] = sent(polarities_lexicon)
                
        #pprint(n['verbatim'])
        ##pprint(polarities_lexicon)
        #print(sent(polarities_lexicon))
        #print(pol_manual)
        #print(n['opinions'])
        #if pol_manual * sent(polarities_lexicon) <= 0:
            #print('***')
            #print()
            #print()
            ##input()
        #print()
        
        
        
        #input()
            #pprint(polarities_lexicon[a:b])
            #input()
        #print(n['verbatim'])
        #print()
        #pprint(polarities_lexicon)
        #print()
        #pprint(n['sent']['lexicon'])
        #print()
        #print()
        
        #input()
        #print()
        #print()

        
        
        sent_aspects = []
        
        
        #if True or POLARITY_ATTRIBUTION == 'complex' or POLARITY_ATTRIBUTION == 'manual':
        for p in list(n['sent']['lexicon'].keys()):
            #print(p)
            if p in aspects_clues:
                sent_aspects.append((aspects_clues[p], n['sent']['lexicon'][p]))
            
            #pprint(sent_aspects)

            
            #pprint(sent_aspects)
        
        #else:
            #for p in polarities_lexicon:
                #if p[0] in aspects_clues:
                    #sent_aspects.append((aspects_clues[p[0]], p[1]))
         
         
        
                    
        #intensity_aspects = 0
        #for w in polarities_lexicon:
            #if w in aspects_clues:
                #polarities_aspects += polarities_lexicon[w]
                
        #pprint(polarities_lexicon)
        #print(intensity_aspects)
        #input()
            
        #pprint(aspects_clues)
            
        #pprint(aspects)
        #pprint(sent_aspects)
        #pprint(polarities_lexicon)
        #pprint(n['opinions'])
        #input()
        
        #sent_asp= sent(sent_aspects)
                
        
        #n['sent']['aspects'] =   {aspects_clues[j]: n['sent']['lexicon'][j] for j in n['sent']['lexicon'] if j in aspects_clues}
        
        
        a = {}
        for j in n['sent']['lexicon']:
            if j in aspects_clues:
                if aspects_clues[j] not in a:
                    a[aspects_clues[j]] = []
                a[aspects_clues[j]].append(n['sent']['lexicon'][j])
                
        n['sent']['aspects'] = {}
        for i in a:
            n['sent']['aspects'][i] = sum(a[i])/len(a[i])
            
            
        #if 'tamanho' in aspects:
            #print(n['verbatim'])
            #pprint(aspects)
            #print(n['sent']['aspects']['tamanho'])
            #pprint(n['opinions'])
            #print()
        
        #n['aspects'] = aspects
        
        if aspects == []:
            
            
            #if BYPASS_SHORT: 
                #if len(words) < 3:
                    ##print(words)
                    #c_rem_generic_short += 1
                    #continue
                
            c_noaspect += 1
        
            
                #continue # ATTENTION
                
                
                
                
            #aspects = ['produto']
            
            if POLARITY_ATTRIBUTION == 'manual':
            
                if n['sent']['aspects'] == {}: # ATTENTION
                    n['sent']['aspects'] = {'produto': pol_manual}
                    
                if sent_aspects == []:
                    sent_aspects.append(('produto', pol_manual))
                    
            else:
                
                if n['sent']['aspects'] == {}: # ATTENTION
                    n['sent']['aspects'] = {'produto': sent(polarities_lexicon)}
                    
                if sent_aspects == []:
                    sent_aspects.append(('produto', sent(polarities_lexicon)))
        
        #if BYPASS_UNRELATAD:
            #if 'empresa' in aspects:
                #c_rem_unrelated += 1
                #continue
            #if 'outro' in aspects:
                #continue
            #if KEY_MEASURE == 'corpus' and 'EMPRESA' in [i[0] for i in n['opinions']]:
                #continue
        
       
        #aspects_found = aspects
        #aspects_tagged = [i[0].lower() for i in n['opinions']]
        
        #if any(i not in aspects_found for i in aspects_tagged) or any(i not in aspects_tagged for i in  aspects_found):
            #if aspects_tagged == []:
                #continue
            #print(n['verbatim'])
            #print(sorted(aspects_tagged))
            #print(sorted(aspects_found))
            #print()
            #count_wrong += 1
        #else:
            #print('o')
       
        #print(n['verbatim'])
        #print()
        #pprint(n['opinions'])
        #print()
        #pprint(n['sent']['aspects'])
        #print()
        #print()
        ##input()
        
        #print(n['verbatim'])
        #pprint(n['sent']['lexicon'])
        #pprint(n['sent']['aspects'])
        #pprint(n['sent']['corpus'] )
        ##print()
        ##print()
        #input()
        
        #pprint(n['sent_corpus'])
        #print()
        #pprint(n['sent_lexicon'])
        #print()
        #print()
        #input()
        
        #print(n['opinions'])
        #print(n['sent_corpus'])
        #input()
        
        n['intensity'] = {}
        
        n['intensity']['corpus'] = opinionsToIntensity(n['opinions'])
        n['intensity']['lexicon'] = opinionsToIntensity(polarities_lexicon)
        
        
        
        #n['intensity']['aspects'] = opinionsToIntensity(sent_aspects)
        
        #pprint(polarities_lexicon)
        #print(n['intensity']['lexicon'])
        #print()
        
        if POLARITY_ATTRIBUTION == 'complex':
            #pprint(sent_aspects)
            n['intensity']['aspects'] = opinionsToIntensity(sent_aspects)
            
            #print(n['verbatim'])
            #pprint(sent_aspects)
            #print(n['intensity']['aspects'])
            #print()
            #input()
            #print(n['intensity']['aspects'])
            #if n['intensity']['aspects'] < 1:
                #print()
                #pprint(n)
                #print()
                #input()
        else:
            n['intensity']['aspects'] = n['intensity']['lexicon']
            
        n['intensity']['aspects'] = n['intensity']['lexicon']
        
        #n['intensity'] = opinionsToIntensity(n['opinions'])
        r[n['id'] ] = n
        
        #pprint(n)
        #input()
        
    print('TOTAL PALAVRAS  ', c_words)
    
    print ("Sentences (initial):", len(info))
    print ("Removed unrelated:", c_rem_unrelated)
    print ("Removed generic short:", c_rem_generic_short)
    print ("Size of initial dataset:", len(r))
    print ("Sentences without aspects:", c_noaspect)
    print()
    
    #pprint(r)
    #input()
    
    #print()
    #print(count_wrong)
    #input()
    
    #217
    #287
    
    #205
    #281
    
    #196
    #282
    
    # 144
    # 168
    
    
    ###max_sent_corpus = max([max(i) for i in [[abs(b) for b in list(r[j]['sent']['corpus'].values())] for j in r] if len(i) > 0])
    ###max_sent_aspects = max([max(i) for i in [[abs(b) for b in list(r[j]['sent']['aspects'].values())] for j in r] if len(i) > 0])
    ###max_sent_lexicon= max([max(i) for i in [[abs(b) for b in list(r[j]['sent']['lexicon'].values())] for j in r] if len(i) > 0])
    ###pprint(max_sent_corpus)
    ###pprint(max_sent_aspects)
    ###input()
    
    
    return r
 



def getAspectSent(opinions, aspect):
    s = []
    for i in opinions: 
        if i[0] == aspect: 
            s.append((i[0], i[1]))
    return sent(s)
        



def opinionsToSent(opinions): 
    r = {}
    for i in opinions: 
        if i[0] in r:
            continue
        r[i[0]] = getAspectSent(opinions, i[0])
    
    return r
    
    





    


def opinionsToIntensity(opinions):
    #print(opinions)
    if len(opinions) == 0:
        return 0
    s = 0
    for o in opinions: 
        s += abs(o[1])
        #print(o[1], s)
    return s#/len(opinions)


def sentBinaryToInt(opinions): 
    for i in opinions: 
        if i[1] == '-': 
            i[1] = -MAXPOLARITY
        elif i[1] == '+':
            i[1] = MAXPOLARITY 
        else:
            i[1] = 0
    return opinions


def removeNonOppinionated(info):
    r = {}
    for i in info:
        if info[i]['opinions'] != []: 
            r[i] = info[i]
    return r
