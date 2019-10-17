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

import os
from time import time

import evaluate
import output_files
import output_format as out
import structure as struct
from setup import DATASETS_TO_TEST
from setup import DISCARD_TESTS
from setup import METHOD
from setup import REPEAT_TESTS
from setup import filepath  # Get full path for the file with data of target

PATH_RESULTS = 'RESULTS'
PATH_OUTPUT = 'OUTPUT'

os.makedirs(PATH_RESULTS, exist_ok=True)
os.makedirs(PATH_OUTPUT, exist_ok=True)

EXECUTION_ID = str(int(time()) % 100000000)  # Execution code (will be in the results file name)


print('\n\nWill perform %d tests and discard %d(x2) best and worst\n\n' % (REPEAT_TESTS, DISCARD_TESTS))


SIZE_FAC_DEFAULT = SIZE_FAC

for SOURCE1, SOURCE2 in DATASETS_TO_TEST:

    SIZE_FAC = SIZE_FAC_DEFAULT

    # Setup language functions
    setLanguage(LANGUAGE)

    print(f'\n\n\n\n  =========datasets=======>  {SOURCE1} {SOURCE2}\n\n')

    out.print_verbose('Loading input')
    source1 = read_input(filepath(SOURCE1))
    source2 = read_input(filepath(SOURCE2))
    out.print_verbose('Sizes of data sets: ', len(source1), len(source2))

    '''
    /source.../ are structures of the form
    {
    0: {'intensity': 80.0,
        'opinions': [('CÂMERA', 80.0)],
        'sent': {'CÂMERA': 88},
        'word_count': 2,
        'verbatim': 'Câmera boa.'},
    2: {'intensity': 80.0,
        'opinions': [('DESEMPENHO',  -80.0),
                     ('DESEMPENHO',  -80.0),
                     ('RESISTÊNCIA', -80.0)],
        'sent': {'DESEMPENHO': -94, 'RESISTÊNCIA': -88},
        'verbatim': 'Entretanto, na primeira semana de uso já ralou facilmente, '
                    'esquenta muito com os dados móveis ligados e trava, mesmo '
                    'que raramente.',
        'word_count': 21}
    }
    '''

    source1_proc = preprocess(source1)
    source2_proc = preprocess(source2)

    set1_pos = source1_proc['+']
    set1_neg = source1_proc['-']
    set2_pos = source2_proc['+']
    set2_neg = source2_proc['-']

    evaluate.reset()  # To start evaluating summaries of the current sources.
    output_files.new_source(SOURCE1, SOURCE2, source1, source2)  # Prepare output files for the current sources.

    map_scores_summary = {}

    distinct_summaries = set()

    time_total = 0

    out.print_verbose('Making summaries\n\n')

    print('     %5s %5s %5s %5s\n' % ('R', 'C', 'D', 'H'))

    for repeat in range(REPEAT_TESTS):

        time_initial = time()

        # Make summary

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

                    # Indexes of each side of the summary
                    summ_idx_1 = [i[0] for i in summ_idx_A + summ_idx_B]
                    summ_idx_2 = [i[1] for i in summ_idx_A + summ_idx_B]

                    summ1 = idx_to_summ(source1, summ_idx_1)
                    summ2 = idx_to_summ(source2, summ_idx_2)

                    # Register time elapsed
                    time_final = time()
                    time_total += time_final - time_initial

                    # Register all summaries generated, ignoring order of sentences.
                    s_id = ([sorted(summ_idx_1), sorted(summ_idx_2)])
                    distinct_summaries.add(str(s_id))

                    # Evaluate summary
                    scores = evaluate.new_sample(source1, source2, summ1, summ2)
                    print('%3d) %5d %5d %5d %5d' % (repeat + 1, scores['R'], scores['C'], scores['D'], scores['H']))

                    # Register parameters used
                    summary_parameters = [METHOD, 'lambda=' + str(LAMBDA), centroid_choices, hungarian_choices]

                    # Write output file
                    output_files.new_summary(summ1, summ2, scores, summary_parameters)

                    # Make dictionary mapping evaluations to summaries
                    map_scores_summary[(scores['R'], scores['C'], scores['D'])] = (summ_idx_1, summ_idx_2)