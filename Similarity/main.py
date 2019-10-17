# From this project:
import evaluation as evalu
import optimization as optm
import output_format as out
import structure as struct
from read_input import read_input
from setup import DATASETS_TO_TEST
from setup import DEBUG_MODE
from setup import EVALUATION_MODE
# Setup options
from setup import LIM_SENTENCES  # Sets the maximum number of SENTENCES in each side of the summary
from setup import LIM_WORDS  # Sets the maximum number of WORDS in each side of the summary
from setup import OUTPUT_MODE
from setup import VERBOSE_MODE
from setup import filepath  # Get full path for the file with data of target
from structure import word_count
from writefiles import overwrite_json

if DEBUG_MODE:
    out.setDebugPrints(True)


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

    print_verbose(" \nLENDO ALVO 2")
    source2 = read_input(filepath(SOURCE2))

    return source1, source2


from time import time

exec_code = str(int(time()) % 100000000)

FILE_RESULTS = 'results_' + exec_code + '.txt'

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


for SOURCE1, SOURCE2 in DATASETS_TO_TEST:

    summScoresList = {}

    OUTPUT_FILE = 'out' + exec_code + '_' + SOURCE1[:-1] + '.txt'

    print('\n\n\n\n ============  ', SOURCE1, SOURCE2)
    print('\n\n')

    total_time = 0

    print_verbose('Loading input')
    source1, source2 = load_input()
    print_verbose('Sizes of datasets: ', len(source1), len(source2))

    wc1 = struct.word_count(source1)
    wc2 = struct.word_count(source2)

    print("Size 1: ", len(source1))
    print("Size 2: ", len(source2))

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

    # /stats_.../ are structures of the form: 
    '''
        {'tela': {'mean':  83, 'prob': 0.07, 'std': 0},
        'cor':  {'mean': -87, 'prob': 0.21, 'std': 1.73}}
    '''

    all_summaries = []

    print(len(source1))
    print(len(source2))
    print()

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

    for METHOD in ['CONTRASTIVE']:

        ini_time = time()

        if VERBOSE_MODE:
            print_verbose('\nOpinions in the summary for each entity:')
            print_verbose('\nOverview of opinions in the source for each entity:')
            struct.printOverview(stats_source_1)
            struct.printOverview(stats_source_2)

        print_verbose('Sizes of datasets without low intensity sentences: ', len(source1), len(source2))

        print_verbose('Making summary')

        # Make contrastive summary

        w_e1_pos = word_count(e1_pos)
        w_e1_neg = word_count(e1_neg)
        w_e2_pos = word_count(e2_pos)
        w_e2_neg = word_count(e2_neg)

        w_tot = w_e1_pos + w_e1_neg + w_e2_pos + w_e2_neg

        size_A_proportion = w_e1_pos + w_e2_neg
        size_B_proportion = w_e1_neg + w_e2_pos

        size_A = LIM_WORDS * size_A_proportion / (size_A_proportion + size_B_proportion)
        size_B = LIM_WORDS * size_B_proportion / (size_A_proportion + size_B_proportion)

        for repeat in range(RTESTS):

            from optimization import random_seed

            random_seed()

            pr = repeat / RTESTS
            out.printProgress('   %3d%%   %s %s' % (100 * pr, SOURCE1, SOURCE2), end="\r")

            summ_idx_1A, summ_idx_2A = optm.MakeContrastiveSummary(e1_pos, e2_neg, stats_e1_pos, stats_e2_neg,
                                                                   size_A, size_A)
            summ_idx_1B, summ_idx_2B = optm.MakeContrastiveSummary(e1_neg, e2_pos, stats_e1_neg, stats_e2_pos,
                                                                   size_B, size_B)

            summ_idx_1 = summ_idx_1A + summ_idx_1B
            summ_idx_2 = summ_idx_2A + summ_idx_2B

            out.printProgress()
            out.printProgress()

            fin_time = time()
            elaps_time = fin_time - ini_time
            total_time += elaps_time

            summ1 = {i: source1[i] for i in summ_idx_1}
            summ2 = {i: source2[i] for i in summ_idx_2}

            sum_stats_1 = struct.aspects_stats(summ1)
            sum_stats_2 = struct.aspects_stats(summ2)




