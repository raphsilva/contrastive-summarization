# From this project:
import optimization as optm
import output_format as out
from read_input import read_input
from setup import DATASETS_TO_TEST
from setup import DEBUGGING
from setup import OUTPUT_MODE
from setup import OVERVIEW_MODE
# Setup options
from setup import RANKING_MODE
from setup import REPEAT_TESTS, DISCARD_TESTS
from setup import VERBOSE_MODE
from setup import filepath  # Get full path for the file with data of target

if DEBUGGING:
    out.setDebugPrints(True)  # Choose whether or not to display information for debugging.


def print_verbose(*msg):
    if not VERBOSE_MODE:
        return
    out.printMessage(*msg)


# Load input
def load_input():
    print_verbose(" \nLENDO ALVO 1")
    source1 = read_input(filepath(SOURCE1))
    print_verbose(" \nLENDO ALVO 2")
    source2 = read_input(filepath(SOURCE2))
    return source1, source2


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

# /stats_.../ are structures of the form: 
'''
    {'tela': {'mean':  83, 'prob': 0.07, 'std': 0},
    'cor':  {'mean': -87, 'prob': 0.21, 'std': 1.73}}
'''

from time import time

exec_code = str(int(time()) % 100000000)

print('Will perform %d tests and discard %d(x2) best and worst\n\n' % (REPEAT_TESTS, DISCARD_TESTS))


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

    ini_time = time()

    print_verbose('Loading input')
    source1, source2 = load_input()
    print_verbose('Sizes of datasets: ', len(source1), len(source2))

    if VERBOSE_MODE:
        print("Size 1: ", len(source1))
        print("Size 2: ", len(source2))

    print_verbose('Sizes of datasets without low intensity sentences: ', len(source1), len(source2))

    print_verbose('Making summary')

    # Make contrastive summary

    for repeat in range(REPEAT_TESTS):

        optm.random_seed()

        summ_idx_1, summ_idx_2 = optm.make_contrastive_summary(source1, source2, RANKING_MODE)
        out.printProgress()
        out.printProgress()

        fin_time = time()
        elaps_time = fin_time - ini_time
        total_time += elaps_time

        summ1 = {i: source1[i] for i in summ_idx_1}
        summ2 = {i: source2[i] for i in summ_idx_2}

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
                print("%s " % (source1[i]['verbatim']))
            print("\n___ Produto 2\n")
            for i in summ_idx_2:
                print("%s " % (source2[i]['verbatim']))
