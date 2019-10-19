# Polarity representation
MAXPOLARITY = 100  # Sets the polarity scale (from -MAXPOLARITY to +MAXPOLARITY)


# Method options
METHOD = ['contrastive', 'noncontrastive'][1]
OPTM_MODE = 'greedy'
MIN_INTENSITY_IN_SUMMARY = 1 * MAXPOLARITY  # If (the absolute value of) the intensity of a sentence is lower than that, that sentence will not be in the summary.
ALPHA = 20

# Summary characteristics

LIM_WORDS = 100  # Sets the maximum number of words in each side of the summary
LIM_SENTENCES = 20  # Sets the maximum number of sentences in each side of the summary


# Evaluation options

REPEAT_TESTS = 10  # Times to repeat each test
DISCARD_TESTS = int(0.1 * REPEAT_TESTS)  # Amount of top-rated and bottom-rated tests to be discarded to compute average


# Display options

VERBOSE_MODE = True  # To print statistics and status information (progress is always shown)
DEBUG_MODE = True


# Input files settings

DATA_DIR = "../input"

INPUT_FILES = [(), ('D1a', 'D1b'), ('D2a', 'D2b'), ('D3a', 'D3b'), ('D4a', 'D4b'), ('D5a', 'D5b'), ('D6a', 'D6b'), ('D7a', 'D7b'), ('D8a', 'D8b')]

DATASETS_TO_TEST = INPUT_FILES[2:4]

def filepath(target):  # Get full path for the file with data of target
    return DATA_DIR + '/' + target + '.json'


# Optimization options

GREEDY_CANDS_SELECTED = 1
# In the greedy optimization, `GREEDY_CANDS_SELECTED` will be selected for the next step.
# For example, if GREEDY_CANDS_SELECTED = 5 and there are 500 candidates for the best summary of length 3, then the 5 best summaries of length 3 will be tried to see which one forms the best summary of length 4.
# Lower values are faster, higher values give better result.
# Use GREEDY_CANDS_SELECTED = 1 for a purely greedy algorithm. (will keep only one best candidate at a time)


if VERBOSE_MODE:
    import output_format as out

    out.printMessage('Datasets: ', DATASETS_TO_TEST)
    out.printMessage()
    out.printMessage('Method: ', METHOD)
    out.printMessage('Limit of sentences (per side): ', LIM_SENTENCES)
    out.printMessage('Limit of words (per side): ', LIM_WORDS)
    out.printMessage()
    out.printMessage('Low sentiment: ', MIN_INTENSITY_IN_SUMMARY)
    out.printMessage('alpha: ', ALPHA)
    out.printMessage('Candidates selected: ', GREEDY_CANDS_SELECTED)
    out.printMessage()
    out.printMessage()

import output_format as out

if DEBUG_MODE:
    out.setDebugPrints(True)  # Choose whether or not to display information for debugging.