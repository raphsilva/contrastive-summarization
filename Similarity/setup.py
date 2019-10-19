# Execution options
METHOD = ['R', 'C', 'D'][1]

REPEAT_TESTS = 10  # Times to repeat each test
DISCARD_TESTS = int(0.1 * REPEAT_TESTS)  # Amount of top-rated and bottom-rated tests to be discarded to compute average

# Display options

VERBOSE_MODE = False  # To print statistics and status information (progress is always shown)
DEBUG_MODE = False

# Input files

DATA_DIR = "../input"

INPUT_FILES = [(), ('D1a', 'D1b'), ('D2a', 'D2b'), ('D3a', 'D3b'), ('D4a', 'D4b'), ('D5a', 'D5b'), ('D6a', 'D6b'), ('D7a', 'D7b'), ('D8a', 'D8b')]

DATASETS_TO_TEST = [INPUT_FILES[2]]

# Scale options

MAXPOLARITY = 100  # Sets the polarity scale (from -MAXPOLARITY to +MAXPOLARITY)

# Summary characteristics

LIM_SENTENCES = 30  # Sets the maximum number of SENTENCES in each side of the summary
LIM_WORDS = 100  # Sets the maximum number of WORDS in each side of the summary


# Get full path for the file with data of target 
def filepath(target):
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
