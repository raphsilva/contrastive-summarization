import math

import method

import structure as struct

import output_format as out

from pprint import pprint

#INFINITY = math.inf
INFINITY = 999999

from setup import LIM_SENTENCES
from setup import LIM_WORDS

from setup import GREEDY_CANDS_SELECTED
from setup import VERBOSE_MODE

from setup import DEBUGGING

from setup import METHOD

import random

RANDOM_SEED = 4

RANDOMIZE_DRAW = False # If two candidates have the same score, chooses random (if true) or chooses the last found (false)

def random_seed():
    global RANDOM_SEED
    RANDOM_SEED = random.randint(0,10000)
    #RANDOM_SEED = 4


from setup import KEY_MEASURE

def makeSummary(source, original_stats, method='greedy', LIM_WORDS=LIM_WORDS):
    if method == 'brute':
        return makeSummary_brute(source, original_stats)
    elif method == 'fast':
        return makeSummary_fast(source, original_stats)
    elif method == 'greedy':
        return makeSummary_greedy(source, original_stats, LIM_WORDS)
    


def MakeContrastiveSummary(t1, t2, d1, d2, method='greedy', LIM_WORDS_1=LIM_WORDS, LIM_WORDS_2=LIM_WORDS):
    if method == 'greedy': 
        return MakeContrastiveSummary_greedy(t1, t2, d1, d2, LIM_WORDS_1, LIM_WORDS_2)
    elif method == 'random': 
        return MakeContrastiveSummary_random(t1, t2)
    if method == 'brute':
        return MakeContrastiveSummary_brute(t1, t2, d1, d2)
    if method == 'fast':
        return MakeContrastiveSummary_fast(t1, t2, d1, d2)



def MakeContrastiveSummary_random(source1, source2):
    from random import sample
    
    idx1 = source1.keys()
    idx2 = source2.keys()
    
    idx_cand_1 = sample(idx1, LIM_SENTENCES)
    idx_cand_2 = sample(idx2, LIM_SENTENCES)
    
    summ_cand_1 = struct.idx_to_summ(source1, idx_cand_1)
    summ_cand_2 = struct.idx_to_summ(source2, idx_cand_2)
    
    while struct.word_count(summ_cand_1) > LIM_WORDS and len(idx_cand_1) > 0:
        idx_cand_1 = idx_cand_1[:-1]
        summ_cand_1 = struct.idx_to_summ(source1, idx_cand_1)
    while struct.word_count(summ_cand_2) > LIM_WORDS and len(idx_cand_2) > 0:
        idx_cand_2 = idx_cand_2[:-1]
        summ_cand_2 = struct.idx_to_summ(source2, idx_cand_2)
            
    return idx_cand_1, idx_cand_2
    






