# Method options

METHOD = ['RF', 'CF'][0]
LAMBDA = 0.5
PICK_CENTROIDS = False  #
HUNGARIAN_METHOD = False  # Whether the Hungarian Method should be used for optimization.
SIZE_FAC = 0.7  # To help control the summary size (since this method doesn't allow to directly control number of words)


# Summary characteristics

LIMIT_WORDS = 100  # Sets the maximum number of words in each side of the summary
LIMIT_SENTENCES = 'Auto'  # Sets the number of sentences on each side. Use 'Auto' for automatic.

ALLOW_REPETITION = False


# Evaluation options

REPEAT_TESTS = 10  # Times to repeat each test
DISCARD_TESTS = int(0.1*REPEAT_TESTS)  # Amount of top-rated and bottom-rated tests to be discarded to compute average


# Display options

VERBOSE_MODE = False


# Input files settings

DATA_DIR = '../input'

INPUT_FILES = [(), ('D1a','D1b'), ('D2a','D2b'), ('D3a','D3b'), ('D4a','D4b'), ('D5a','D5b'), ('D6a','D6b'), ('D7a','D7b'), ('D8a','D8b')]

DATASETS_TO_TEST = [INPUT_FILES[2]]

def filepath(target):  # Get full path for the file with data of target
    return DATA_DIR + '/' + target + '.json'

