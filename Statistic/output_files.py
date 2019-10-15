import json

from setup import DISCARD_TESTS, REPEAT_TESTS
from setup import LIM_SENTENCES  # Sets the maximum number of SENTENCES in each side of the summary
from setup import LIM_WORDS  # Sets the maximum number of WORDS in each side of the summary
from setup import MIN_INTENSITY_IN_SUMMARY  # Sets the minimum intensity that a sentence in the summary has to have
from structure import word_count

json_results = {}


def reset():
    global json_results
    json_results = {'meta': {}}
    json_results['meta']['source'] = []
    json_results['meta']['limits (per side)'] = {}
    json_results['meta']['limits (per side)']['sentences'] = LIM_SENTENCES
    json_results['meta']['limits (per side)']['words'] = LIM_WORDS
    json_results['meta']['method_options'] = {}
    json_results['meta']['method_options']['minimum intensity'] = MIN_INTENSITY_IN_SUMMARY
    json_results['output'] = []


def new_source(SOURCE1_NAME, SOURCE2_NAME, source1, source2):
    reset()
    json_results['meta']['source'] = (SOURCE1_NAME, SOURCE2_NAME)
    json_results['meta']['size'] = {}
    json_results['meta']['size']['source'] = {}
    json_results['meta']['size']['source']['sentences'] = []
    json_results['meta']['size']['source']['sentences'].append(len(source1))
    json_results['meta']['size']['source']['sentences'].append(len(source2))
    json_results['meta']['size']['source']['words'] = []
    json_results['meta']['size']['source']['words'].append(word_count(source1))
    json_results['meta']['size']['source']['words'].append(word_count(source2))


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
    json_results['output'].append(n)


def overall_scores(e, time_total, all_summaries):
    global json_results
    json_results['meta']['run time'] = round(time_total, 2)
    json_results['meta']['different summaries generated'] = len(all_summaries)
    json_results['evaluation'] = e


def make_table_of_results():

    means = json_results['evaluation']['means']
    stdevs = json_results['evaluation']['stdevs']
    scores = json_results['evaluation']['scores']
    sizes = json_results['evaluation']['avg_sizes']

    table_results = '\n\nSCORES'
    table_results += '\n\n'
    table_results += '                R     C     D   harm mean '
    table_results += '\n\n'
    table_results += 'mean          %3.0lf   %3.0lf   %3.0lf   [ %3.0lf ]' % (means['R'], means['C'], means['D'], means['H'])
    table_results += '\n\n'
    table_results += 'stdevs       ~%3.0lf  ~%3.0lf  ~%3.0lf    ~%3.0lf' % (stdevs['R'], stdevs['C'], stdevs['D'], stdevs['H'])
    table_results += '\n\n\n'
    table_results += 'max           %3.0lf   %3.0lf   %3.0lf     %3.0lf' % ((max(scores['R'])), (max(scores['C'])), (max(scores['D'])), (max(scores['H'])))
    table_results += '\n\n'
    table_results += 'min           %3.0lf   %3.0lf   %3.0lf     %3.0lf' % ((min(scores['R'])), (min(scores['C'])), (min(scores['D'])), (min(scores['H'])))
    table_results += '\n\n\n'

    table_results += '\n\n'
    table_results += ' avg words 1:  %6.2lf ' % (sizes['words_1'])
    table_results += '\n'
    table_results += ' avg words 2:  %6.2lf ' % (sizes['words_2'])
    table_results += '\n\n'
    table_results += ' avg sentences 1:  %6.2lf ' % (sizes['sentences_1'])
    table_results += '\n'
    table_results += ' avg sentences 2:  %6.2lf ' % (sizes['sentences_2'])
    table_results += '\n\n'
    table_results += ' time %6.2lf ' % (json_results['meta']['run time'])
    table_results += '\n'
    table_results += ' diff summs: %d' % (json_results['meta']['different summaries generated'])
    table_results += '\n\n'

    return table_results


def write_files(SOURCE1, SOURCE2, exec_code):
    json_results_filename = 'RESULTS/' + exec_code + '_' + SOURCE1 + '_' + SOURCE2 + '.json'
    f = open(json_results_filename, 'w')
    f.write(json.dumps(json_results, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False))
    f.close()

    table_results = make_table_of_results()
    table_results_filename = 'RESULTS/' + exec_code + '_' + 'table' + '.txt'  # Name of file that will save the results
    f = open(table_results_filename, 'a')
    f.write('%d tests, discard %d(x2) best and worst\n\n' % (REPEAT_TESTS, DISCARD_TESTS))
    f.write('\n\n')
    f.write('============  %s %s ============' % (SOURCE1, SOURCE2))
    f.write('\n\n')
    f.write(table_results)
    f.write('\n\n\n\n\n\n')
    f.close()