def MakeContrastiveSummary_C(source1, source2, stats_source_1, stats_source_2, LIM_WORDS_1=LIM_WORDS, LIM_WORDS_2=LIM_WORDS):
    
    candidate_options_1 = sorted(list(source1.keys()))
    candidate_options_2 = sorted(list(source2.keys())) 
    random.seed(RANDOM_SEED)
    random.shuffle(candidate_options_1)
    random.shuffle(candidate_options_2)
    
    #scores = {}
    
    #for i in candidate_options_1:
        #for j in candidate_options_2:            
            
            #idx_cand_1 = [i]                
            #summ_cand_1 = struct.idx_to_summ(source1, idx_cand_1)                
            #stats_cand_1 = struct.aspects_stats(summ_cand_1, KEY_MEASURE)
            
            #idx_cand_2 = [j]                
            #summ_cand_2 = struct.idx_to_summ(source2, idx_cand_2)                
            #stats_cand_2 = struct.aspects_stats(summ_cand_2, KEY_MEASURE)
            
            #sC = method.score_C(stats_source_1, stats_source_2, stats_cand_1, stats_cand_2)
            ##sR = method.score_R(stats_source_1, stats_source_2, stats_cand_1, stats_cand_2)
            ##sD = method.score_D(stats_source_1, stats_source_2, stats_cand_1, stats_cand_2)
            
            #s = sC  
            
            ##if s == 0:
                ##continue
            
            #scores[(i,j)] = s
            
    #rank = sorted(scores.keys(), key=lambda i: scores[i], reverse=True)
    

    if METHOD == 'C':
        rank_1, rank_2 = method.rank_C(stats_source_1, stats_source_2)
    if METHOD == 'R':
        rank_1, rank_2 = method.rank_R(stats_source_1, stats_source_2)
    if METHOD == 'D':
        rank_1, rank_2 = method.rank_D(stats_source_1, stats_source_2)

    
    idx_summ_1 = []
    idx_summ_2 = []
    
    for i in rank_1:
        
        if i in idx_summ_1:
            continue
        
        idx_cand_1 = list(idx_summ_1) + [i]
        
        cand_1 = struct.idx_to_summ(source1, idx_cand_1)  
        
        size_cand_1 = struct.word_count(cand_1)
        
        if size_cand_1 <= LIM_WORDS_1:
            idx_summ_1 = list(idx_cand_1)
            
        if len(idx_summ_1) >= LIM_SENTENCES:
            break
            
            
    for i in rank_2:
        
        if i in idx_summ_2:
            continue
        
        idx_cand_2 = list(idx_summ_2) + [i]
        
        cand_2 = struct.idx_to_summ(source2, idx_cand_2)  
        
        size_cand_2 = struct.word_count(cand_2)
        
        if size_cand_2 <= LIM_WORDS_2:
            idx_summ_2 = list(idx_cand_2)
            
        if len(idx_summ_2) >= LIM_SENTENCES:
            break
            
            
    #for i, j in rank:
        
        #if i in idx_summ_1 or j in idx_summ_2:
            #continue
        
        ##print(p)
        
        ##i = p[0]
        ##j = p[1]
        
        #idx_cand_1 = list(idx_summ_1) + [i]
        #idx_cand_2 = list(idx_summ_2) + [j]
        
        #cand_1 = struct.idx_to_summ(source1, idx_cand_1)  
        #cand_2 = struct.idx_to_summ(source2, idx_cand_2)  
        
        #size_cand_1 = struct.word_count(cand_1)
        #size_cand_2 = struct.word_count(cand_2)
        
        #if size_cand_1 <= LIM_WORDS_1 and size_cand_2 < LIM_WORDS_2:
            #idx_summ_1 = list(idx_cand_1)
            #idx_summ_2 = list(idx_cand_2)
        
      
    return idx_summ_1, idx_summ_2
    
    pprint(rank)
    
    exit()






