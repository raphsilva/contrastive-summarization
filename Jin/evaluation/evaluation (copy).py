MAXSENT = 100




from pprint import pprint

#from LermanFunctions import *
#import method

import structure as struct


BYPASS_ASPECTS = []


def get_opinions(source, KEYMEASURE='corpus'):
    
    return [(item[0], trinary_polarity(item[1])) for sublist in [source[j]['opinions'] for j in source] for item in sublist if item[0] not in BYPASS_ASPECTS]
    
    
    r = []
    for j in source:
        for aspect in source[j]['sent'][KEYMEASURE]:
            
            polarity = trinary_polarity(source[j]['sent'][KEYMEASURE][aspect])
            
            if aspect in BYPASS_ASPECTS:
                continue
            
            #if polarity == 0:
                #continue
            
            r.append((aspect, polarity))
            
    
    return r


def representativiness(source, summ):
    
    points = 0
    
    opinions_source = get_opinions(source)
    opinions_summ = get_opinions(summ)
    
    #pprint(sorted(opinions_source))
    
    
    for o in opinions_source:
        for u in opinions_summ:
            if o[0] == u[0] and trinary_polarity(o[1]) ==  trinary_polarity(u[1]):
                #print(o, u)
                points += 1
                break
    
    return points/len(opinions_source)


    
    
def trinary_polarity(num):
            
    if num < -25:
        return -1
    if num > 25:
        return +1
    return 0
    
    
    






def diversity(source, summ):
    
    opinions_source = get_opinions(source)
    opinions_summ = get_opinions(summ)
    
    opinions_source = list(set(opinions_source)) # Remove duplicates
    opinions_summ = list(set(opinions_summ))
    
    #pprint(opinions_source)
    #pprint(opinions_summ)
    #print()
    
    return len(opinions_summ)/len(opinions_source)




    
def contrastiviness(source1, source2, summ1, summ2):
    
    
    opinions_source1 = get_opinions(source1)
    opinions_source2 = get_opinions(source2)
    
    opinions_summ1 = get_opinions(summ1)
    opinions_summ2 = get_opinions(summ2)
    
    points = 0
    
    # Compares source 1 with summ 2 and vice-versa.
    for opinions_source, opinions_opposite_source, opinions_summ, opinions_opposite_summ in zip([opinions_source1, opinions_source2], [opinions_source2, opinions_source1], [opinions_summ1, opinions_summ2], [opinions_summ2, opinions_summ1]):
        
        all_possibles = []
        
        for op1 in opinions_source:
            for op2 in opinions_opposite_source:
                pol1 = (op1[1])
                pol2 = (op2[1])
                if op1[0] == op2[0] and pol1 == -pol2 and pol1 != 0:
                    asp_cont = (op1[0], pol1, pol2) # This aspect has the possibility to form a possible contrastive pair. 

                    if asp_cont not in all_possibles:
                        all_possibles.append(asp_cont)
     
        pairs_formed = []
        
        debug_found_1 = []
        debug_found_2 = []
        
        c = 0
        for p in all_possibles:
            if (p[0], p[1]) in opinions_summ:
                c += .5
                
                if (p[0], p[1]) not in debug_found_1:
                    debug_found_1.append((p[0], p[1]))
                
            if (p[0], p[2]) in opinions_opposite_summ:
                c += .5
                
                if (p[0], p[2]) not in debug_found_2:
                    debug_found_2.append((p[0], p[2]))
                    
        
                
        #pprint(all_possibles)
        #print()
        #pprint(debug_found_1)
        #print()
        #pprint(debug_found_2)
        #print()
        #print()
        #print()
        #input()
                
        points += c/len(all_possibles)
        
        #for op1 in opinions_source:
            #for op2 in opinions_opposite_summ:
                #pol1 = (op1[1])
                #pol2 = (op2[1])
                #if op1[0] == op2[0] and pol1 == -pol2:
                    #asp_cont = (op1[0], pol1, pol2) # This aspect has the possibility to form a possible contrastive pair. 
                    #if asp_cont not in pairs_formed:
                        #pairs_formed.append(asp_cont)
                #elif op1[0] == op2[0]:
                    #print('**', op1, op2)
     
             
             
        #points += len(pairs_formed)/len(all_possibles)
        
        #points += p/max_possible 
    
    ##print(points)
    
    #points /= max_possible

    
    return points/2

    
    
