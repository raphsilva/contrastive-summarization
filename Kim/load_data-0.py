from language import process_sentence
from language import makecache_remove_negs_adjs
from setup import *

from writefiles import get_variable_from_file



MAXPOLARITY = 100


polarity_scale = {'++':  1.00*MAXPOLARITY,
                  '+' :   .80*MAXPOLARITY,
                  '+.':   .50*MAXPOLARITY,
                  '.' :    0,                                    
                  '..' :   0,                  
                  '!' :    0,                  
                  '-.':  -.50*MAXPOLARITY,
                  '-' :  -.80*MAXPOLARITY,
                  '--': -1.00*MAXPOLARITY,
                  'X' : None,
                  'x' : None}




def load_dataset(filename):
    from setup import ASPECTS_TAGS
    
    info = get_variable_from_file(filename)['data']
    
    r = {}
    
    for i in info:
        
        
        
     
        
        n = {}
        n['opinions'] = []
        for o in i['opinions']:
            asp = o[0]
            
            #if asp == '_GENERIC':
                #continue
            
            
            pol = polarity_scale[o[1]]
           

            if pol == None:
                continue # Ignores things that are not opinions
           
            n['opinions'].append((asp, pol))
            
        n['sentence'] = i['sentence']
        n['word_count'] = len((n['sentence']).split()) # number of words
        
        n['text_info'] = process_sentence(i['sentence'])
        
        #print(n['sentence'])
        #print(n['text_info'])
        #input()
        
        if ASPECTS_TAGS == 'join':
            for o in n['opinions']:
                n['text_info'].append('_'+o[0])
        if ASPECTS_TAGS == 'only':
            n['text_info'] = [o[0] for o in n['opinions']]
            
            #print(n['text_info'], n['sentence']  )
            
        if len(n['text_info']) == 0:
            continue
        
        n['id'] = i['id']       
        r[len(r)] = n
        
        makecache_remove_negs_adjs(n['sentence']) # Process the sentence to get information that will be used later.

    #print(len(r))
    #exit()
    
    return r
    
    

def preprocess(data):
    r = {'+': [], '-': []} # Data will be returned split by polarity
    
    for sample_id in data: 
        
        sample = data[sample_id]
        
        #print(sample['opinions'], sample['text_info'])
        #print(sample['opinions'])
        
        #aspects = [i[0] for i in sample['opinions']]
        
        #if len(aspects) == 0:
            #continue
        
        
        #if 'EMPRESA' in aspects:
            #continue
        
        #if '_NONE' in aspects:
            #continue
        #if '_TRASH' in aspects:
            #continue
        #if '_DUPLICATE' in aspects:
            #continue
        
        #if 'x' in aspects:
            #continue
        #if 'X' in aspects:
            #continue
        
        #if len(aspects) == 1 and ('produto' in aspects or 'PRODUTO' in aspects or '_GENERIC' in aspects): 
            #if len(sample['text_info']) <= 3: 
                #continue
        
        
        general_pol = 0 # Will define general polarity of sentence
        for opinion in sample['opinions']:
            general_pol += opinion[1]
        if general_pol < 0:
            pol = '-'
        elif general_pol > 0:
            pol = '+'
        else:
            continue # Ignores neutral opinions 
        
        #text_info = process_sentence(sample['sentence'])
        
        n = {}
        n['text_info'] = sample['text_info'] 
        n['id'] = sample_id
        
        r[pol].append(n)
    
    return r
    






def load_dataset_DEPREC():
    # structure that stores the raw and processed sentences for both polarities positive and negative
    datasets = {}
    for target in [TARGET1, TARGET2]:
        datasets[target] = {
            'raw': {'+': [], '-': []},
            'processed': {'+': [], '-': []},
            'IDs': {'+': {}, '-': {}} # Used to keep sentences' original IDs. 
        }
    for target in [TARGET1, TARGET2]: 
        
        with open(PAR[target], encoding='utf-8') as fp_dataset:
            
            for line in fp_dataset:
                
                if len(line) < 3:
                    continue
                if line[0] == '#':
                    continue
                              
                polarity = int(line[1])
                
                opinion_id = int(line.split()[1])

                sentence = ' '.join(((line.split())[3:]))

                # adding the unprocessed sentence to the set
                datasets[target]['raw'][['-', '+'][polarity]].append([sentence, opinion_id])
                
                # saving the sentence original ID
                id_sequential = len(datasets[target]['raw'][['-', '+'][polarity]])-1
                datasets[target]['IDs'][['-', '+'][polarity]][id_sequential] = opinion_id

                sentence_proc = process_sentence(sentence)
                            
                # adding the processed sentence to the set
                datasets[target]['processed'][['-', '+'][polarity]].append(sentence_proc)                 
                                            
                save_noadj(sentence)
                
    return datasets