def MakeContrastiveSummary_greedy(source1, source2, stats_source_1, stats_source_2, LIM_WORDS_1=LIM_WORDS, LIM_WORDS_2=LIM_WORDS):
    
    
    return MakeContrastiveSummary_C(source1, source2, stats_source_1, stats_source_2, LIM_WORDS_1, LIM_WORDS_2)
    
    #SPEED = 'CAREFUL'
    SPEED = 'FAST'
    
    #if SPEED == 'FAST':
        #GREEDY_CANDS_SELECTED = 1
    #else:
        #from setup import GREEDY_CANDS_SELECTED
    
    #return MakeContrastiveSummary_greedy_DEPREC(source1, source2, stats_source_1, stats_source_2, LIM_SENTENCES, LIM_WORDS)


    best_score = -INFINITY

    total_candidates = len(source1) * len(source2) # number of new candidates at each iteration

    top_candidates = [(([],[]),-INFINITY)]
    
    candidate_options_1 = sorted(list(source1.keys()))
    candidate_options_2 = sorted(list(source2.keys())) 
    random.seed(RANDOM_SEED)
    random.shuffle(candidate_options_1)
    random.shuffle(candidate_options_2)
    
    for s in range(1, LIM_SENTENCES+1): 
        
        
        if len(top_candidates[0][0][0]) < s-1 and len(top_candidates[0][0][1]) < s-1:
            #pprint(top_candidates)
            print()
            out.printMessage('\nWon\'t find any larger summary', s)
            break
                
        search_paths = len(top_candidates)
        c_searched_paths = 0
        
        best_for_size_prev = [i[0] for i in top_candidates]
        
        for best_prev in best_for_size_prev:
            c_searched_paths += 1      

            idx_best_for_size1 = best_prev[0]
            idx_best_for_size2 = best_prev[1]
            
            c = 0
            
            
            
            for i in candidate_options_1:    
                
                c += 1
                #if GREEDY_CANDS_SELECTED != 0:
                
                if not DEBUGGING:
                    pr = (s-1)/LIM_SENTENCES + (c_searched_paths-1)/search_paths/LIM_SENTENCES + c/len(source1)/search_paths/LIM_SENTENCES
                    out.printProgress (" %6.2lf%%   ( path %3d/%d  of  size  %2d/%d )  %16.2lf     (%d %d)" % (100*pr, c_searched_paths, search_paths, s, LIM_SENTENCES, best_score, len(idx_best_for_size1), len(idx_best_for_size2)), end="\r")
                    out.printdebug()
                
                
                if i in idx_best_for_size1: 
                    continue # Opinion already chosen.
                
                idx_cand_1 = idx_best_for_size1 + [i]
                
                summ_cand_1 = struct.idx_to_summ(source1, idx_cand_1)
                
                
                
                
                
                size_cand_1 = struct.word_count(summ_cand_1)
                
                #if SPEED == 'FAST':
                if size_cand_1 > LIM_WORDS_1: 
                    continue # Candidate not considered because it is too long.
                
                stats_cand_1 = struct.aspects_stats(summ_cand_1, KEY_MEASURE)
                
                if SPEED == 'CAREFUL':
                    idx_cand_1_0 = idx_best_for_size1
                    summ_cand_1_0 = struct.idx_to_summ(source1, idx_best_for_size1) # Option to keep last summary (and change the other side)
                    stats_cand_1_0 = struct.aspects_stats(summ_cand_1_0, KEY_MEASURE)
                # If there's not enough data to calculate stdev
                #for i in stats_cand_1: 
                    #if stats_cand_1[i]['std'] == None: 
                        #stats_cand_1[i]['std'] = 0 #stats_source_1[i]['std']
                
                   
                    
                for j in candidate_options_2: 
                    
                    #if GREEDY_CANDS_SELECTED == 0:
                        #pr = pr_cur/pr_tot
                        #out.printProgress ("  %.2lf%%    %10.2lf" % (100*pr, best_score), end="\r")
                        #pr_cur += 1
                    
                    
                    
                    
                    if j in idx_best_for_size2: 
                        continue 
                    
                    idx_cand_2 = idx_best_for_size2 + [j] 
                    summ_cand_2 = struct.idx_to_summ(source2, idx_cand_2)
                    
                    size_cand_2 = struct.word_count(summ_cand_2)
                    
                    
                    #if SPEED == 'FAST':
                    if size_cand_2 > LIM_WORDS_2: 
                        continue
                    
                    
                    
                    
                    
                    stats_cand_2 = struct.aspects_stats(summ_cand_2, KEY_MEASURE)
                    
                    if SPEED == 'CAREFUL':
                        idx_cand_2_0 = idx_best_for_size2
                        summ_cand_2_0 = struct.idx_to_summ(source2, idx_best_for_size2)
                        stats_cand_2_0 = struct.aspects_stats(summ_cand_2_0, KEY_MEASURE)
                    # If there's not enough data to calculate stdev
                    #for i in stats_cand_2: 
                        #if stats_cand_2[i]['std'] == None: 
                            #stats_cand_2[i]['std'] = 0 #stats_source_2[i]['std']    
                    
                    
                    score = method.score(stats_source_1, stats_source_2, stats_cand_1, stats_cand_2)#*((len(idx_cand_1)+len(idx_cand_2))**0.1)
                    
                    if SPEED == 'CAREFUL':
                        score_01 = method.score(stats_source_1, stats_source_2, stats_cand_1_0, stats_cand_2)#*((len(idx_cand_1)+len(idx_cand_2))**0.1)
                        score_10 = method.score(stats_source_1, stats_source_2, stats_cand_1, stats_cand_2_0)#*((len(idx_cand_1)+len(idx_cand_2))**0.1)
                        
                        #print(score, score_01, score_10)
                        
                        m = max(score, score_01, score_10)
                        
                        #if score == m:
                            #pass
                        if score_01 > score:
                            score = score_01
                            idx_cand_1 = idx_cand_1_0
                            size_cand_1 = struct.word_count(summ_cand_1_0)
                        if score_10 > score:
                            score = score_10
                            idx_cand_2 = idx_cand_2_0
                            size_cand_2 = struct.word_count(summ_cand_2_0)
                        
                        
                    if size_cand_1 + size_cand_2 > (LIM_WORDS_1 + LIM_WORDS_2):
                        continue
     
                    #score /= LIM_SENTENCES # Normalize by limit of sentences (doesn't affect anything, only makes it prettier)
                    
                    #out.printdebug("   candidates:  ", idx_cand_1, idx_cand_2)        
                    #out.printdebug("   score: ", score)
                    #out.printdebug("   sizes: ", size_cand_1, size_cand_2)
                    #out.printdebug()
                    
                    #if score > best_score: 

                        #best_score = score
                        
                        ##idx_best_for_size[s] = [(idx_cand_1, idx_cand_2)]
                        
                        #top_candidates = [((idx_cand_1, idx_cand_2), score)]
                        
                        ##idx_best_for_size1[s] = idx_cand_1
                        ##idx_best_for_size2[s] = idx_cand_2                
                        
                        ## Display information
                        #out.printdebug("   best candidates:  ", idx_cand_1, idx_cand_2)        
                        #out.printdebug("   score: ", score)
                        #out.printdebug("   sizes: ", size_cand_1, size_cand_2)
                        #out.printdebug()
                     
                    
                    
                    #out.printdebug("   length top cands ", len(top_candidates), 0.001*total_candidates)
                    #out.printdebug()
                    
                    prob = 10/(max(len(source1),len(source2)))
                    draw = random.uniform(0,1)
                    
                    #if score == top_candidates[0][-1] :
                        #print(draw)
                        #print(prob)
                        #print()
                        
                    if len(top_candidates) < GREEDY_CANDS_SELECTED:
                        
                        top_candidates.append(((idx_cand_1, idx_cand_2), score))
                        top_candidates = sorted(top_candidates, key=lambda x: x[1], reverse=True)
                        
                        out.printdebug("   ADDING TO FILL ", idx_cand_1, idx_cand_2)
                        out.printdebug("   score: ", score)
                        out.printdebug("   best: ", best_score)
                        out.printdebug("   sizes: ", size_cand_1, size_cand_2)
                        out.printdebug()
                    
                    #elif score > top_candidates[0][-1] or (not RANDOMIZE_DRAW and score == top_candidates[0][-1]) or (RANDOMIZE_DRAW and score == top_candidates[0][-1] and draw<prob): 
                    elif score >= top_candidates[0][-1]: 
                        x = len(top_candidates) - 1
                        while x > 0 and top_candidates[x][1] < score:
                            x -= 1
                        
                        top_candidates.insert(x, ((idx_cand_1, idx_cand_2), score))
                        
                        del top_candidates[-1]
                        
                        out.printdebug("   best candidates:  ", idx_cand_1, idx_cand_2)        
                        out.printdebug("   score: ", score)
                        out.printdebug("   sizes: ", size_cand_1, size_cand_2)
                        out.printdebug()
                        
                    best_score =  top_candidates[0][1]
                        
                        
                    #print(top_candidates)
                    #input()
                    
                    #elif score > OPTM_GREEDY_TOLERANCE * best_score: 
                        #out.printdebug("   GOT A DRAW ", idx_cand_1, idx_cand_2, score)
                        #out.printdebug("   best: ", best_score)
                        #out.printdebug("   sizes: ", size_cand_1, size_cand_2)
                        #out.printdebug()
                        #idx_best_for_size[s].append((idx_cand_1, idx_cand_2))
                        
                        #if len(idx_best_for_size[s]):
                            #pprint(idx_best_for_size[s])
                            #input()
                            
            #idx_best_for_size[s] = [i[0] for i in top_candidates]


        
    
    #out.printMessage('Sumários empatados: ', len(idx_best_for_size[LIM_SENTENCES]))
    
    if VERBOSE_MODE:
        out.printinfo('Best score: ', best_score)
            
    #print(top_candidates)
    #print(idx_best_for_size)
            
    best_summ1 = top_candidates[0][0][0]
    best_summ2 = top_candidates[0][0][1]
    
    return best_summ1, best_summ2 

    # End of greedy algorithm to find best summary
    
    
    