def BAK_contrastiviness(source1, source2, summ1, summ2):
    
    opinions_source1 = [item for sublist in [source1[j]['opinions'] for j in source1] for item in sublist]
    opinions_source2 = [item for sublist in [source2[j]['opinions'] for j in source2] for item in sublist]
    
    opinions_summ1 = [item for sublist in [summ1[j]['opinions'] for j in summ1] for item in sublist]
    opinions_summ2 = [item for sublist in [summ2[j]['opinions'] for j in summ2] for item in sublist]
    
    points = 0
    
    
    
    
                
    #for opinions1 in opinions_source1:
        #m = [0]
        #for opinions2 in opinions_source2:
            #if opinions1[0] == opinions2[0]:
                #m.append(abs(opinions1[1] - opinions2[1]))
        #max_possible += max(m)
                
    #for opinions2 in opinions_source2:
        #m = [0]
        #for opinions1 in opinions_source1:
            #if opinions1[0] == opinions2[0]:
                #m.append(abs(opinions1[1] - opinions2[1]))
        #max_possible += max(m)
    
    #max_possible /= 2
                
        
                #print(max_possible)
                #print(opinions1)
                #print(opinions2)
                #print()
    
    #exit()
        
    
    # Compares source 1 with summ 2 and vice-versa.
    for opinions_source, opinions_opposite_source, opinions_opposite_summ in zip([opinions_source1, opinions_source2], [opinions_source2, opinions_source1], [opinions_summ2, opinions_summ1]):
    
    
        
        
        #pprint(opinions_source)
        #pprint(opinions_summ)
        
        #print()
        #print()
        #print()
        
        max_possible = 0
        
        for opinions1 in opinions_source:
            for opinions2 in opinions_opposite_source:
                if opinions1[0] == opinions2[0] and opinions1[1] * opinions2[1] < 0:
                    max_possible += 1
                    #break
                
        p = 0
        
        for o in opinions_source:
            for u in opinions_opposite_summ:
                if o[0] == u[0] and o[1] * u[1] < 0:
                    p += 1
                    #break
                #if o[0] == u[0]:
                    #points += abs(o[1] - u[1])
        
        points += p/max_possible 
    
    ##print(points)
    
    #points /= max_possible

    
    return points/2




############# IMPLEMENTING ########################





def representativeness_sim(set1, set2, summ):
    """
    The representativeness of a contrastive opinion summary S, denoted as r(S), measures how well the summary S represents the opinions expressed by the sentences in both X and Y .
    :return: [float] representativeness of the generated summary.
    """
    
    #pprint(set1)
    #for i in set1:
        #print("olha")
        #pprint(i)
        #print(i['text_info'])
    #input()
    
    source1_text_info = [s['text_info'] for s in set1]
    source2_text_info = [s['text_info'] for s in set2]
    
    summ1_text_info = [s['text_info'] for s in [i[0] for i in summ]] 
    summ2_text_info = [s['text_info'] for s in [i[1] for i in summ]] 

    sum_in_x, sum_in_y = 0, 0

    for sX in source1_text_info:
        best_value = 0
        for u in summ1_text_info:
            best_value = max(best_value, phi(sX, u))
        sum_in_x += best_value

    for sY in source2_text_info:
        best_value = 0
        for v in summ2_text_info:
            best_value = max(best_value, phi(sY, v))
        sum_in_y += best_value


    r = (sum_in_x / len(set1) + sum_in_y / len(set2))/2

    return r


def contrastiveness_sim(summ):
    """
    The contrastiveness of a contrastive opinion summary S, denoted as c(S), measures how well each u matches up with v in the summary.
    :return: [float] contrastiveness of the generated summary.
    """

    sumc = 0

    for (u, v) in summ:
        
        p = psi(u['text_info'], v['text_info'])
        sumc += p
        

    return sumc / len(summ)





      

