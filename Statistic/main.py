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
from setup import OUTPUT_MODE
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


def print_result(*msg):
    print(*msg, end='', flush=True)


def remove_low_intensity(source):
    # Remove sentences with low intensity. 
    # Will bypass any sentence which the intensity is lower than MIN_INTENS_IN_SUMMARY.
    for i in dict(source):
        if source[i]['intensity'] < MIN_INTENSITY_IN_SUMMARY:
            del source[i]
    return source


print('Will perform %d tests and discard %d(x2) best and worst\n\n' % (REPEAT_TESTS, DISCARD_TESTS))

for SOURCE1, SOURCE2 in DATASETS_TO_TEST:

    summScoresList = {}

    time_total = 0

    OUTPUT_FILE = f'OUTPUT/out_{EXECUTION_ID}_{SOURCE1[:-1]}.txt'

    print(f'\n\n\n ===============datasets======>  {SOURCE1} {SOURCE2}\n\n')

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

    print_verbose('Sizes of datasets without low intensity sentences: ', len(source1), len(source2))

    print_verbose('Making summaries\n\n')

    print('%3s  %5s %5s %5s %5s\n' % ('n', 'R', 'C', 'D', 'H'))

    evaluate.reset()

    for repeat in range(REPEAT_TESTS):

        # Display progress
        out.printProgress('   %3d%% ' % (100 * repeat / REPEAT_TESTS), end="\n")

        time_initial = time()

        # Make summary
        summ_idx_1, summ_idx_2 = summarize(source1, source2, stats_source_1, stats_source_2, METHOD, OPTM_MODE)

        summ1 = {i: source1[i] for i in summ_idx_1}
        summ2 = {i: source2[i] for i in summ_idx_2}

        # Register all summaries generated, ignoring order of sentences.
        s_id = (sorted(summ_idx_1), sorted(summ_idx_2))
        if s_id not in all_summaries:
            all_summaries.append(s_id)

        # Register time elapsed
        time_final = time()
        time_total += time_final - time_initial

        # Evaluate summary
        evals = evaluate.new_sample(source1, source2, summ1, summ2)
        print('%3d) %5d %5d %5d %5d' % (repeat+1, evals['R'], evals['C'], evals['D'], evals['H']))

        # Register parameters used
        summary_parameters = [METHOD, OPTM_MODE, 'alpha=' + str(ALPHA)]

        # Write output file
        output_files.new_summary(summ1, summ2, evals, summary_parameters)

        # Make dictionary mapping evaluations to summaries
        summScoresList[(evals['R'], evals['C'], evals['D'])] = (summ_idx_1, summ_idx_2)

    overall_scores = evaluate.overall_samples()

    output_files.overall_scores(overall_scores, time_total, all_summaries)


    # Choose the summary that best reflects the method's evaluation
    # (based on the scores gotten after running the method several times for this dataset)

    def sqdiff(l1, l2):  # To determine difference between two summaries scores
        r = 0
        for i in range(len(l1)):
            r += pow(l1[i] - l2[i], 2)
        return r

    print()

    means = [overall_scores['means'][s] for s in ['R', 'C', 'D']]
    fairness_rank = sorted(summScoresList.keys(), key=lambda k: sqdiff(k, means))

    summ_idx_f_1 = summScoresList[fairness_rank[0]][0]
    summ_idx_f_2 = summScoresList[fairness_rank[0]][1]

    summ1 = {i: source1[i] for i in summ_idx_f_1}
    summ2 = {i: source2[i] for i in summ_idx_f_2}

    if VERBOSE_MODE:
        print_verbose('\nOverview of opinions in the summary for each entity:')
        sum_stats_1 = struct.aspects_stats(summ1)
        sum_stats_2 = struct.aspects_stats(summ2)
        struct.printOverview(sum_stats_1)
        struct.printOverview(sum_stats_2)
        print_verbose('\nOpinions in the summary for each entity:')
        for i in summ_idx_1:
            out.printinfo("      %4d)   %s " % (i, source1[i]['opinions']))
        print()
        for i in summ_idx_2:
            out.printinfo("      %4d)   %s " % (i, source2[i]['opinions']))

    print("\nSUMMARY THAT BEST REFLECTS THIS METHOD'S EVALUATION (based on %d executions that were performed)\n" % (REPEAT_TESTS))
    summ_out = '\n'
    for i in summ_idx_f_1:
        summ_out += "%s " % (source1[i]['verbatim'])
        summ_out += "\n"

    summ_out += '\n\n'

    for i in summ_idx_f_2:
        summ_out += "%s " % (source2[i]['verbatim'])
        summ_out += "\n"

    w1 = sum([summ1[i]['word_count'] for i in summ1])
    w2 = sum([summ2[i]['word_count'] for i in summ2])

    summ_out += '\n\n\n'

    summ_out += '          sentences:   %3d  %3d\n' % (len(summ1), len(summ2))
    summ_out += '              words:   %3d  %3d' % (w1, w2)
    summ_out += 'different summaries: %d:' % (len(all_summaries))
    summ_out += '\n'

    print(summ_out)

    print('\n')
    print('\n')

    f = open(OUTPUT_FILE, 'w')
    f.write(summ_out)
    f.close()

    output_files.write_files(SOURCE1, SOURCE2, EXECUTION_ID)

    method.save_caches()

print(f'Summaries and evaluations are in folders {PATH_OUTPUT} and {PATH_RESULTS}')