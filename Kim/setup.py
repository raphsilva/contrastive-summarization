from collections import defaultdict

SUMLEN = None  # Summary length (number of sentences on each side). Set 'None' for automatic.

MAX_WORDS = 2 * 100

LANGUAGE = 'portuguese'
LAMBDA = '0.5'
METHOD = 'CF'
CENTROIDS_AS_SUMMARY = 'False'
USE_HUNGARIAN_METHOD = 'False'
ALLOW_REPETITION = False

DATASET_ID = 8

ASPECTS_TAGS = ['none', 'join', 'only'][0]

SOURCE1, SOURCE2 = \
    [(), ('D1a', 'D1b'), ('D2a', 'D2b'), ('D3a', 'D3b'), ('D4a', 'D4b'), ('D5a', 'D5b'), ('D6a', 'D6b'), ('D7a', 'D7b'),
     ('D8a', 'D8b')][DATASET_ID]


SIZE_FAC = defaultdict(lambda : defaultdict (lambda : defaultdict(lambda : 0.7)))

DATAPATH = '../input'

SHOW_SUMMARY = False
SHOW_EVALUATION = True
SHOW_INDEXES = False


def filepath(target):
    return DATAPATH + '/' + target + '.json'