def precision(summ):
    """
    The precision of a summary with k contrastive sentence pairs is the percentage of the k pairs that are agreed by a human annotator. If a retrieved pair exists in an evaluator’s paired-cluster set, we assume that the pair is agreed by the annotator (i.e., “relevant”).
    :return: [float] precision of the generated summary.
    """
    
    #print()
    #pprint(summ)
    #print()
    
    c_match = 0

    for (u, v) in summ:
        pair_is_agreed = False
        
        c1 = [i[0] for i in u['opinions']] # gets aspects
        c2 = [i[0] for i in v['opinions']] # gets aspects
        #c1 = getHumanClusteringForSentence(TARGET1, u['id'])
        #c2 = getHumanClusteringForSentence(TARGET2, v['id'])
        
        if any(i in c1 for i in c2):
            c_match += 1
            #print(c1)
            #print(c2)
            #print()
            

    return c_match / len(summ)


def aspect_coverage(source, summ):
    """
    The aspect coverage of a summary is the percentage of human-aligned clusters covered in the summary. If a pair of sentences appears in a human-aligned pair of clusters, we would assume that the aligned cluster is covered.
    :return: [float] aspect coverage of the generated summary.
    """

    covered_clusters = []
    all_clusters = []
    
    # Get all possible clusters (a cluster is identified by the aspect it represents)
    
    for u in source:
        cs = [i[0] for i in u['opinions']] # gets aspects
        for c in cs:
            if c not in all_clusters:
                all_clusters.append(c)

    
    #for product_id in human_clustering:
        #for cluster in human_clustering[product_id]:
            #if cluster not in all_clusters:
                
                ## If a cluster is in one target but not in the other, it won't be counted because it can't make pairs
                #if cluster not in human_clustering[TARGET1]:
                    #continue
                #if cluster not in human_clustering[TARGET2]:
                    #continue
                    
                #all_clusters.append(cluster)
                
     
    # Get all clusters that were covered in the summary 
    for (u, v) in summ:
        
        c1 = [i[0] for i in u['opinions']] # gets aspects
        c2 = [i[0] for i in v['opinions']] # gets aspects
        
        for c in c1 + c2: 
            if c not in covered_clusters:
                covered_clusters.append(c)


    return len(covered_clusters) / len(all_clusters)






############## TEST ################################################33

def representativiness_competitive(source, summ):
    
    points = 0
    
    opinions_source = [item for sublist in [source[j]['opinions'] for j in source] for item in sublist]
    opinions_summ = [item for sublist in [summ[j]['opinions'] for j in summ] for item in sublist]
    
    #pprint(opinions_source)
    #pprint(opinions_summ)
    
    #print()
    #print()
    #print()
    
    for o in opinions_source:
        for u in opinions_summ:
            if o[0] == u[0] and o[1] * u[1] >= 0:
                #print(o, u)
                points += 1
            elif o[0] == u[0] and o[1] * u[1] < 0:
                points -= 1
    
    #print(points)
    #print(points/len(opinions_source))
    
    return points/len(opinions_source)
    
    
    
    
    
def contrastiviness_competitive(source, summ):
    
    points = 0
    
    opinions_source = [item for sublist in [source[j]['opinions'] for j in source] for item in sublist]
    opinions_summ = [item for sublist in [summ[j]['opinions'] for j in summ] for item in sublist]
    
    #pprint(opinions_source)
    #pprint(opinions_summ)
    
    #print()
    #print()
    #print()
    
    for o in opinions_source:
        for u in opinions_summ:
            if o[0] == u[0] and o[1] * u[1] <= 0:
                #print(o, u)
                points += 1
            elif o[0] == u[0] and o[1] * u[1] < 0:
                #print(o, u)
                points -= 1
    
    #print(points)
    return points/len(opinions_source)








################################ DEPRECATED ############################



def sim_DEPREC(s1, s2): 
    r = 0
    for i in s1: 
        if i in s2: 
            r += 1
    return r






def sim(a1, a2):
    t1 = struct.getTopics({0:a1})
    t2 = struct.getTopics({0:a2})
    
    inter = intersection(t1, t2)
    un = union(t1, t2)
    return len(inter)/len(un)




def pairing(sum1, sum2):
    
    r = 0
    for i in range(min(len(sum1),len(sum2))):
        r += sim(sum1[i], sum2[i])
    
    return r/(max(len(sum1), len(sum2)))
    
    

