import os
import sys
from time import time

sys.path.append(os.path.realpath('..'))

import common.evaluate as evaluate
import Ranking.summarization as optm
import common.output_files as output_files
import common.console_output as out
import common.structure as struct
from common.read_input import read_input
from OPTIONS import INPUT_DATASETS
from OPTIONS import DISCARD_TESTS
from OPTIONS import REPEAT_TESTS
from OPTIONS import filepath  # Get full path for the file with data of target
from OPTIONS import options
from OPTIONS import DIR_RESULTS, DIR_OUTPUT

METHOD_NAME = 'Ranking'

RANKING_MODE = options[METHOD_NAME]['variation']
INDEPENDENT_RANK = options[METHOD_NAME]['independent']
SENTENCE_IDEAL_LENGTH = options[METHOD_NAME]['ideal length']

method_info = [RANKING_MODE, INDEPENDENT_RANK, SENTENCE_IDEAL_LENGTH]

if SENTENCE_IDEAL_LENGTH != None:
    METHOD_NAME = 'Ranking+'


# Load input
def load_input():
    out.print_verbose(" \nLENDO ALVO 1")
    source1 = read_input(filepath(SOURCE1))
    out.print_verbose(" \nLENDO ALVO 2")
    source2 = read_input(filepath(SOURCE2))
    return source1, source2


EXECUTION_ID = str(int(time()) % 100000000)  # Execution code (will be in the results file name)

print('\n\nWill perform %d tests and discard %d(x2) best and worst\n\n' % (REPEAT_TESTS, DISCARD_TESTS))

for SOURCE1, SOURCE2 in INPUT_DATASETS:

    print(f'\n\n\n\n  =========datasets=======>  {SOURCE1} {SOURCE2}\n\n')

    out.print_verbose('Loading input')
    source1, source2 = load_input()
    out.print_verbose('Sizes of data sets: ', len(source1), len(source2))
    out.print_verbose('Words: ', struct.word_count(source1), struct.word_count(source2))

    '''
    /source.../ are structures that contain
    {
    0: { 'opinions': [('CÂMERA', 80.0)],
         'verbatim': 'Câmera boa.'}
    }
    '''

    evaluate.reset()  # To start evaluating summaries of the current sources.
    output_files.new_source(SOURCE1, SOURCE2, source1, source2, METHOD_NAME)  # Prepare output files for the current sources.

    map_scores_summary = {}

    distinct_summaries = set()

    time_total = 0

    out.print_verbose('Making summaries\n\n')

    print('     %5s %5s %5s %5s\n' % ('R', 'C', 'D', 'H'))

    for repeat in range(REPEAT_TESTS):
        time_initial = time()

        # Make summary

        summ_idx_1, summ_idx_2 = optm.make_contrastive_summary(source1, source2, RANKING_MODE)
        summ1 = {i: source1[i] for i in summ_idx_1}
        summ2 = {i: source2[i] for i in summ_idx_2}

        # Register time elapsed
        time_final = time()
        time_elapsed = time_final - time_initial
        time_total += time_elapsed

        # Register all summaries generated, ignoring order of sentences.
        s_id = ([sorted(summ_idx_1), sorted(summ_idx_2)])
        distinct_summaries.add(str(s_id))

        # Evaluate summary
        scores = evaluate.new_sample(source1, source2, summ1, summ2)
        print('%3d) %5d %5d %5d %5d' % (repeat + 1, scores['R'], scores['C'], scores['D'], scores['H']))

        # Write output file
        output_files.new_summary(summ1, summ2, scores, time_elapsed)

        # Make dictionary mapping evaluations to summaries
        map_scores_summary[(scores['R'], scores['C'], scores['D'])] = (summ_idx_1, summ_idx_2)

        # Evaluate source based on all summaries that were gotten.
    overall_scores = evaluate.source()

    # Saves evaluation information that will be written in json output files.
    output_files.overall_scores(overall_scores, time_total, distinct_summaries)

    # Choose the summary that best reflects the method's evaluation (based on the scores)
    means = [overall_scores['means'][s] for s in ['R', 'C', 'D']]
    summ_idx_1, summ_idx_2 = struct.get_summ_closest_to_scores(means, map_scores_summary)
    summ1 = {i: source1[i] for i in summ_idx_1}
    summ2 = {i: source2[i] for i in summ_idx_2}

    # Write summary in output file.
    output_files.write_summary(summ1, summ2, len(distinct_summaries))

    # Save output files in disc.
    output_files.write_files(SOURCE1, SOURCE2, METHOD_NAME, EXECUTION_ID)

print(f'\n\nSummaries and evaluations are in folders {DIR_OUTPUT} and {DIR_RESULTS}.')
