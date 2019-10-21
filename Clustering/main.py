import os
from time import time

import evaluate
import output_files
import output_format as out
from load_data import preprocess
from load_data import read_input
from setup import DATASETS_TO_TEST
from setup import DISCARD_TESTS
from setup import HUNGARIAN_METHOD
from setup import LAMBDA
from setup import LIMIT_WORDS
from setup import METHOD
from setup import PICK_CENTROIDS
from setup import REPEAT_TESTS
from setup import SIZE_FAC
from setup import filepath  # Get full path for the file with data of target
from structure import get_summ_closest_to_scores
from structure import idx_to_summ
from summarization import contrastiveness_first
from summarization import representativeness_first

PATH_RESULTS = 'RESULTS'
PATH_OUTPUT = 'OUTPUT'

os.makedirs(PATH_RESULTS, exist_ok=True)
os.makedirs(PATH_OUTPUT, exist_ok=True)

EXECUTION_ID = str(int(time()) % 100000000)  # Execution code (will be in the results file name)

print('\n\nWill perform %d tests and discard %d(x2) best and worst\n\n' % (REPEAT_TESTS, DISCARD_TESTS))

SIZE_FAC_DEFAULT = SIZE_FAC

for SOURCE1, SOURCE2 in DATASETS_TO_TEST:

    SIZE_FAC = SIZE_FAC_DEFAULT

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

    repeat = 0
    discarded = 0
    while repeat < REPEAT_TESTS:

        repeat += 1

        time_initial = time()

        # Make summary

        ini_time = time()

        if METHOD == 'CF':

            summ_idx_A = contrastiveness_first(set1_pos, set2_neg, '+', '-', SIZE_FAC, LAMBDA, PICK_CENTROIDS,
                                               HUNGARIAN_METHOD)
            summ_idx_B = contrastiveness_first(set1_neg, set2_pos, '-', '+', SIZE_FAC, LAMBDA, PICK_CENTROIDS,
                                               HUNGARIAN_METHOD)

        elif METHOD == 'RF':

            summ_idx_A = representativeness_first(set1_pos, set2_neg, '+', '-', LAMBDA,
                                                  PICK_CENTROIDS, HUNGARIAN_METHOD)
            summ_idx_B = representativeness_first(set1_neg, set2_pos, '-', '+', LAMBDA,
                                                  PICK_CENTROIDS, HUNGARIAN_METHOD)

        # Indexes of each side of the summary
        summ_idx_1 = [i[0] for i in summ_idx_A + summ_idx_B]
        summ_idx_2 = [i[1] for i in summ_idx_A + summ_idx_B]

        summ1 = idx_to_summ(source1, summ_idx_1)
        summ2 = idx_to_summ(source2, summ_idx_2)

        w1 = sum([summ1[i]['word_count'] for i in summ1])
        w2 = sum([summ2[i]['word_count'] for i in summ2])

        if w1 + w2 > 2 * LIMIT_WORDS:  # Summary is too large; will repeat with smaller size factor.
            discarded += 1
            repeat -= 1
            SIZE_FAC *= 0.95
            print('too large')
            continue
        else:  # Summary succeeded
            SIZE_FAC *= 1.01

        # Register time elapsed
        time_final = time()
        time_total += time_final - time_initial

        # Register all summaries generated, ignoring order of sentences.
        s_id = ([sorted(summ_idx_1), sorted(summ_idx_2)])
        distinct_summaries.add(str(s_id))

        # Evaluate summary
        scores = evaluate.new_sample(source1, source2, summ1, summ2)
        print('%3d) %5d %5d %5d %5d' % (repeat, scores['R'], scores['C'], scores['D'], scores['H']))

        # Register parameters used
        summary_parameters = [METHOD, 'lambda=' + str(LAMBDA), PICK_CENTROIDS, HUNGARIAN_METHOD]

        # Write output file
        output_files.new_summary(summ1, summ2, scores, summary_parameters)

        # Make dictionary mapping evaluations to summaries
        map_scores_summary[(scores['R'], scores['C'], scores['D'])] = (summ_idx_1, summ_idx_2)

    print(f'\nDiscarded {discarded} summaries that didn\'t fit into size limit.\n')

    # Evaluate source based on all summaries that were gotten.
    overall_scores = evaluate.source()

    # Saves evaluation information that will be written in json output files.
    output_files.overall_scores(overall_scores, time_total, distinct_summaries)

    # Choose the summary that best reflects the method's evaluation (based on the scores)
    means = [overall_scores['means'][s] for s in ['R', 'C', 'D']]
    summ_idx_1, summ_idx_2 = get_summ_closest_to_scores(means, map_scores_summary)
    summ1 = {i: source1[i] for i in summ_idx_1}
    summ2 = {i: source2[i] for i in summ_idx_2}

    # Write summary in output file.
    output_files.write_summary(summ1, summ2, len(distinct_summaries))

    # Save output files in disc.
    output_files.write_files(SOURCE1, SOURCE2, EXECUTION_ID)

print(f'\n\nSummaries and evaluations are in folders {PATH_OUTPUT} and {PATH_RESULTS}.')