def comparability (sum1, sum2):

    t1 = []
    t2 = []
    for i in sum1: 
        for o in sum1[i]['opinions']: 
            if o[0] not in t1: 
                t1.append(o[0])
    for i in sum2:
        for o in sum2[i]['opinions']:
            if o[0] not in t2: 
                t2.append(o[0])
    inter = intersection(t1, t2)
    un = union(t1, t2)

    return len(inter)/len(un)
    
    
    
#def divergence(t1, t2):
    #return 0.5 * (divergenceFrom(t1, t2) + divergenceFrom(t2, t1))
    
    
def divergence(t1, t2): 
    
    c = 0
    r = 0
    for i in t1: 
        for o1 in t1[i]['opinions']:             
            asp1 = o1[0]
            sent1 = o1[1]
            best = 0
            for j in t2: 
                for o2 in t2[j]['opinions']: 
                    asp2 = o2[0]
                    if asp2 != asp1: 
                        continue
                    c += 1
                    sent2 = o2[1]
                    d = abs(sent1 - sent2)/(2*MAXSENT)
                    if d > best: 
                        best = d
            r += best
        
    if c == 0:
        return 0
    
    r /= c
    
    return r
                
            
def conformity(sum1, sum2): 
    
    c = 0
    r = 0
    for i in sum1: 
        for o1 in sum1[i]['opinions']:             
            asp1 = o1[0]
            sent1 = o1[1]
            best = 1
            for j in sum2: 
                for o2 in sum2[j]['opinions']:                    
                    asp2 = o2[0]
                    if asp2 != asp1: 
                        continue
                    c += 1
                    sent2 = o2[1]
                    d = abs(sent1 - sent2)/(2*MAXSENT)
                    if d < best: 
                        best = d
            r += best
        
    if c == 0:
        return 0
      
    r /= c
    
    return 1 - r
                
            

#def equity(source1, sum1, source2, sum2):
    #t1 = getAspectsSentDistrib(source1)
    #t2 = getAspectsSentDistrib(source2)
    #s1 = getAspectsSentDistrib(sum1)
    #s2 = getAspectsSentDistrib(sum2)
    #eq1 = SAM(t1, s1)
    #eq2 = SAM(t2, s2)
    #return (eq1+eq2)/2
            


def equity(source, summ):
    
    r = 0
    for i in source: 
        for o1 in source[i]['opinions']: 
            asp1 = o1[0]
            sent1 = o1[1]
            best = 2*MAXSENT 
            for j in summ:
                for o2 in summ[j]['opinions']:
                    asp2 = o2[0]
                    if asp1 != asp2: 
                        continue
                    sent2 = o2[1]
                    d = abs(sent1 - sent2)
                    if d < best: 
                        best = d
            r += best/(2*MAXSENT)
    return 1 - r/len(source)
            
            

        
    
    
    
def OLD_diversity(sum1, sum2):
    sim1 = 0
    sim2 = 0
    c1 = 0
    c2 = 0
    for i in sum1: 
        for j in sum1: 
            if i == j: 
                continue
            sim1 += sim(sum1[i], sum1[j])
            c1 += 1
                
    for i in sum2: 
        for j in sum2: 
            if i == j: 
                continue
            sim2 += sim(sum2[i], sum2[j])
            c2 += 1
            
    sim1 /= c1+.001
    sim2 /= c2+.001
    
    print (" sims: ", sim1, sim2)
            
    return 1 - 0.5*(sim1+sim2)
  
  
def diversity_OLD(summ):
    r = 0
    c = 0
    for i in summ: 
        for j in summ: 
            if i == j: 
                continue
            r += sim(summ[i], summ[j])
            c += 1

            
    r /= c+.001
    
            
    return 1 - r
            
        
                    
def aggregation(sum1, sum2, maxsize): 
    # Total de tópicos em relação à quantidade que poderia conter
    topics = []
    for i in sum1: 
        for o1 in sum1[i]['opinions']: 
            a1 = o1[0]
            if a1 not in topics: 
                topics.append(a1)
    for i in sum2: 
        for o2 in sum2[i]['opinions']: 
            a2 = o2[0]
            if a2 not in topics: 
                topics.append(a2)
            
    return len(topics)/maxsize



