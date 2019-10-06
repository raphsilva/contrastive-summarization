DEBUGGING = False

RANKING_MODE = ['contrastive', 'contrastive+representative', 'random'][1]

INDEPENDENT_RANK = False

SENTENCE_IDEAL_LENGTH = None

REPEAT_TESTS = 10  # Times to repeat each test
DISCARD_TESTS = int(0.1 * REPEAT_TESTS)  # Amount of top-rated and bottom-rated tests to be discarded to compute average without outliers

# Display options

VERBOSE_MODE = False  # To print statistics and status information (progress is always shown)
EVALUATION_MODE = True  # To print evaluation metrics results
OUTPUT_MODE = False  # To print the summaries
OVERVIEW_MODE = False

METHOD = [RANKING_MODE, INDEPENDENT_RANK, SENTENCE_IDEAL_LENGTH]

# Input files 

DATA_DIR = "../input"

INPUT_FILES = [(), ('D1a', 'D1b'), ('D2a', 'D2b'), ('D3a', 'D3b'), ('D4a', 'D4b'), ('D5a', 'D5b'), ('D6a', 'D6b'), ('D7a', 'D7b'), ('D8a', 'D8b')]

DATASETS_TO_TEST = [INPUT_FILES[2]]

# Scale options

MAXPOLARITY = 100  # Sets the polarity scale (from -MAXPOLARITY to +MAXPOLARITY)

# Summary characteristics

LIM_SENTENCES = 20  # Sets the maximum number of SENTENCES in each side of the summary
LIM_WORDS = 150  # Sets the maximum number of WORDS in each side of the summary

LOW_PRIORITY_ASPECTS = ['_GENERIC']  # Aspects that are send to the end of the queue


# Get full path for the file with data of target 
def filepath(target):
    return DATA_DIR + '/' + target + '.json'


if VERBOSE_MODE or EVALUATION_MODE:
    import output_format as out

    out.printMessage('Datasets: ', DATASETS_TO_TEST)
    out.printMessage()
    out.printMessage('Limit of words (per side): ', LIM_WORDS)
    out.printMessage()
    out.printMessage()
