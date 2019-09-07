# -*- coding: utf-8 -*-


# From Python standard library:
import statistics # For mean and stdev

# From this project:
import method
from read_input import read_input
import evaluation.evaluation as evalu
import output_format as out
import structure as struct 
from structure import word_count


import optimization as optm

# Setup options
from setup import LIM_SENTENCES     # Sets the maximum number of SENTENCES in each side of the summary
from setup import LIM_WORDS         # Sets the maximum number of WORDS in each side of the summary
from setup import MIN_INTENS_IN_SUMMARY         
from setup import DATA_DIR
from setup import SOURCE1, SOURCE2
from setup import filepath          # Get full path for the file with data of target 

from setup import VERBOSE_MODE
from setup import EVALUATION_MODE 
from setup import OUTPUT_MODE 
from setup import OVERVIEW_MODE 

from setup import BYPASS_GENERIC 
from setup import BYPASS_SHORT 
from setup import BYPASS_UNRELATAD 

from setup import METHOD
from setup import OPTM_METHOD
from setup import ALPHA

from setup import KEY_MEASURE

from setup import ASPECT_DETECTION
from setup import POLARITY_ATTRIBUTION


from writefiles import underwrite_file




results = {}
results['meta'] = {}
results['meta']['source'] = []
results['meta']['source'].append(SOURCE1)
results['meta']['source'].append(SOURCE2)
results['meta']['limits (per side)'] = {}
results['meta']['limits (per side)']['sentences'] = LIM_SENTENCES
results['meta']['limits (per side)']['words'] = LIM_WORDS
results['output'] = []



from setup import DEBUGGING


if DEBUGGING:
    # For debugging
    out.setDebugPrints(True)     # Choose whether or not to display information for debugging.
    #out.setDebugPrints(False)   # Choose whether or not to display information for debugging.
from pprint import pprint
            




def print_verbose(*msg):
    if not VERBOSE_MODE:
        return
    out.printMessage(*msg)



def print_result(*msg):
    print(*msg, end='', flush=True)



# Load input
def load_input():
    print_verbose(" \nLENDO ALVO 1")
    source1 = read_input(filepath(SOURCE1))
    #out.printdebug(source1)
    #input()

    print_verbose(" \nLENDO ALVO 2")
    source2 = read_input(filepath(SOURCE2))
    #out.printdebug(source2)
    
    return source1, source2

        


from time import time



exec_code = str(int(time())%100000000)


FILE_RESULTS = 'results_'+exec_code+'.txt'



RTESTS = 100
DTESTS = int(RTESTS/10)

print('Will perform %d tests and discard %d(x2) best and worst\n\n' % (RTESTS, DTESTS))




f = open(FILE_RESULTS, 'a')
f.write('%d tests, discard %d(x2) best and worst\n\n' % (RTESTS, DTESTS))
f.close()


SHOW_ALL_ITERAT = False




def sqdiff (l1, l2):
    r = 0
    for i in range(len(l1)):
        r += pow(l1[i]-l2[i], 2)
    return r






#SHOW_ALL_ITERAT = False

