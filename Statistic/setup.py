# Execution options
METHOD = ['contrastive', 'noncontrastive'][1]

OPTM_MODE = 'greedy'

REPEAT_TESTS = 10  # Times to repeat each test
DISCARD_TESTS = int(0.1 * REPEAT_TESTS)  # Amount of top-rated and bottom-rated tests to be discarded to compute average

# Display options

VERBOSE_MODE = True  # To print statistics and status information (progress is always shown)
DEBUG_MODE = True

# Input files

DATA_DIR = "../input"

INPUT_FILES = [(), ('D1a', 'D1b'), ('D2a', 'D2b'), ('D3a', 'D3b'), ('D4a', 'D4b'), ('D5a', 'D5b'), ('D6a', 'D6b'), ('D7a', 'D7b'), ('D8a', 'D8b')]

DATASETS_TO_TEST = INPUT_FILES[2:4]

# Scale options

MAXPOLARITY = 100  # Sets the polarity scale (from -MAXPOLARITY to +MAXPOLARITY)

# Summary characteristics

LIM_SENTENCES = 20  # Sets the maximum number of SENTENCES in each side of the summary
LIM_WORDS = 100  # Sets the maximum number of WORDS in each side of the summary

MIN_INTENSITY_IN_SUMMARY = 1 * MAXPOLARITY  # If (the absolute value of) the intensity of a sentence is lower than that, that sentence will not be in the summary.

# Method parameters

ALPHA = 20

# Optimization options


GREEDY_CANDS_SELECTED = 1  # 5#1#5#0.0002


# In the greedy optimization, [max(1, GREEDY_CANDS_SELECTED * (total number of candidates))] will be selected for the next step.
# For example, if GREEDY_CANDS_SELECTED = 0.001 and there are 10k candidates for the best summary of length 3, then the 0.001*10k = 10 best summaries of length 3 will be tried to see which one forms the best summary of length 4. 
# Must be in the interval [0,1]. Lower values are faster, but higher values give better result. 
# Use GREEDY_CANDS_SELECTED = 0 for a purely greedy algorithm. (will keep only one best candidate at a time)
# Suggestion: GREEDY_CANDS_SELECTED = 0.0005 is a nice setting for datasets of size around 200, where it'll keep the top 10 candidates at each iteration. It is slower than GREEDY_CANDS_SELECTED = 0 but might deliever a better result. 
# GREEDY_CANDS_SELECTED = 1 would run a brute force algorithm (won't discard any candidate) NOTICE: this takes a lot and does lots of unecessary computing; it's better to use the brute force algorithm that is implemented in this project (which, of course, also takes a lot, but doesn't do unecessary computing)


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
    out.printMessage('Low sentiment: ', MIN_INTENSITY_IN_SUMMARY)
    out.printMessage('alpha: ', ALPHA)
    out.printMessage('Candidates selected: ', GREEDY_CANDS_SELECTED)
    out.printMessage()
    out.printMessage()