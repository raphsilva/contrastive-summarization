import evaluation as evalu
import output_format as out
from interface import *
from language import setLanguage
from load_data import preprocess
from load_data import read_input
from setup import LANGUAGE
from setup import MAX_WORDS
from setup import SHOW_EVALUATION
from setup import SHOW_INDEXES
from setup import SHOW_SUMMARY
from setup import SOURCE1
from setup import SOURCE2
from setup import SUMLEN
from setup import filepath
from structure import idx_to_summ
from structure import word_count
from summarization import contrastiveness_first
from summarization import representativeness_first

results = {}
results['meta'] = {}
results['meta']['implementation'] = 'Kim'
results['meta']['source'] = []
results['meta']['source'].append(SOURCE1)
results['meta']['source'].append(SOURCE2)
results['meta']['language'] = LANGUAGE
results['meta']['limits'] = {}
results['meta']['limits']['pairs'] = SUMLEN
results['output'] = []


def print_result(*msg):
    print(*msg, end='', flush=True)

from writefiles import underwrite_file

def round_num(num):
    return float('%.2g' % (num))

from setup import SIZE_FAC, METHOD, DATASET_ID

from time import time

exec_code = str(int(time()) % 100000000)

FILE_RESULTS = 'results_ ' + exec_code + '.txt'

RTESTS = 10
DTESTS = int(RTESTS / 10)

print('Will perform %d tests and discard %d(x2) best and worst\n\n' % (RTESTS, DTESTS))

f = open(FILE_RESULTS, 'a')
f.write('%d tests, discard %d(x2) best and worst\n\n' % (RTESTS, DTESTS))
f.close()

SHOW_ALL_ITERAT = False


def sqdiff(l1, l2):
    r = 0
    for i in range(len(l1)):
        r += pow(l1[i] - l2[i], 2)
    return r


