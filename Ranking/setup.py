# Polarity representation
MAXPOLARITY = 100  # Sets the polarity scale (from -MAXPOLARITY to +MAXPOLARITY)


# Method options

RANKING_MODE = ['contrastive', 'contrastive+representative', 'random'][1]
INDEPENDENT_RANK = False
SENTENCE_IDEAL_LENGTH = None
METHOD = [RANKING_MODE, INDEPENDENT_RANK, SENTENCE_IDEAL_LENGTH]


# Summary characteristics

LIM_WORDS = 100  # Sets the maximum number of words in each side of the summary
LIM_SENTENCES = 20  # Sets the maximum number of sentences in each side of the summary


# Evaluation options

REPEAT_TESTS = 10  # Times to repeat each test
DISCARD_TESTS = int(0.1 * REPEAT_TESTS)  # Amount of top-rated and bottom-rated tests to be discarded to compute average without outliers


# Display options

VERBOSE_MODE = False  # To print statistics and status information (progress is always shown)


# Input files settings

DATA_DIR = "../input"

INPUT_FILES = [(), ('D1a', 'D1b'), ('D2a', 'D2b'), ('D3a', 'D3b'), ('D4a', 'D4b'), ('D5a', 'D5b'), ('D6a', 'D6b'), ('D7a', 'D7b'), ('D8a', 'D8b')]

DATASETS_TO_TEST = [INPUT_FILES[2]]

LOW_PRIORITY_ASPECTS = ['_GENERIC']  # Aspects that are send to the end of the queue

def filepath(target):  # Get full path for the file with data of target
    return DATA_DIR + '/' + target + '.json'


if VERBOSE_MODE:
    import output_format as out

    out.printMessage('Datasets: ', DATASETS_TO_TEST)
    out.printMessage()
    out.printMessage('Limit of words (per side): ', LIM_WORDS)
    out.printMessage()
    out.printMessage()
