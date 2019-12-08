# Polarity representation

POLARITY_SCALE = 100  # To set the polarity scale (from -MAXPOLARITY to +MAXPOLARITY)


# Methods options

from collections import defaultdict

options = defaultdict(lambda : defaultdict())

options['Statistic']['variation'] = ['contrastive', 'noncontrastive'][0]
options['Statistic']['optimization'] = 'greedy'
options['Statistic']['min intensity'] = 1 * POLARITY_SCALE  # If (the absolute value of) the intensity of a sentence is lower than that, that sentence will not be in the summary.
options['Statistic']['alpha'] = 20

options['Similarity']['variation'] = ['R', 'C', 'D'][2]

options['Clustering']['variation'] = ['RF', 'CF'][1]
options['Clustering']['lambda'] = 0.5  # Weight for contrastivity vs. representativity
options['Clustering']['centroids'] = False  # Use centroids as the best sentences (faster, but worse result)
options['Clustering']['hungarian'] = False  # Use the Hungarian method of optimization
options['Clustering']['size_fac'] = 0.7  # To adjust summaries' size (this method doesn't allow to limit sentences)
options['Clustering']['repetitions'] = False  # To allow sentences to be repeated in the same summary

options['Ranking']['variation'] = ['contrastive', 'contrastive+representative', 'random'][1]
options['Ranking']['independent'] = False
options['Ranking']['ideal length'] = None


# Summary characteristics

LIM_WORDS = 100  # Sets the maximum number of words in each side of the summary
LIM_SENTENCES = 20  # Sets the number of sentences on each side.

ALLOW_REPETITION = False

LOW_PRIORITY_ASPECTS = ['PRODUTO']


# Evaluation options

REPEAT_TESTS = 10  # Times to repeat each test
DISCARD_TESTS = int(0.1*REPEAT_TESTS)  # Amount of top-rated and bottom-rated tests to be discarded to compute average


# Display options

VERBOSE_MODE = False
DEBUG_MODE = False


# Input files settings

DATA_DIR = '../input'

INPUT_FILES = [(), ('D1a','D1b'), ('D2a','D2b'), ('D3a','D3b'), ('D4a','D4b'), ('D5a','D5b'), ('D6a','D6b'), ('D7a','D7b'), ('D8a','D8b')]

DATASETS_TO_TEST = [INPUT_FILES[2]]
# DATASETS_TO_TEST = reversed(INPUT_FILES[:])

DIR_RESULTS = '../OUTPUT/results'
DIR_OUTPUT = '../OUTPUT/summaries'

def filepath(target):  # Get full path for the file with data of target
    return DATA_DIR + '/' + target + '.json'


