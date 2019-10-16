# From Python standard library:
from os import mkdir
from time import time

import evaluate
# From this project:
import method
import output_files
import output_format as out
import structure as struct
from read_input import read_input
from setup import ALPHA
from setup import DATASETS_TO_TEST
from setup import DEBUG_MODE
from setup import DISCARD_TESTS
from setup import METHOD
# Setup options
from setup import MIN_INTENSITY_IN_SUMMARY  # Sets the minimum intensity that a sentence in the summary has to have
from setup import OPTM_MODE
from setup import REPEAT_TESTS
from setup import VERBOSE_MODE
from setup import filepath  # Get full path for the file with data of target
from summarization import summarize

PATH_RESULTS = 'RESULTS'
PATH_OUTPUT = 'OUTPUT'

try:
    mkdir(PATH_RESULTS)
    mkdir(PATH_OUTPUT)
except:
    pass

EXECUTION_ID = str(int(time()) % 100000000)  # Execution code (will be in the results file name)

if DEBUG_MODE:
    out.setDebugPrints(True)  # Choose whether or not to display information for debugging.


def print_verbose(*msg):
    if not VERBOSE_MODE:
        return
    out.printMessage(*msg)


def remove_low_intensity(source):
    # Remove sentences with low intensity. 
    # Will bypass any sentence which the intensity is lower than MIN_INTENS_IN_SUMMARY.
    for i in dict(source):
        if source[i]['intensity'] < MIN_INTENSITY_IN_SUMMARY:
            del source[i]
    return source


print('\n\nWill perform %d tests and discard %d(x2) best and worst\n\n' % (REPEAT_TESTS, DISCARD_TESTS))

for SOURCE1, SOURCE2 in DATASETS_TO_TEST:

    map_scores_summary = {}

    time_total = 0

    print(f'\n\n\n\n  =========datasets=======>  {SOURCE1} {SOURCE2}\n\n')

    print_verbose('Loading input')
    source1 = read_input(filepath(SOURCE1))
    source2 = read_input(filepath(SOURCE2))
    print_verbose('Sizes of datasets: ', len(source1), len(source2))
    source1 = remove_low_intensity(source1)
    source2 = remove_low_intensity(source2)
    print_verbose('Sizes of datasets after cleaning: ', len(source1), len(source2))
    wc1 = struct.word_count(source1)
    wc2 = struct.word_count(source2)
    print_verbose('Words: ', wc1, wc2)

    output_files.new_source(SOURCE1, SOURCE2, source1, source2)

    '''
    /source.../ are structures of the form
    {
    0: {'intensity': 80.0,
        'opinions': [('CÂMERA', 80.0)],
        'sent': {'CÂMERA': 88},
        'word_count': 2,
        'verbatim': 'Câmera boa.'},
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

    '''
     /stats_.../ are structures of the form: 
        {'tela': {'mean':  83, 'prob': 0.07, 'std': 0},
        'cor':  {'mean': -87, 'prob': 0.21, 'std': 1.73}}
    '''

    all_summaries = []

    if VERBOSE_MODE:
        print_verbose('\nOverview of opinions in the source for each entity:')
        struct.printOverview(stats_source_1)
        struct.printOverview(stats_source_2)

    print_verbose('Sizes of data sets without low intensity sentences: ', len(source1), len(source2))

    print_verbose('Making summaries\n\n')

    print('     %5s %5s %5s %5s\n' % ('R', 'C', 'D', 'H'))

    evaluate.reset()

    for repeat in range(REPEAT_TESTS):

        time_initial = time()

        # Make summary
        summ_idx_1, summ_idx_2 = summarize(source1, source2, stats_source_1, stats_source_2, METHOD, OPTM_MODE)
        summ1 = {i: source1[i] for i in summ_idx_1}
        summ2 = {i: source2[i] for i in summ_idx_2}

        # Register time elapsed
        time_final = time()
        time_total += time_final - time_initial

        # Register all summaries generated, ignoring order of sentences.
        s_id = (sorted(summ_idx_1), sorted(summ_idx_2))
        if s_id not in all_summaries:
            all_summaries.append(s_id)

        # Evaluate summary
        scores = evaluate.new_sample(source1, source2, summ1, summ2)
        print('%3d) %5d %5d %5d %5d' % (repeat + 1, scores['R'], scores['C'], scores['D'], scores['H']))

        # Register parameters used
        summary_parameters = [METHOD, OPTM_MODE, 'alpha=' + str(ALPHA)]

        # Write output file
        output_files.new_summary(summ1, summ2, scores, summary_parameters)

        # Make dictionary mapping evaluations to summaries
        map_scores_summary[(scores['R'], scores['C'], scores['D'])] = (summ_idx_1, summ_idx_2)

    overall_scores = evaluate.overall_samples()

    output_files.overall_scores(overall_scores, time_total, all_summaries)


    # Choose the summary that best reflects the method's evaluation
    # (based on the scores gotten after running the method several times for this data set)

    means = [overall_scores['means'][s] for s in ['R', 'C', 'D']]

    summ_idx_f_1, summ_idx_f_2 = struct.get_summ_closest_to_scores(means, map_scores_summary)

    summ1 = {i: source1[i] for i in summ_idx_f_1}
    summ2 = {i: source2[i] for i in summ_idx_f_2}

    output_files.write_summary(summ1, summ2, len(all_summaries))

    if DEBUG_MODE:
        out.printMessage('\nOverview of opinions in the summary for each entity:')
        sum_stats_1 = struct.aspects_stats(summ1)
        sum_stats_2 = struct.aspects_stats(summ2)
        struct.printOverview(sum_stats_1)
        struct.printOverview(sum_stats_2)
        out.printMessage('\nOpinions in the summary for each entity:')
        for i in summ_idx_1:
            out.printinfo("      %4d)   %s " % (i, source1[i]['opinions']))
        print()
        for i in summ_idx_2:
            out.printinfo("      %4d)   %s " % (i, source2[i]['opinions']))

    output_files.write_files(SOURCE1, SOURCE2, EXECUTION_ID)

    method.save_caches()

print(f'\n\nSummaries and evaluations are in folders {PATH_OUTPUT} and {PATH_RESULTS}.')