for SOURCE1, SOURCE2 in [('D1a','D1b'), ('D2a','D2b'), ('D3a','D3b'), ('D4a','D4b'), ('D5a','D5b'), ('D6a','D6b'), ('D7a','D7b'), ('D8a','D8b')]:
#for SOURCE1, SOURCE2 in ([('D3a','D3b'),('D4a','D4b'), ('D5a','D5b')]):
    
    summScoresList = {}
    
    OUTPUT_FILE = 'out'+exec_code+'_'+SOURCE1[:-1]+'.txt'

    print ('\n\n\n\n ============  ', SOURCE1, SOURCE2)
    print('\n\n')
    
    total_time = 0


    print_verbose('Loading input')
    source1, source2 = load_input()
    print_verbose('Sizes of datasets: ', len(source1), len(source2))




    wc1 = struct.word_count(source1)
    wc2 = struct.word_count(source2)





        
    
    print("Size 1: ", len(source1))
    print("Size 2: ", len(source2))

    #if BYPASS_UNRELATAD:
        #source1 = remove_aspects(source1, 'empresa')
        #source2 = remove_aspects(source2, 'empresa')
        #source1 = remove_aspects(source1, 'x')
        #source2 = remove_aspects(source2, 'x')
        #source1 = remove_aspects(source1, '_NONE')
        #source2 = remove_aspects(source2, '_NONE')

        #print("Size after removing unrelated 1: ", len(source1))
        #print("Size after removing unrelated 2: ", len(source2))

    # /source.../ are structures of the form
    '''
    {
    0: {'intensity': 80.0,
        'opinions': [('CÂMERA', 80.0)],
        'sent': {'CÂMERA': 88},
        'word_count': 2,
        'verbatim': 'Câmera boa.'},
    1: {'intensity': 80.0,
        'opinions': [('CÂMERA', 80.0)],
        'sent': {'CÂMERA': 88},
        'word_count': 3,
        'verbatim': 'Gostei da câmera.'}
    5: {'intensity': 80.0,
        'opinions': [('BATERIA', 80.0), ('DESEMPENHO', 80.0)],
        'sent': {'BATERIA': 88, 'DESEMPENHO': 88},
        'verbatim': 'Muito rápido! Não trava! Bateria dura muito!',
        'word_count': 7},
    2: {'intensity': 80.0,
        'opinions': [('DESEMPENHO', -80.0),
                    ('DESEMPENHO', -80.0),
                    ('RESISTÊNCIA', -80.0)],
        'sent': {'DESEMPENHO': -94, 'RESISTÊNCIA': -88},
        'verbatim': 'Entretanto, na primeira semana de uso já ralou facilmente, '
                    'esquenta muito com os dados móveis ligados e trava, mesmo '
                    'que raramente.',
        'word_count': 21}
    }
    '''

    # Estimate overall sentiment about targets
    overall_rate_1 = struct.avgSent(source1)  
    overall_rate_2 = struct.avgSent(source2)

    # Get statistics about aspects in the source (mean, stdev, probability)
    stats_source_1 = struct.aspects_stats(source1)
    stats_source_2 = struct.aspects_stats(source2)

    # /stats_.../ are structures of the form: 
    '''
        {'tela': {'mean':  83, 'prob': 0.07, 'std': 0},
        'cor':  {'mean': -87, 'prob': 0.21, 'std': 1.73}}
    '''



        
    


    #if KEY_MEASURE == 'lexicon':
        #source1 = remove_low_prob(source1, stats_source_1)
        #source2 = remove_low_prob(source2, stats_source_2)
        
        #print("Size after removing low prob 1: ", len(source1))
        #print("Size after removing low prob 2: ", len(source2))
        
        #stats_source_1 = struct.aspects_stats(source1)
        #stats_source_2 = struct.aspects_stats(source2)
        
        
    #else:
    #source1 = dict(source1)
    #source2 = dict(source2)
        
    all_summaries = []    
        
        
    #struct.printOverview(stats_source_1)
    #print()
    #struct.printOverview(stats_source_2)
    #print()
    #print()
    #input()



    #struct.printOverview(stats_source_1)
    #print()
    #struct.printOverview(stats_source_2)
    #input()


        
    #if BYPASS_GENERIC:
        #source1 = remove_generic(source1)
        #source2 = remove_generic(source2)

        #print("Size after removing empty aspects 1: ", len(source1))
        #print("Size after removing empty aspects 2: ", len(source2))

    ##if BYPASS_SHORT and KEY_MEASURE == 'aspects':
    #if BYPASS_SHORT:
        #source1 = remove_short_length(source1)
        #source2 = remove_short_length(source2)

        #print("Size after removing short sentences 1: ", len(source1))
        #print("Size after removing short sentences 2: ", len(source2))
        
        
    #stats_source_1 = struct.aspects_stats(source1)
    #stats_source_2 = struct.aspects_stats(source2)
        

    #source1 = remove_low_intensity(source1)
    #source2 = remove_low_intensity(source2)

    #print("Size after removing low intensity 1: ", len(source1))
    #print("Size after removing low intensity 2: ", len(source2))





    print(len(source1))
    print(len(source2))
    print()

    #c1 = {}
    #c1['data'] = [source1[i] for i in source1]
    #c2 = {}
    #c2['data'] = [source2[i] for i in source2]

    #from writefiles import save_to_file
    #save_to_file('30-clean.json', c1)
    #save_to_file('31-clean.json', c2)

    #exit()

    #pprint(source1)

    e1_pos = {}
    e1_neg = {}
    e2_pos = {}
    e2_neg = {}

    for i in source1:
        if sum([source1[i]['sent'][a] for a in source1[i]['sent']]) > 0:
            e1_pos[i] = source1[i]
        if sum([source1[i]['sent'][a] for a in source1[i]['sent']]) < 0:
            e1_neg[i] = source1[i]
            
    for i in source2:
        if sum([source2[i]['sent'][a] for a in source2[i]['sent']]) > 0:
            e2_pos[i] = source2[i]
        if sum([source2[i]['sent'][a] for a in source2[i]['sent']]) < 0:
            e2_neg[i] = source2[i]


    stats_e1_pos = struct.aspects_stats(e1_pos)
    stats_e1_neg = struct.aspects_stats(e1_neg)
    stats_e2_pos = struct.aspects_stats(e2_pos)
    stats_e2_neg = struct.aspects_stats(e2_neg)


    from setup import PRESET


    #for alpha_choice in [10*i+1 for i in range(6)]:
    for METHOD in ['CONTRASTIVE']:


    #for METHOD in ['NONCONTRASTIVE', 'CONTRASTIVE']:
    #for METHOD in ['NONCONTRASTIVE']:
        
        
        ini_time = time()

        

        
        
        
        #stats_source_1 = struct.aspects_stats(source1)
        #stats_source_2 = struct.aspects_stats(source2)
        
        if VERBOSE_MODE:
            print_verbose('\nOpinions in the summary for each entity:')
            print_verbose('\nOverview of opinions in the source for each entity:')
            struct.printOverview(stats_source_1)
            struct.printOverview(stats_source_2)
        
            


        print_verbose('Sizes of datasets without low intensity sentences: ', len(source1), len(source2))







        print_verbose('Making summary')


        #Make contrastive summary
        
        
        hr = []
        hc = []
        hd = []
        hh = []
        
        h_words1 = []
        h_words2 = []
        h_sentences1 = []
        h_sentences2 = []
        
        w_e1_pos = word_count(e1_pos)
        w_e1_neg = word_count(e1_neg)
        w_e2_pos = word_count(e2_pos)
        w_e2_neg = word_count(e2_neg)
        
        w_tot = w_e1_pos + w_e1_neg + w_e2_pos + w_e2_neg
        
        size_A_proportion = w_e1_pos + w_e2_neg
        size_B_proportion = w_e1_neg + w_e2_pos
        
        size_A = LIM_WORDS*size_A_proportion/(size_A_proportion+size_B_proportion)
        size_B = LIM_WORDS*size_B_proportion/(size_A_proportion+size_B_proportion)

        #size_1_pos = LIM_WORDS*w_e1_pos/w_tot
        #size_1_neg = LIM_WORDS*w_e1_neg/w_tot
        #size_2_pos = LIM_WORDS*w_e2_pos/w_tot
        #size_2_neg = LIM_WORDS*w_e2_neg/w_tot

        #print(size_1_pos)
        #print(size_1_neg)
        #print(size_2_pos)
        #print(size_2_neg)

        
        for repeat in range(RTESTS):
            
            from optimization import random_seed
            random_seed()
            
            
            

            #if METHOD == 'CONTRASTIVE':
                
            pr = repeat/RTESTS
            out.printProgress('   %3d%%   %s %s' % (100*pr, SOURCE1, SOURCE2), end="\r")    

            summ_idx_1A, summ_idx_2A = optm.MakeContrastiveSummary(e1_pos, e2_neg, stats_e1_pos, stats_e2_neg, OPTM_METHOD, size_A, size_A)
            summ_idx_1B, summ_idx_2B = optm.MakeContrastiveSummary(e1_neg, e2_pos, stats_e1_neg, stats_e2_pos, OPTM_METHOD, size_B, size_B)
            
            summ_idx_1 = summ_idx_1A + summ_idx_1B
            summ_idx_2 = summ_idx_2A + summ_idx_2B
            
            #summ_idx_1, summ_idx_2 = optm.MakeContrastiveSummary(source1, source2, stats_source_1, stats_source_2)
            out.printProgress()
            out.printProgress()



            #elif METHOD == 'NONCONTRASTIVE':
                

                #print_verbose('Making non-contrastive summary 1/2  (size of set: %d)' % len(source1))
                #summ_idx_1 = optm.makeSummary(source1, stats_source_1, OPTM_METHOD)
                
                #out.printProgress()

            
                #print_verbose('Making non-contrastive summary 2/2  (size of set: %d)' % len(source2))
                #summ_idx_2 = optm.makeSummary(source2, stats_source_2, OPTM_METHOD)
                
                #out.printProgress()
                
                #exit()
            
            fin_time = time()
            elaps_time = fin_time - ini_time 
            total_time += elaps_time 



            summ1 = {i: source1[i] for i in summ_idx_1}
            summ2 = {i: source2[i] for i in summ_idx_2}

            sum_stats_1 = struct.aspects_stats(summ1)
            sum_stats_2 = struct.aspects_stats(summ2)
            
            
            s_id = (sorted(summ_idx_1), sorted(summ_idx_2))            
            if s_id not in all_summaries:
                all_summaries.append(s_id)
                        


            if VERBOSE_MODE:
                print_verbose('\nOverview of opinions in the summary for each entity:')
                struct.printOverview(sum_stats_1)
                struct.printOverview(sum_stats_2)



                
                    
                
                
            # Display the results     



            if OVERVIEW_MODE:
                print_verbose('\nOpinions in the summary for each entity:')
                for i in summ_idx_1:
                    out.printinfo("      %4d)   %s " % (i, source1[i]['opinions']))        
                print()
                for i in summ_idx_2:
                    out.printinfo("      %4d)   %s " % (i, source2[i]['opinions']))        


            if OUTPUT_MODE:
                print("\nCONTRASTIVE SUMMARY\n")
                print("\n___ Produto 1\n")
                for i in summ_idx_1:
                    print ("%s " % (source1[i]['verbatim']))        
                    #print ("      %4d)   %s " % (i, source1[i]['verbatim']))        
                print("\n___ Produto 2\n")
                for i in summ_idx_2:
                    print ("%s " % (source2[i]['verbatim']))        
                    #print ("      %4d)   %s " % (i, source2[i]['verbatim']))          

            
            def harmonic_mean(l):
                s = 0
                if min(l) == 0:
                    return -1
                for i in l:
                    s += 1/i
                m = s/len(l)
                return 1/m
            

            if EVALUATION_MODE: 
                
                
                
                evals = {}
            
                evals['r1'] = 100*evalu.representativiness(source1, summ1)
                evals['r2'] = 100*evalu.representativiness(source2, summ2)
                evals['R'] = (evals['r1']+evals['r2'])/2
                
                evals['C'] = 100*evalu.contrastiviness(source1, source2, summ1, summ2)
                            
                evals['d1'] = 100*evalu.diversity(source1, summ1)
                evals['d2'] = 100*evalu.diversity(source2, summ2)
                
                evals['D'] = (evals['d1']+evals['d2'])/2
                
                
                evals['H'] = harmonic_mean([evals['R'],evals['C'],evals['D']])
                
                
                #for i in evals:
                    #evals[i] = int('%3.0lf'%(evals[i]))
                    
                    
                w1 = sum([summ1[i]['word_count'] for i in summ1])
                w2 = sum([summ2[i]['word_count'] for i in summ2])
    
                
                #print()
                #print_result("%3.0lf)   %s %3.0lf    " % (repeat+1, METHOD[:4], ALPHA))
                #print_result('(%3.0lf %3.0lf) %3.0lf   ' % (evals['r1'], evals['r2'], evals['R']))
                #print_result('%3.0lf   ' % ( evals['C']))
                #print_result('    %3.0lf' % (evals['D']))
                #print_result('    [[%3.0lf]]' % (evals['H']))
                #print_result('    %3.0lfs' % elaps_time)
                #print_result('\n')
                #print_result('\n')
                
                
                
                
                #print('sentences: ', len(summ1), len(summ2))
                #print('words: ', w1, w2)
                #print('diff summs: ', len(all_summaries))
                
                #print('\n')
                #print('\n')
                
                h_words1.append(w1)
                h_words2.append(w2)
                h_sentences1.append(len(summ1))
                h_sentences2.append(len(summ2))
                
                
                hr.append(evals['R'])
                hc.append(evals['C'])
                hd.append(evals['D'])
                hh.append(evals['H'])
                

                
                n = {}
                n['parameters'] = {}
                n['parameters']['method'] = METHOD
                n['evaluation'] = {}
                n['evaluation']['R'] = evals['R']
                n['evaluation']['C'] = evals['C']
                n['evaluation']['D'] = evals['D']
                n['evaluation']['H'] = evals['H']
                n['summ'] = []
                n['summ'].append(summ_idx_1)
                n['summ'].append(summ_idx_2)
                n['size'] = {}
                n['size']['word count'] = []
                n['size']['word count'].append(word_count(summ1))
                n['size']['word count'].append(word_count(summ2))
                results['output'].append(n)
                
                
                
                summScoresList[(evals['R'],evals['C'],evals['D'])] = (summ_idx_1, summ_idx_2)
                
        #pprint(summScoresList)
                
        from statistics import stdev
            
                    
        hr_medians = sorted(hr)[DTESTS:-DTESTS]
        hc_medians = sorted(hc)[DTESTS:-DTESTS]
        hd_medians = sorted(hd)[DTESTS:-DTESTS]
        hh_medians = sorted(hh)[DTESTS:-DTESTS]


        sthh = stdev(hh_medians)
        sthc = stdev(hc_medians)
        sthr = stdev(hr_medians)
        sthd = stdev(hd_medians)


            
        r = sum(hr)/len(hr)
        c = sum(hc)/len(hc)
        d = sum(hd)/len(hd)
        h = harmonic_mean([r,c,d])
        
        
        r_median_mean = sum(hr_medians)/len(hr_medians)
        c_median_mean = sum(hc_medians)/len(hc_medians)
        d_median_mean = sum(hd_medians)/len(hd_medians)
        h_median_mean = harmonic_mean([r,c,d])

        ht = sum(hh)/len(hh)
        ht_median_mean = sum(hh_medians)/len(hh_medians)
        
        
        results_msg = ''
        results_msg += '\n\n'
        results_msg += '              %3.0lf   %3.0lf   %3.0lf   [ %3.0lf ]    (%3.0lf)      ~%3.0lf' % (r_median_mean, c_median_mean, d_median_mean, h_median_mean, ht_median_mean, sthh)
        results_msg += '\n\n'  
        results_msg += '             ~%3.0lf  ~%3.0lf  ~%3.0lf               ~%3.0lf' % (sthr, sthc, sthd, sthh)
        results_msg += '\n\n\n'
        results_msg += 'max           %3.0lf   %3.0lf   %3.0lf                %3.0lf' % ((max(hr_medians)), (max(hc_medians)), (max(hd_medians)), (max(hh_medians)))
        results_msg += '\n\n'
        results_msg += 'min           %3.0lf   %3.0lf   %3.0lf                %3.0lf' % ((min(hr_medians)), (min(hc_medians)), (min(hd_medians)), (min(hh_medians)))
        results_msg += '\n\n\n'
        results_msg += 'simple mean   %3.0lf   %3.0lf   %3.0lf     %3.0lf       \'%3.0lf\'      ~%3.0lf' % (r, c, d, h, ht, sthh)
        results_msg += '\n\n\n'
        


        avg_words1 = sum(h_words1)/len(h_words1)
        avg_words2 = sum(h_words2)/len(h_words2)
        avg_sentences1 = sum(h_sentences1)/len(h_sentences1)
        avg_sentences2 = sum(h_sentences2)/len(h_sentences2)
        
        
        
        results_msg += '\n\n'
        results_msg += ' avg words 1:  %6.2lf ' % (avg_words1)
        results_msg += '\n'
        results_msg += ' avg words 2:  %6.2lf ' % (avg_words2)
        results_msg += '\n\n'
        results_msg += ' avg sentences 1:  %6.2lf ' % (avg_sentences1)
        results_msg += '\n'
        results_msg += ' avg sentences 2:  %6.2lf ' % (avg_sentences2)
        results_msg += '\n\n'
        results_msg += ' time %6.2lf ' % (elaps_time)
        results_msg += '\n'
        results_msg += ' diff summs: %d' % (len(all_summaries))
        results_msg += '\n\n'
        
        print(results_msg)
        
        
        f = open(FILE_RESULTS, 'a')
        f.write('\n\n')
        f.write('============  %s %s ============' % (SOURCE1, SOURCE2))
        f.write('\n\n')
        f.write(results_msg)
        f.write('\n\n\n\n\n\n')
        f.close()


            
        fairness_rank = sorted(summScoresList.keys(), key= lambda k : sqdiff(k, [r_median_mean, c_median_mean, d_median_mean]))
        #pprint(fairness_rank)
        #for i in fairness_rank:
            #print(sqdiff(i, [r_median_mean, c_median_mean, d_median_mean]))
        #print([r_median_mean, c_median_mean, d_median_mean])
        #exit()
        
        summ_idx_f_1 = summScoresList[fairness_rank[0]][0]
        summ_idx_f_2 = summScoresList[fairness_rank[0]][1]
        
        
        summ1 = {i: source1[i] for i in summ_idx_f_1}
        summ2 = {i: source2[i] for i in summ_idx_f_2}
        
        
        
        print("\nMOST FAIR SUMMARY\n")
        summ_out = '\n'
        #summ_out += " = Produto A = \n"
        for i in summ_idx_f_1:
            summ_out += "%s " % (source1[i]['verbatim'])
            summ_out += '\n'
            #print ("      %4d)   %s " % (i, source1[i]['verbatim']))    
            
        summ_out += '\n\n'
        
        #summ_out += " = Produto B = \n"
        for i in summ_idx_f_2:
            summ_out += "%s " % (source2[i]['verbatim'])
            summ_out += '\n'
            #print ("      %4d)   %s " % (i, source2[i]['verbatim']))  
            
        w1 = sum([summ1[i]['word_count'] for i in summ1])
        w2 = sum([summ2[i]['word_count'] for i in summ2])
        
        summ_out += '\n\n\n'
        
        summ_out += 'sentences:   %3d  %3d\n' % (len(summ1), len(summ2))
        summ_out += '    words:   %3d  %3d' % (w1, w2)
        summ_out += '\n'
        
        
        evals = {}
                
        evals['r1'] = 100*evalu.representativiness(source1, summ1)
        evals['r2'] = 100*evalu.representativiness(source2, summ2)
        evals['R'] = (evals['r1']+evals['r2'])/2
        
        evals['C'] = 100*evalu.contrastiviness(source1, source2, summ1, summ2)
                    
        evals['d1'] = 100*evalu.diversity(source1, summ1)
        evals['d2'] = 100*evalu.diversity(source2, summ2)
        
        evals['D'] = (evals['d1']+evals['d2'])/2
        
        
        evals['H'] = harmonic_mean([evals['R'],evals['C'],evals['D']])
        
        
        #for i in evals:
            #evals[i] = int('%3.0lf'%(evals[i]))
            
            
        w1 = sum([summ1[i]['word_count'] for i in summ1])
        w2 = sum([summ2[i]['word_count'] for i in summ2])

        
        #print()
        summ_out += '\n\n'
        summ_out += '(%3.0lf %3.0lf)     %3.0lf   %3.0lf   %3.0lf   [[%3.0lf]]  ' % (evals['r1'], evals['r2'], evals['R'], evals['C'], evals['D'],  evals['H'])
        summ_out += '\n\n'

        summ_out += '              %3.0lf   %3.0lf   %3.0lf    [%3.0lf]      ~%3.0lf' % (r_median_mean, c_median_mean, d_median_mean, ht_median_mean, sthh)    
        
        summ_out += '\n'
        summ_out += '\n'
        
        
        summ_out += str(summ_idx_f_1) + '\n'
        summ_out += str(summ_idx_f_2) + '\n'
        summ_out += '\n'
        summ_out += '\n'
        
        
        
        
        print('sentences: ', len(summ1), len(summ2))
        print('words: ', w1, w2)
        print('diff summs: ', len(all_summaries))
        
        print('\n')
        print('\n')
                
                
        
        print(summ_out)
        
        f = open(OUTPUT_FILE, 'w')
        f.write(summ_out)
        f.close()



        results['meta']['size'] = {}
        results['meta']['size']['source'] = {}
        results['meta']['size']['source']['sentences'] = []
        results['meta']['size']['source']['sentences'].append(len(source1))
        results['meta']['size']['source']['sentences'].append(len(source2))
        results['meta']['size']['source']['words'] = [] 
        results['meta']['size']['source']['words'].append(word_count(source1))
        results['meta']['size']['source']['words'].append(word_count(source2))
        results['meta']['run time'] = round(total_time,2)

        underwrite_file('output/'+SOURCE1+' '+SOURCE2+' ('+str(int(time()))+').json', results)

        #method.save_caches()