def makeSummary_greedy (source, stats_source, LIM_WORDS=LIM_WORDS):
    
    #return makeSummary_greedy_DEPREC (source, stats_source)
            
    best_score = -INFINITY 
    
    total_candidates = len(source)
    
    top_candidates = [([],-INFINITY)]

    idx_best_for_size = {}
    idx_best_for_size[0] = []
    
    
    candidate_options = sorted(list(source.keys()))            
    random.seed(RANDOM_SEED)
    random.shuffle(candidate_options)
    
    print(candidate_options[:10])


    for s in range(1, LIM_SENTENCES+1): 
        
        #print('-----', s)
                
        if len(top_candidates[0][0]) < s-1:
            if VERBOSE_MODE:
                print()
                pprint(top_candidates)
                out.printMessage('\nWon\'t find any larger summary', s)
            break
        
        #idx_best_for_size[s] = idx_best_for_size[s-1]
        
        best_for_size_prev = [i[0] for i in top_candidates]
        
        search_paths = len(top_candidates)
        c_searched_paths = 0
                
        for best_prev in best_for_size_prev:
            c_searched_paths += 1  
            
            idx_best_for_size = best_prev
            
            
            c = 0
            
            
        
            for i in candidate_options: 
                c += 1
                pr = (s-1)/LIM_SENTENCES + (c_searched_paths-1)/search_paths/LIM_SENTENCES + c/len(source)/search_paths/LIM_SENTENCES
                out.printProgress (" %6.2lf%%   ( path %3d/%d  of  size  %2d/%d )  %16.2lf" % (100*pr, c_searched_paths, search_paths, s, LIM_SENTENCES, best_score), end="\r")
                
                                
                #pprint(source[candidate_opinion])
                sent_density = source[i]['intensity']['aspects']/source[i]['word_count']
                #print(sent_density)
                #input()
                
                if i in idx_best_for_size: # Candidate opinion already in the summary
                    continue 
                
                idx_cand = idx_best_for_size + [i] 
                
                summ_cand = struct.idx_to_summ(source, idx_cand)
                
                
                size_cand = struct.word_count(summ_cand)
                
                if size_cand > LIM_WORDS:
                    continue
                
                stats_cand = struct.aspects_stats(summ_cand, KEY_MEASURE)
                
                #sum_prob_sum = 0
                #for i in stats_cand:
                    #sum_prob_sum += stats_cand[i]['prob']
                    
                
                #input()

                    

                
                
                #for i in stats_cand:
                    #stats_cand[i]['prob'] /= (LIM_SENTENCES)

                
                score = method.SAM(stats_source, stats_cand)
                
                #score /= LIM_SENTENCES # Normalize by limit of sentences (doesn't affect anything, only makes it prettier)
                
                
                ##pprint(summ_cand)
                ##print()
                #pprint(stats_source)
                #print()
                #pprint(stats_cand)
                #print()
                #print(score)
                #print()
                #print()
                #print()
                #print()
                #input()
                
                
                #prob = 10/len(source)
                #draw = random.uniform(0,1)*0
                
                #print(i)
                
                if len(top_candidates) < GREEDY_CANDS_SELECTED: # There's space for more candidates
                            
                    top_candidates.append((idx_cand, score))
                    top_candidates = sorted(top_candidates, key=lambda x: x[1], reverse=True)
                    
                    out.printdebug()
                    out.printdebug("   ADDING TO FILL ", idx_cand)
                    out.printdebug("   score: ", score)
                    out.printdebug("   best: ", best_score)
                    out.printdebug("   size: ", size_cand)
                    out.printdebug()
                
                    #print('filling: ', idx_cand)
                
                
                #elif score > top_candidates[0][-1] or (not RANDOMIZE_DRAW and score == top_candidates[0][-1]) or (RANDOMIZE_DRAW and score == top_candidates[0][-1] and draw<prob): 
                
                
                
                elif score >= top_candidates[0][-1]:
                    
                    #if len(idx_cand) > 3:
                    #print('best: ', idx_cand)
                    #print(score)
                    #print()
                    
                
                    
                    
                    # If score is best than the worst top candidate, the worse is replaced by the new.
                    # If score is equal than the worst top candidate, it may be replaced or not based on random decision
                    
                    #del top_candidates[-1]
                    #top_candidates.append(((idx_cand_1, idx_cand_2), score))
                    
                    x = len(top_candidates) - 1
                    while x > 0 and top_candidates[x][1] < score:
                        x -= 1
                    
                    top_candidates.insert(x, (idx_cand, score))
                    
                    del top_candidates[-1]
                    
                    #top_candidates[-1] = ((idx_cand_1, idx_cand_2), score)
                    #top_candidates = sorted(top_candidates, key=lambda x: x[1], reverse=True)
                    
                    out.printdebug()
                    out.printdebug("   best candidate:  ", idx_cand)        
                    out.printdebug("   score: ", score)
                    out.printdebug("   size: ", size_cand)
                    out.printdebug()
                    
                   
                best_score =  top_candidates[0][1]
                
                #if score >= best_score: 
                    #best_score = score
                    #idx_best_for_size[s] = idx_cand
                    
                    #out.printdebug ('*', idx_cand, score)
                    
                #else:
                    #out.printdebug (idx_cand, score)
                
                #pprint(stats_cand)
                #pprint(stats_source)

    best_idx = top_candidates[0][0]
    
    return best_idx









