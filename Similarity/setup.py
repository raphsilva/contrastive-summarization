# Polarity representation
MAXPOLARITY = 100  # Sets the polarity scale (from -MAXPOLARITY to +MAXPOLARITY)


# Method options

METHOD = ['R', 'C', 'D'][1]


# Summary characteristics

LIM_WORDS = 100  # Sets the maximum number of words in each side of the summary
LIM_SENTENCES = 20  # Sets the maximum number of sentences in each side of the summary


# Evaluation options

REPEAT_TESTS = 10  # Times to repeat each test
DISCARD_TESTS = int(0.1 * REPEAT_TESTS)  # Amount of top-rated and bottom-rated tests to be discarded to compute average


# Display options

VERBOSE_MODE = False  # To print statistics and status information
DEBUG_MODE = False


# Input files settings

DATA_DIR = "../input"

INPUT_FILES = [(), ('D1a', 'D1b'), ('D2a', 'D2b'), ('D3a', 'D3b'), ('D4a', 'D4b'), ('D5a', 'D5b'), ('D6a', 'D6b'), ('D7a', 'D7b'), ('D8a', 'D8b')]

DATASETS_TO_TEST = [INPUT_FILES[2]]

def filepath(target):  # Get full path for the file with data of target
    return DATA_DIR + '/' + target + '.json'


if VERBOSE_MODE:
    import output_format as out

    out.printMessage('Datasets: ', DATASETS_TO_TEST)
    out.printMessage()
    out.printMessage('Method: ', METHOD)
    out.printMessage('Limit of sentences (per side): ', LIM_SENTENCES)
    out.printMessage('Limit of words (per side): ', LIM_WORDS)
    out.printMessage()
    out.printMessage()
