import os
import sys
from time import time

sys.path.append(os.path.realpath('..'))

import common.evaluate as evaluate
import Statistic.method as method
import common.output_files as output_files
import Statistic.output_format as out
import Statistic.structure as struct
from Statistic.read_input import read_input

from Statistic.summarization import summarize

from options import DATASETS_TO_TEST
from options import DISCARD_TESTS
from options import DEBUG_MODE
from options import REPEAT_TESTS
from options import filepath  # Get full path for the file with data of target

from options import options
OPTM_MODE = options['Statistic']['optimization']
METHOD = options['Statistic']['strategy']
ALPHA = options['Statistic']['alpha']

PATH_RESULTS = 'RESULTS'
PATH_OUTPUT = 'OUTPUT'

os.makedirs(PATH_RESULTS, exist_ok=True)
os.makedirs(PATH_OUTPUT, exist_ok=True)

EXECUTION_ID = str(int(time()) % 100000000)  # Execution code (will be in the results file name)


print('\n\nWill perform %d tests and discard %d(x2) best and worst\n\n' % (REPEAT_TESTS, DISCARD_TESTS))

for SOURCE1, SOURCE2 in DATASETS_TO_TEST:

    print(f'\n\n\n\n  =========datasets=======>  {SOURCE1} {SOURCE2}\n\n')

    out.print_verbose('Loading input')
    source1 = read_input(filepath(SOURCE1))
    source2 = read_input(filepath(SOURCE2))
    out.print_verbose('Sizes of data sets: ', len(source1), len(source2))
    source1 = method.remove_low_intensity(source1)
    source2 = method.remove_low_intensity(source2)
    out.print_verbose('Sizes of data sets after cleaning: ', len(source1), len(source2))
    out.print_verbose('Words: ', struct.word_count(source1), struct.word_count(source2))

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

    # Get statistics about aspects in the source (mean, standard deviation, probability)
    stats_source_1 = struct.aspects_stats(source1)
    stats_source_2 = struct.aspects_stats(source2)

    '''
     /stats_.../ are structures of the form: 
        {'tela': {'mean':  83, 'prob': 0.07, 'std': 0},
        'cor':   {'mean': -87, 'prob': 0.21, 'std': 1.73}}
    '''

    evaluate.reset()  # To start evaluating summaries of the current sources.
    output_files.new_source(SOURCE1, SOURCE2, source1, source2, 'Statistic')  # Prepare output files for the current sources.

    map_scores_summary = {}

    distinct_summaries = set()

    time_total = 0

    out.print_verbose('Making summaries\n\n')

    print('     %5s %5s %5s %5s\n' % ('R', 'C', 'D', 'H'))


    for repeat in range(REPEAT_TESTS):

        time_initial = time()

        # Make summary
        summ_idx_1, summ_idx_2 = summarize(source1, source2, stats_source_1, stats_source_2, METHOD, OPTM_MODE)
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

        # Register parameters used
        summary_parameters = [METHOD, OPTM_MODE, 'alpha=' + str(ALPHA)]

        # Write output file
        output_files.new_summary(summ1, summ2, scores, summary_parameters,time_elapsed)

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

    if DEBUG_MODE:
        output_files.print_stats(summ_idx_1, summ_idx_2, source1, source2)

    # Save output files in disc.
    output_files.write_files(SOURCE1, SOURCE2, EXECUTION_ID)

    # Update cache.
    method.save_caches()

print(f'\n\nSummaries and evaluations are in folders {PATH_OUTPUT} and {PATH_RESULTS}.')