def MakeContrastiveSummary_brute(source1, source2, stats_source_1, stats_source_2):

    import itertools

    best = -INFINITY 
    best_summ1 = []
    best_summ2 = []

    p = 0
    
    tg1 = len(source1)+(LIM_SENTENCES-1) # Includes possibilities of none
    tg2 = len(source2)+(LIM_SENTENCES-1)
    togo = 1
    for i in range(LIM_SENTENCES):
        togo *= tg1
        tg1 -= 1
    for i in range(LIM_SENTENCES):
        togo *= tg2
        tg2 -= 1
    print("togo = ", togo, len(source1), len(source2), LIM_SENTENCES)

    for L1 in range(0, LIM_SENTENCES+1):
        
        for subset1 in itertools.combinations(list(source1.keys()), L1):
            
            if len(subset1) == 0:
                continue
            if len(subset1) > LIM_SENTENCES:
                break
            
            for L2 in range(0, LIM_SENTENCES+1):            
                for subset2 in itertools.combinations(list(source2.keys()), L2):
                    
                    if len(subset2) == 0:
                        continue
                    if len(subset2) > LIM_SENTENCES:
                        break
                    
                    cand1 = {i: source1[i] for i in subset1}
                    cand2 = {i: source2[i] for i in subset2}
                    
                    if struct.word_count(cand1) > LIM_WORDS:
                        continue
                    if struct.word_count(cand2) > LIM_WORDS:
                        continue
                    
                    summ_cand_1 = struct.idx_to_summ(source1, cand1)
                    summ_cand_2 = struct.idx_to_summ(source2, cand2)
                    
                    stats_cand_1 = struct.aspects_stats(summ_cand_1, KEY_MEASURE)
                    stats_cand_2 = struct.aspects_stats(summ_cand_2, KEY_MEASURE)
                                      
                    score = method.score(stats_source_1, stats_source_2, stats_cand_1, stats_cand_2)
                    
                    score /= LIM_SENTENCES # Normalize by limit of sentences (doesn't affect anything, only makes it prettier)
                    
                    
                    p += 1
                    if p%1000 == 0: 
                        pr = float(p/togo)
                        out.printProgress("  %6.2lf%%   %10s %10s   %6.2lf   /   %10s %10s %6.2lf" % (100*pr, subset1, subset2, score, best_summ1, best_summ2, best))
                    
                    if score >= best: 
                        best = score
                        best_summ1 = subset1
                        best_summ2 = subset2
        
        
    sum1 =  getSum(source1, list(best_summ1))
    sum2 =  getSum(source2, list(best_summ2))
        
        
    return best_summ1, best_summ2 