for SOURCE1, SOURCE2 in reversed([('D2a', 'D2b')]):

    summScoresList = {}

    OUTPUT_FILE = 'out ' + exec_code + '_ ' + SOURCE1[:-1] + '.txt'

    print('\n\n\n\n ============  ', SOURCE1, SOURCE2)
    print('\n\n')

    # Setup language functions
    setLanguage(LANGUAGE)

    # Load dataset
    source1 = read_input(filepath(SOURCE1))
    source2 = read_input(filepath(SOURCE2))

    source1_proc = preprocess(source1)
    source2_proc = preprocess(source2)

    print(len(source1), len(source1_proc['+'] + source1_proc['-']))
    print(len(source2), len(source2_proc['+'] + source2_proc['-']))

    set1_pos = source1_proc['+']
    set1_neg = source1_proc['-']
    set2_pos = source2_proc['+']
    set2_neg = source2_proc['-']

    hr = []
    hc = []
    hd = []
    hh = []

    h_words1 = []
    h_words2 = []
    h_sentences = []
    h_sentences1 = []
    h_sentences2 = []

    RTESTS = 100
    DTESTS = int(RTESTS / 10)

    print('Will perform %d tests and discard %d(x2) best and worst\n\n' % (RTESTS, DTESTS))

    total_time = 0

    ini_time = time()

    all_summaries = []

    repeat = 0

    for repeat in range(RTESTS):

        pr = repeat / RTESTS
        out.printProgress('   %3d%% ' % (100 * pr), end="\r")

        from random import shuffle

        shuffle(set1_pos)
        shuffle(set1_neg)
        shuffle(set2_pos)
        shuffle(set2_neg)

        if METHOD == 'RF':
            centroid_choices = [False]
            hungarian_choices = [False]
        else:
            centroid_choices = [None]
            hungarian_choices = [None]

        for lambda_choice in [0.5]:
            LAMBDA = lambda_choice

            for centroid_choice in centroid_choices:
                CENTROIDS_AS_SUMMARY = centroid_choice

                for hungarian_choice in hungarian_choices:
                    USE_HUNGARIAN_METHOD = hungarian_choice

                    ini_time = time()

                    if METHOD == 'CF':

                        summ_idx_A = contrastiveness_first(set1_pos, set2_neg, '+', '-', LAMBDA, CENTROIDS_AS_SUMMARY, USE_HUNGARIAN_METHOD)
                        summ_idx_B = contrastiveness_first(set1_neg, set2_pos, '-', '+', LAMBDA, CENTROIDS_AS_SUMMARY, USE_HUNGARIAN_METHOD)

                    elif METHOD == 'RF':

                        summ_idx_A = representativeness_first(set1_pos, set2_neg, '+', '-', LAMBDA, CENTROIDS_AS_SUMMARY, USE_HUNGARIAN_METHOD)
                        summ_idx_B = representativeness_first(set1_neg, set2_pos, '-', '+', LAMBDA, CENTROIDS_AS_SUMMARY, USE_HUNGARIAN_METHOD)

                    fin_time = time()
                    elaps_time = fin_time - ini_time
                    total_time += elaps_time

                    # Indexes of each side of the summary
                    summ_idx_1 = [i[0] for i in summ_idx_A + summ_idx_B]
                    summ_idx_2 = [i[1] for i in summ_idx_A + summ_idx_B]

                    summ1 = idx_to_summ(source1, summ_idx_1)
                    summ2 = idx_to_summ(source2, summ_idx_2)

                    s_id = (sorted(summ_idx_1), sorted(summ_idx_2))
                    if s_id not in all_summaries:
                        all_summaries.append(s_id)

                    fin_time = time()
                    elaps_time = fin_time - ini_time
                    total_time += elaps_time

                    # IDs of sentences in the summary (gotten from original dataset)
                    summ_idx_A1 = [source1[i[0]]['id'] for i in summ_idx_A]
                    summ_idx_A2 = [source2[i[1]]['id'] for i in summ_idx_A]
                    summ_idx_B1 = [source1[i[0]]['id'] for i in summ_idx_B]
                    summ_idx_B2 = [source2[i[1]]['id'] for i in summ_idx_B]

                    summ_idx_1 = summ_idx_A1 + summ_idx_B1
                    summ_idx_2 = summ_idx_A2 + summ_idx_B2

                    n = {}
                    n['parameters'] = {}
                    n['parameters']['method'] = METHOD
                    n['parameters']['lambda'] = LAMBDA
                    n['parameters']['hungarian'] = USE_HUNGARIAN_METHOD
                    n['parameters']['centroid'] = CENTROIDS_AS_SUMMARY
                    n['summ'] = []
                    n['summ'].append(summ_idx_1)
                    n['summ'].append(summ_idx_2)
                    n['size'] = {}
                    n['size']['word count'] = []
                    n['size']['word count'].append(word_count(summ1))
                    n['size']['word count'].append(word_count(summ2))

                    results['output'].append(n)

                    if SHOW_SUMMARY:
                        show_summary(source1, source2, summ_idx_A, part=1)
                        show_summary(source1, source2, summ_idx_B, part=2)

                    if SHOW_INDEXES:
                        print('#')
                        print("%s  %4.2lf " % (METHOD, LAMBDA))
                        print('>', SOURCE1, summ_idx_1)
                        print('>', SOURCE2, summ_idx_2)
                        print()

                    w1 = sum([summ1[i]['word_count'] for i in summ1])
                    w2 = sum([summ2[i]['word_count'] for i in summ2])

                    if w1 + w2 > MAX_WORDS: # Summary is too large; will repeat with smaller size factor.
                        repeat -= 1
                        SIZE_FAC[METHOD][DATASET_ID] *= 0.95
                        break
                    else:
                        SIZE_FAC[METHOD][DATASET_ID] *= 1.01

                    if SHOW_EVALUATION:

                        summ = [(source1[i], source2[j]) for i, j in summ_idx_A + summ_idx_B]

                        print(" %s  %4.2lf " % (METHOD, LAMBDA), end='')

                        repres1 = evalu.representativeness_sim(source1, summ1)
                        repres2 = evalu.representativeness_sim(source2, summ2)
                        contrs = evalu.contrastiveness_sim(summ1, summ2)
                        pair = evalu.precision(summ1, summ2)
                        cove1 = evalu.aspect_coverage(source1, summ1)
                        cove2 = evalu.aspect_coverage(source2, summ2)

                        repres = (repres1 + repres2) / 2
                        cove = (cove1 + cove2) / 2

                        repres = round_num(repres)
                        contrs = round_num(contrs)
                        pair = round_num(pair)
                        cove = round_num(cove)

                        from scipy.stats import hmean

                        h_mean = hmean([repres + .00001, contrs + .00001])  # Sums 0.00001 to avoid 0
                        h_mean = round_num(h_mean)

                        print("   %3d %3d [%2d]  " % (100 * repres, 100 * contrs, 100 * h_mean), end='')

                        h_mean = hmean([pair + .00001, cove + .00001])  # Sums 0.00001 to avoid 0
                        h_mean = round_num(h_mean)

                        print(" %3d %3d [%2d] " % (100 * pair, 100 * cove, 100 * h_mean), end='')


                        def harmonic_mean(l):
                            s = 0
                            if min(l) == 0:
                                return -1
                            for i in l:
                                s += 1 / i
                            m = s / len(l)
                            return 1 / m


                        evals = {}

                        evals['r1'] = 100 * evalu.representativiness(source1, summ1)
                        evals['r2'] = 100 * evalu.representativiness(source2, summ2)
                        evals['R'] = (evals['r1'] + evals['r2']) / 2

                        evals['C'] = 100 * evalu.contrastiviness(source1, source2, summ1, summ2)

                        evals['d1'] = 100 * evalu.diversity(source1, summ1)
                        evals['d2'] = 100 * evalu.diversity(source2, summ2)

                        evals['D'] = (evals['d1'] + evals['d2']) / 2

                        evals['H'] = harmonic_mean([evals['R'], evals['C'], evals['D']])

                        w1 = sum([summ1[i]['word_count'] for i in summ1])
                        w2 = sum([summ2[i]['word_count'] for i in summ2])

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

                        summScoresList[(evals['R'], evals['C'], evals['D'])] = (summ_idx_1, summ_idx_2)

    from statistics import stdev

    hr_medians = sorted(hr)[DTESTS:-DTESTS]
    hc_medians = sorted(hc)[DTESTS:-DTESTS]
    hd_medians = sorted(hd)[DTESTS:-DTESTS]
    hh_medians = sorted(hh)[DTESTS:-DTESTS]

    print()
    print(hh_medians)

    sthh = stdev(hh_medians)
    sthc = stdev(hc_medians)
    sthr = stdev(hr_medians)
    sthd = stdev(hd_medians)

    r = sum(hr) / len(hr)
    c = sum(hc) / len(hc)
    d = sum(hd) / len(hd)
    h = harmonic_mean([r, c, d])

    r_median_mean = sum(hr_medians) / len(hr_medians)
    c_median_mean = sum(hc_medians) / len(hc_medians)
    d_median_mean = sum(hd_medians) / len(hd_medians)
    h_median_mean = harmonic_mean([r, c, d])

    ht = sum(hh) / len(hh)
    ht_median_mean = sum(hh_medians) / len(hh_medians)

    results_msg = ''
    results_msg += '\n\n'
    results_msg += '              %3.0lf   %3.0lf   %3.0lf   [ %3.0lf ]    (%3.0lf)      ~%3.0lf' % (
        r_median_mean, c_median_mean, d_median_mean, h_median_mean, ht_median_mean, sthh)
    results_msg += '\n\n'
    results_msg += '             ~%3.0lf  ~%3.0lf  ~%3.0lf               ~%3.0lf' % (sthr, sthc, sthd, sthh)
    results_msg += '\n\n\n'
    results_msg += 'max           %3.0lf   %3.0lf   %3.0lf                %3.0lf' % (
        (max(hr_medians)), (max(hc_medians)), (max(hd_medians)), (max(hh_medians)))
    results_msg += '\n\n'
    results_msg += 'min           %3.0lf   %3.0lf   %3.0lf                %3.0lf' % (
        (min(hr_medians)), (min(hc_medians)), (min(hd_medians)), (min(hh_medians)))
    results_msg += '\n\n\n'
    results_msg += 'simple mean   %3.0lf   %3.0lf   %3.0lf     %3.0lf       \'%3.0lf\'      ~%3.0lf' % (
        r, c, d, h, ht, sthh)
    results_msg += '\n\n\n'

    avg_words1 = sum(h_words1) / len(h_words1)
    avg_words2 = sum(h_words2) / len(h_words2)
    avg_sentences1 = sum(h_sentences1) / len(h_sentences1)
    avg_sentences2 = sum(h_sentences2) / len(h_sentences2)

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

    fairness_rank = sorted(summScoresList.keys(),
                           key=lambda k: sqdiff(k, [r_median_mean, c_median_mean, d_median_mean]))

    summ_idx_f_1 = summScoresList[fairness_rank[0]][0]
    summ_idx_f_2 = summScoresList[fairness_rank[0]][1]

    summ1 = {i: source1[i] for i in summ_idx_f_1}
    summ2 = {i: source2[i] for i in summ_idx_f_2}

    print("\nMOST FAIR SUMMARY\n")
    summ_out = '\n'
    for i in summ_idx_f_1:
        summ_out += "%s " % (source1[i]['sentence'])
        summ_out += '\n'

    summ_out += '\n\n'

    for i in summ_idx_f_2:
        summ_out += "%s " % (source2[i]['sentence'])
        summ_out += '\n'

    w1 = sum([summ1[i]['word_count'] for i in summ1])
    w2 = sum([summ2[i]['word_count'] for i in summ2])

    summ_out += '\n\n\n'

    summ_out += 'sentences:   %3d  %3d\n' % (len(summ1), len(summ2))
    summ_out += '    words:   %3d  %3d' % (w1, w2)
    summ_out += '\n'

    evals = {}

    evals['r1'] = 100 * evalu.representativiness(source1, summ1)
    evals['r2'] = 100 * evalu.representativiness(source2, summ2)
    evals['R'] = (evals['r1'] + evals['r2']) / 2

    evals['C'] = 100 * evalu.contrastiviness(source1, source2, summ1, summ2)

    evals['d1'] = 100 * evalu.diversity(source1, summ1)
    evals['d2'] = 100 * evalu.diversity(source2, summ2)

    evals['D'] = (evals['d1'] + evals['d2']) / 2

    evals['H'] = harmonic_mean([evals['R'], evals['C'], evals['D']])

    w1 = sum([summ1[i]['word_count'] for i in summ1])
    w2 = sum([summ2[i]['word_count'] for i in summ2])

    summ_out += '\n\n'
    summ_out += '(%3.0lf %3.0lf)     %3.0lf   %3.0lf   %3.0lf   [[%3.0lf]]  ' % (
        evals['r1'], evals['r2'], evals['R'], evals['C'], evals['D'], evals['H'])
    summ_out += '\n\n'

    summ_out += '              %3.0lf   %3.0lf   %3.0lf    [%3.0lf]      ~%3.0lf' % (
        r_median_mean, c_median_mean, d_median_mean, ht_median_mean, sthh)

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
    results['meta']['run time'] = round(total_time, 2)

    underwrite_file('output/' + SOURCE1 + ' ' + SOURCE2 + ' (' + str(int(time())) + ').json', results)
