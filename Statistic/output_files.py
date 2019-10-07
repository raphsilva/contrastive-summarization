import json

from setup import LIM_SENTENCES  # Sets the maximum number of SENTENCES in each side of the summary
from setup import LIM_WORDS  # Sets the maximum number of WORDS in each side of the summary
from setup import MIN_INTENSITY_IN_SUMMARY  # Sets the minimum intensity that a sentence in the summary has to have
from setup import DISCARD_TESTS, REPEAT_TESTS
from structure import word_count

results = {}


def reset():
    global results
    results = {'meta': {}}
    results['meta']['source'] = []
    results['meta']['limits (per side)'] = {}
    results['meta']['limits (per side)']['sentences'] = LIM_SENTENCES
    results['meta']['limits (per side)']['words'] = LIM_WORDS
    results['meta']['method_options'] = {}
    results['meta']['method_options']['minimum intensity'] = MIN_INTENSITY_IN_SUMMARY
    results['output'] = []


def new_source(SOURCE1_NAME, SOURCE2_NAME, source1, source2):
    reset()
    results['meta']['source'] = (SOURCE1_NAME, SOURCE2_NAME)
    results['meta']['size'] = {}
    results['meta']['size']['source'] = {}
    results['meta']['size']['source']['sentences'] = []
    results['meta']['size']['source']['sentences'].append(len(source1))
    results['meta']['size']['source']['sentences'].append(len(source2))
    results['meta']['size']['source']['words'] = []
    results['meta']['size']['source']['words'].append(word_count(source1))
    results['meta']['size']['source']['words'].append(word_count(source2))


def new_summary(summ1, summ2, evals, summary_parameters):
    n = {}
    n['parameters'] = summary_parameters
    n['evaluation'] = {}
    n['evaluation']['R'] = evals['R']
    n['evaluation']['C'] = evals['C']
    n['evaluation']['D'] = evals['D']
    n['evaluation']['H'] = evals['H']
    n['summ'] = []
    n['summ'].append([i for i in summ1])
    n['summ'].append([i for i in summ2])
    n['size'] = {}
    n['size']['word count'] = []
    n['size']['word count'].append(word_count(summ1))
    n['size']['word count'].append(word_count(summ2))
    results['output'].append(n)


def overall_scores(e, time_total, all_summaries, exec_code, SOURCE1, SOURCE2):
    TABLE_RESULTS_FILENAME = 'RESULTS/table_results_' + exec_code + '.txt'  # Name of file that will save the results

    means = e['means']
    stdevs = e['stdevs']
    scores = e['scores']
    sizes = e['avg_sizes']

    results_msg = 'SCORES'
    results_msg += '\n\n'
    results_msg += '                R     C     D   harm mean '
    results_msg += '\n\n'
    results_msg += 'mean          %3.0lf   %3.0lf   %3.0lf   [ %3.0lf ]' % (means['R'], means['C'], means['D'], means['H'])
    results_msg += '\n\n'
    results_msg += 'stdevs       ~%3.0lf  ~%3.0lf  ~%3.0lf    ~%3.0lf' % (stdevs['R'], stdevs['C'], stdevs['D'], stdevs['H'])
    results_msg += '\n\n\n'
    results_msg += 'max           %3.0lf   %3.0lf   %3.0lf     %3.0lf' % ((max(scores['R'])), (max(scores['C'])), (max(scores['D'])), (max(scores['H'])))
    results_msg += '\n\n'
    results_msg += 'min           %3.0lf   %3.0lf   %3.0lf     %3.0lf' % ((min(scores['R'])), (min(scores['C'])), (min(scores['D'])), (min(scores['H'])))
    results_msg += '\n\n\n'

    results_msg += '\n\n'
    results_msg += ' avg words 1:  %6.2lf ' % (sizes['words_1'])
    results_msg += '\n'
    results_msg += ' avg words 2:  %6.2lf ' % (sizes['words_2'])
    results_msg += '\n\n'
    results_msg += ' avg sentences 1:  %6.2lf ' % (sizes['sentences_1'])
    results_msg += '\n'
    results_msg += ' avg sentences 2:  %6.2lf ' % (sizes['sentences_2'])
    results_msg += '\n\n'
    results_msg += ' time %6.2lf ' % (time_total)
    results_msg += '\n'
    results_msg += ' diff summs: %d' % (len(all_summaries))
    results_msg += '\n\n'

    print(results_msg)

    f = open(TABLE_RESULTS_FILENAME, 'a')
    f.write('%d tests, discard %d(x2) best and worst\n\n' % (REPEAT_TESTS, DISCARD_TESTS))
    f.write('\n\n')
    f.write('============  %s %s ============' % (SOURCE1, SOURCE2))
    f.write('\n\n')
    f.write(results_msg)
    f.write('\n\n\n\n\n\n')
    f.close()

    results['meta']['run time'] = round(time_total, 2)

    results['evaluation'] = e



def write_files(SOURCE1, SOURCE2, exec_code):
    f = open('RESULTS/' + SOURCE1 + '_' + SOURCE2 + '_' + exec_code + '.json', 'w')
    f.write(json.dumps(results, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False))
    f.close()