def makeSummary_brute(source, stats_source):

    import itertools
    from scipy.special import comb 
    
    best_score = -INFINITY 
    best_idx = []
        
    # Variables to display progress
    pr_cur = 0
    pr_tot = 0
    for i in range(1, LIM_SENTENCES+1):
        pr_tot += comb(len(source), i) # Counts all possible combinations
    
    
    for L1 in range(1, LIM_SENTENCES+1): # For each possible size of summary
        
        for idx_cand in itertools.combinations(list(source.keys()), L1): # For each possible subset of that size

            summ_cand = struct.idx_to_summ(source, idx_cand)
            
            stats_cand = struct.aspects_stats(summ_cand, KEY_MEASURE)
                                            
            score = method.SAM(stats_source, stats_cand)
            
            score /= LIM_SENTENCES # Normalize by limit of sentences (doesn't affect anything, only makes it prettier)
            
            if score >= best_score: 
                best_score = score
                best_idx = idx_cand
            
            # Display progress information
            pr_cur += 1
            pr = pr_cur/pr_tot
            if pr_cur%100 == 0: 
                out.printProgress("  %6.2lf%% " % (100*pr), end="\r")
                out.printdebug(" cur subset: %20s   score:  %6.2lf   /  best subset: %10s  score: %6.5lf" % (idx_cand, score, best_idx, best_score))
            
                    
    return best_idx








