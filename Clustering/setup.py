LIMIT_SENTENCES = None  # Summary length (number of sentences on each side). Set 'None' for automatic.

LIMIT_WORDS = 100

LANGUAGE = ['portuguese'][0]

METHOD = ['RF', 'CF'][0]
LAMBDA = 0.5
CENTROIDS_AS_SUMMARY = False
USE_HUNGARIAN_METHOD = False
ALLOW_REPETITION = False

REPEAT_TESTS = 10  # Times to repeat each test
DISCARD_TESTS = int(0.1*REPEAT_TESTS)  # Amount of top-rated and bottom-rated tests to be discarded to compute average

DATA_DIR = '../input'

INPUT_FILES = [(), ('D1a','D1b'), ('D2a','D2b'), ('D3a','D3b'), ('D4a','D4b'), ('D5a','D5b'), ('D6a','D6b'), ('D7a','D7b'), ('D8a','D8b')]

DATASETS_TO_TEST = [INPUT_FILES[2]]

VERBOSE_MODE = True

SIZE_FAC = 0.7

def filepath(target):
    return DATA_DIR + '/' + target + '.json'


