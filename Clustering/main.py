import metrics as evalu
import output_format as out
from interface import *
from language import setLanguage
from load_data import preprocess
from load_data import read_input
from setup import DATASETS_TO_TEST
from setup import DISCARD_TESTS
from setup import LANGUAGE
from setup import LIMIT_PAIRS
from setup import LIMIT_WORDS
from setup import REPEAT_TESTS
from setup import SHOW_EVALUATION
from setup import SHOW_INDEXES
from setup import SHOW_SUMMARY
from setup import filepath
from structure import idx_to_summ
from structure import word_count
from summarization import contrastiveness_first
from summarization import representativeness_first
from writefiles import overwrite_json


from setup import SIZE_FAC, METHOD

from time import time

EXECUTION_ID = str(int(time()) % 100000000)

FILE_RESULTS = 'results_ ' + EXECUTION_ID + '.txt'

print('Will perform %d tests and discard %d(x2) best and worst\n\n' % (REPEAT_TESTS, DISCARD_TESTS))

f = open(FILE_RESULTS, 'a')
f.write('%d tests, discard %d(x2) best and worst\n\n' % (REPEAT_TESTS, DISCARD_TESTS))
f.close()


SIZE_FAC_DEFAULT = SIZE_FAC

for SOURCE1, SOURCE2 in DATASETS_TO_TEST:

    SIZE_FAC = SIZE_FAC_DEFAULT

    # Setup language functions
    setLanguage(LANGUAGE)

    # Load dataset
    source1 = read_input(filepath(SOURCE1))
    source2 = read_input(filepath(SOURCE2))

    source1_proc = preprocess(source1)
    source2_proc = preprocess(source2)

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

    print('Will perform %d tests and discard %d(x2) best and worst\n\n' % (REPEAT_TESTS, DISCARD_TESTS))

    total_time = 0

    ini_time = time()

    all_summaries = []

    repeat = 0

    while repeat < REPEAT_TESTS:
        repeat += 1

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

                    if w1 + w2 > LIMIT_WORDS:  # Summary is too large; will repeat with smaller size factor.
                        repeat -= 1
                        SIZE_FAC *= 0.95
                        break
                    else:
                        SIZE_FAC *= 1.01