def makeSummary_fast(source, stats_source):
    
    best_score = -INFINITY 
    
    idx_best = []
    
    score_gain = [[i, -INFINITY] for i in source]
    
   
    for s in range(1, LIM_SENTENCES+1): 
        
        #pprint(idx_best)
        #pprint(score_gain)
        
        best_score_prev = best_score
        idx_best_prev = idx_best
        
        if len(idx_best_prev) < s-1:
            #print('not finding best', len(idx_best_prev), s-1)
            break
        
        
        #m_gain = max(score_gain.values())
        #lim_gain = sorted([i[1] for i in score_gain], reverse=True)[int(len(score_gain)/2)]
        #if m_gain > 0:
            #min_gain = 0.9*m_gain
        #else:
            #min_gain = 1.1*m_gain
                
        score_gain = sorted(score_gain, key=lambda x : x[1], reverse=True)                
        
        for i in range(int(len(score_gain))): 
            
            # If already chose a new element for the summary, doesn't continue searching
            if len(idx_best_prev) >= 1 and len(idx_best) > len(idx_best_prev):
                break
            
            #print(c)
            
            p = score_gain[i]
            
            c = p[0]
                         
            
            #if score_gain[c] < lim_gain:
                ##print ('skipping')
                #continue
            
            #print ('%5d  :  %10d ' % (c, p[1]))
            
            idx_cand = idx_best_prev + [c]
            
            summ_cand = struct.idx_to_summ(source, idx_cand)
            
            size_cand = struct.word_count(summ_cand)
            
            if size_cand > LIM_WORDS:
                continue
            
            stats_cand = struct.aspects_stats(summ_cand, KEY_MEASURE)
            
            score = method.SAM(stats_source, stats_cand)
            
            #score /= LIM_SENTENCES # Normalize by limit of sentences (doesn't affect anything, only makes it prettier)
            
            g = score - best_score_prev 
            score_gain[i][1] += g
            
            if score > best_score:
                best_score = score
                idx_best = idx_cand 
    return idx_best