def getSum_DEPRECATED(source, sumIndexes):
    summary = {}
    for i in sumIndexes:         
        source[i]['sourceID'] = i
        summary[len(summary)] = source[i]
    return summary 







    


def union(l1, l2):
    u = []
    for i in l1: 
        if i not in u: 
            u.append(i)
    for j in l2: 
        if i not in u:
            u.append(i)
    return u


def intersection(l1, l2):
    r = []
    for i in l1: 
        if i in l2: 
            r.append(i)
    return r



    
def independentRepresentativiness(source, summ):
    T1 = struct.getTopics(source)
    TP = struct.getTopics(summ)
    return len(TP)/len(T1)


def representativiness_DEPREC (source1, sum1, source2, sum2): 
    T1 = struct.getTopics(source1)
    T2 = struct.getTopics(source2)
    TP = struct.getTopics(sum1)
    TQ = struct.getTopics(sum2)
    
    T12 = union(T1, T2)
    TPQ = union(TP, TQ)
    
    return len(TPQ)/(len(T12))
        




def contrastiviness_repr(source1, source2, summ1, summ2):
     
     
    opinions_source1 = [item for sublist in [source1[j]['opinions'] for j in source1] for item in sublist]
    opinions_source2 = [item for sublist in [source2[j]['opinions'] for j in source2] for item in sublist]
     
    opinions_summ1 = [item for sublist in [summ1[j]['opinions'] for j in summ1] for item in sublist]
    opinions_summ2 = [item for sublist in [summ2[j]['opinions'] for j in summ2] for item in sublist]
     
    points = 0
     
    # Compares source 1 with summ 2 and vice-versa.
    for opinions_source, opinions_opposite_source, opinions_opposite_summ in zip([opinions_source1, opinions_source2], [opinions_source2, opinions_source1], [opinions_summ2, opinions_summ1]):
         
        all_possibles = []
         
        idx1_used = []
        idx2_used = []
         
        for idx1 in range(len(opinions_source)):
            if idx1 in idx1_used:
                continue
            op1 = opinions_source[idx1]
            for idx2 in range(len(opinions_opposite_source)):
                if idx2 in idx2_used:
                    continue
                op2 = opinions_opposite_source[idx2]
                pol1 = trinary_polarity(op1[1])
                pol2 = trinary_polarity(op2[1])
                if op1[0] == op2[0] and pol1 == -pol2:
                    asp_cont = (op1[0], pol1) # This aspect has the possibility to form a possible contrastive pair. 
                    #asp_opposite = (op1[0], -pol1)
                     
                    #if asp_opposite in all_possibles:
                        ##pprint(all_possibles)
                        ##print('deleting ', asp_opposite)
                        ##input()
                        #del all_possibles[all_possibles.index(asp_opposite)]
                    #else:
                    ##if asp_cont not in all_possibles:
                    all_possibles.append(asp_cont)
                         
                    idx1_used.append(idx1)
                    idx2_used.append(idx2)
          
        #pprint(sorted(all_possibles))
        #input()
          
        pairs_formed = []
         
        idx1_used = []
        idx2_used = []
         
        for idx1 in range(len(opinions_source)):
            if idx1 in idx1_used:
                continue
            op1 = opinions_source[idx1]
            for idx2 in range(len(opinions_opposite_summ)):
                if idx2 in idx2_used:
                    continue
                 
                op2 = opinions_opposite_summ[idx2]
                pol1 = trinary_polarity(op1[1])
                pol2 = trinary_polarity(op2[1])
                if op1[0] == op2[0] and pol1 == -pol2:
                    asp_cont = (op1[0], pol1, pol2) # This aspect has the possibility to form a possible contrastive pair. 
                    pairs_formed.append(asp_cont)
                    idx1_used.append(idx1)
                    idx2_used.append(idx2)
   
             
             
        p = 0
        for o in all_possibles:
            for u in pairs_formed:
                if o[0] == u[0] and o[1] * u[1] >= 0:
                    #print(o, u)
                    p += 1
                    break
             
        points += p/len(all_possibles)
 
     
    return points/2
