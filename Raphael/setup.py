DEBUGGING = False

# Execution options
# METHOD = ['CONTRASTIVE', 'NONCONTRASTIVE'][0]

OPTM_MODE = 'selection'
# OPTM_MODE = 'random'
# OPTM_MODE = 'alternate'

# INDEPENDENT_RANK = True
INDEPENDENT_RANK = False

# SENTENCE_IDEAL_LENGTH = 5
SENTENCE_IDEAL_LENGTH = 0

# Display options

VERBOSE_MODE = False  # To print statistics and status information (progress is always shown)
EVALUATION_MODE = True  # To print evaluation metrics results
OUTPUT_MODE = False  # To print the summaries
OVERVIEW_MODE = False

METHOD = [OPTM_MODE, INDEPENDENT_RANK, SENTENCE_IDEAL_LENGTH]

# Input files 

DATA_DIR = "../input"

SOURCE1, SOURCE2 = \
    [(), ('10', '11'), ('30', '31'), ('10-sel', '11-sel'), ('10-chop', '11'), ('30a', '31a'), ('30b', '31b'),
     ('30f', '31f')][1]

# SOURCE1 = '10'
# SOURCE2 = '11'


# Scale options

MAXPOLARITY = 100  # Sets the polarity scale (from -MAXPOLARITY to +MAXPOLARITY)

# Summary characteristics

LIM_SENTENCES = 20  # Sets the maximum number of SENTENCES in each side of the summary
LIM_WORDS = 150  # Sets the maximum number of WORDS in each side of the summary

MIN_INTENS_IN_SUMMARY = 1 * MAXPOLARITY  # If (the absolute value of) a sentence is lower than that, that sentence will not be in the summary.

# Method parameters

ALPHA = 20

preset = [0, 1, 2][2]

PRESET = [
    {
        'KEY_MEASURE': 'aspects',
        'setting': 0},
    {
        'KEY_MEASURE': 'aspects',
        'setting': 1},
    {
        'KEY_MEASURE': 'corpus',
        'setting': 1}
]

config = PRESET[preset]

# KEY_MEASURE = preset['KEY_MEASURE']

# setting = preset['setting']

# ASPECT_DETECTION =   ['keywords', 'clues'][setting]
# POLARITY_ATTRIBUTION = ['pure', 'complex', 'manual'][setting]

# BYPASS_GENERIC =   [True, False][setting]
# BYPASS_UNRELATAD = [False, True][setting]
# BYPASS_SHORT =     [False, True][setting]


# KEY_MEASURE = 'aspects'
# KEY_MEASURE = 'lexicon'
# KEY_MEASURE = 'corpus'

# def update_settings(preset=preset):

KEY_MEASURE = config['KEY_MEASURE']

setting = config['setting']

ASPECT_DETECTION = ['keywords', 'clues'][setting]
POLARITY_ATTRIBUTION = ['pure', 'complex', 'manual'][setting]

BYPASS_GENERIC = [True, False][setting]
BYPASS_UNRELATAD = [False, True][setting]
BYPASS_SHORT = [False, True][setting]

# BYPASS_GENERIC =   False
# BYPASS_UNRELATAD = False
# BYPASS_SHORT =     False


POLARITY_LEXICON = 'sentilex'

# Optimization options


GREEDY_CANDS_SELECTED = 10  # 5#1#5#0.0002


# In the greedy optimization, [max(1, GREEDY_CANDS_SELECTED * (total number of candidates))] will be selected for the next step.
# For example, if GREEDY_CANDS_SELECTED = 0.001 and there are 10k candidates for the best summary of length 3, then the 0.001*10k = 10 best summaries of length 3 will be tried to see which one forms the best summary of length 4. 
# Must be in the interval [0,1]. Lower values are faster, but higher values give better result. 
# Use GREEDY_CANDS_SELECTED = 0 for a purely greedy algorithm. (will keep only one best candidate at a time)
# Suggestion: GREEDY_CANDS_SELECTED = 0.0005 is a nice setting for datasets of size around 200, where it'll keep the top 10 candidates at each iteration. It is slower than GREEDY_CANDS_SELECTED = 0 but might deliever a better result. 
# GREEDY_CANDS_SELECTED = 1 would run a brute force algorithm (won't discard any candidate) NOTICE: this takes a lot and does lots of unecessary computing; it's better to use the brute force algorithm that is implemented in this project (which, of course, also takes a lot, but doesn't do unecessary computing)


# If true, in the greedy algorithm, chooses all candidates (not just one) with score equal to the best one. MUCH SLOWER! May deliever a better result.


# Get full path for the file with data of target 
def filepath(target):
    return DATA_DIR + '/' + target + '.json'


if VERBOSE_MODE or EVALUATION_MODE:
    import output_format as out

    out.printMessage('Datasets: ', SOURCE1, SOURCE2)
    out.printMessage()
    # out.printMessage('Method: ', OPTM_METHOD, INDEPENDENT_RANK)
    out.printMessage('Limit of words (per side): ', LIM_WORDS)
    out.printMessage()
    out.printMessage('Aspect detection: ', ASPECT_DETECTION)
    out.printMessage('Polarity attribution: ', POLARITY_ATTRIBUTION)
    out.printMessage()