def MakeContrastiveSummary_fast(source1, source2, stats_source1, stats_source2):
    
    best_score = -INFINITY 
    
    idx_best1 = []
    idx_best2 = []
    
    score_gain1 = [[i, -INFINITY] for i in source1]
    score_gain2 = [[i, -INFINITY] for i in source2]
    
   
    for s in range(1, LIM_SENTENCES+1): 
        
        #pprint(idx_best)
        #pprint(score_gain)
        
        best_score_prev = best_score
        idx_best_prev1 = idx_best1
        idx_best_prev2 = idx_best2
        
        if max(len(idx_best_prev1), len(idx_best_prev2)) < s-1:
            #print('not finding best', len(idx_best_prev), s-1)
            break
        
        
        #m_gain = max(score_gain.values())
        #lim_gain = sorted([i[1] for i in score_gain], reverse=True)[int(len(score_gain)/2)]
        #if m_gain > 0:
            #min_gain = 0.9*m_gain
        #else:
            #min_gain = 1.1*m_gain
                
        score_gain1 = sorted(score_gain1, key=lambda x : x[1], reverse=True)                
        score_gain2 = sorted(score_gain2, key=lambda x : x[1], reverse=True)                
        
        for i in range(int(len(score_gain1))): 
            
            pr = (s-1)/LIM_SENTENCES + i/len(score_gain1)/LIM_SENTENCES
            out.printProgress("  %6.2lf%% " % (100*pr), end='\r')
            
            if len(idx_best_prev1) >= 1 and len(idx_best1) > len(idx_best_prev1):
                break
            
            #print(c)
            
            p1 = score_gain1[i]
            
            cand1 = p1[0]
            
            if cand1 in idx_best1:
                continue
            
            idx_cand1 = list(idx_best_prev1) + [cand1]
            
            summ_cand1 = struct.idx_to_summ(source1, idx_cand1)
            
            size_cand1 = struct.word_count(summ_cand1)
            
            if size_cand1 > LIM_WORDS:
                continue
            
            
            
            stats_cand1 = struct.aspects_stats(summ_cand1, KEY_MEASURE)
            
            
            for j in range(int(len(score_gain2))): 
                
                
                #pr = i/len(score_gain1) + j/len(score_gain2)/len(score_gain1)
                #out.printProgress("  %3d%% " % (100*pr), end='\r')
                
            
                if len(idx_best_prev2) >= 1 and len(idx_best2) > len(idx_best_prev2):
                    break
                
                #print(c)
                
                p2 = score_gain2[j]
                
                cand2 = p2[0]
                
                if cand2 in idx_best2:
                    continue
                
                idx_cand2 = list(idx_best_prev2) + [cand2]
                
                summ_cand2 = struct.idx_to_summ(source2, idx_cand2)
                
                size_cand2 = struct.word_count(summ_cand2)
                
                if size_cand1 + size_cand2 > LIM_WORDS:
                    continue
                
                stats_cand2 = struct.aspects_stats(summ_cand2, KEY_MEASURE)
                                
                score = method.score(stats_source1, stats_source2, stats_cand1, stats_cand2)
                        
                score /= LIM_SENTENCES # Normalize by limit of sentences (doesn't affect anything, only makes it prettier)
            
                g = score - best_score_prev 
                score_gain2[j][1] += g
                score_gain1[i][1] += g/len(score_gain2)
            
                if score > best_score:
                    best_score = score
                    idx_best1 = idx_cand1
                    idx_best2 = idx_cand2
                
      
    print()  
    return idx_best1, idx_best2
                
            
            
            
            
        
