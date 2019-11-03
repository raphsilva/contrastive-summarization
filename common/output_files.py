import json

from options import DISCARD_TESTS, REPEAT_TESTS
from options import LIM_SENTENCES  # Sets the maximum number of SENTENCES in each side of the summary
from options import LIM_WORDS  # Sets the maximum number of WORDS in each side of the summary
from options import options
from structure import word_count

json_results = {}
summary = ''


def reset():
    global json_results
    json_results = {'meta': {}}
    json_results['meta']['source'] = []
    json_results['meta']['limits (per side)'] = {}
    json_results['meta']['limits (per side)']['sentences'] = LIM_SENTENCES
    json_results['meta']['limits (per side)']['words'] = LIM_WORDS
    json_results['meta']['method_parameters'] = options
    json_results['output'] = []


def new_source(SOURCE1_NAME, SOURCE2_NAME, source1, source2, method):
    reset()
    json_results['meta']['source'] = (SOURCE1_NAME, SOURCE2_NAME)
    json_results['meta']['method'] = method
    json_results['meta']['size'] = {}
    json_results['meta']['size']['source'] = {}
    json_results['meta']['size']['source']['sentences'] = []
    json_results['meta']['size']['source']['sentences'].append(len(source1))
    json_results['meta']['size']['source']['sentences'].append(len(source2))
    json_results['meta']['size']['source']['words'] = []
    json_results['meta']['size']['source']['words'].append(word_count(source1))
    json_results['meta']['size']['source']['words'].append(word_count(source2))


def new_summary(summ1, summ2, evals, summary_parameters, time_elapsed):
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
    n['time'] = time_elapsed
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


def write_summary(summ1, summ2, num_summaries):
    global summary

    summary = '\n'
    for i in summ1:
        summary += "%s " % (summ1[i]['verbatim'])
        summary += "\n"

    summary += '\n\n'

    for i in summ2:
        summary += "%s " % (summ2[i]['verbatim'])
        summary += "\n"

    w1 = sum([summ1[i]['word_count'] for i in summ1])
    w2 = sum([summ2[i]['word_count'] for i in summ2])

    summary += '\n\n\n'

    summary += '          sentences:   %3d  %3d\n' % (len(summ1), len(summ2))
    summary += '              words:   %3d  %3d\n' % (w1, w2)


def print_stats(summ_idx_1, summ_idx_2, source1, source2):
    import output_format as out
    import structure as struct
    # Get statistics about aspects in the source (mean, standard deviation, probability)
    stats_source_1 = struct.aspects_stats(source1)
    stats_source_2 = struct.aspects_stats(source2)
    out.printMessage('\nOverview of opinions in the source for each entity:')
    struct.printOverview(stats_source_1)
    struct.printOverview(stats_source_2)
    summ1 = {i: source1[i] for i in summ_idx_1}
    summ2 = {i: source2[i] for i in summ_idx_2}
    out.printMessage('\nOverview of opinions in the summary for each entity:')
    sum_stats_1 = struct.aspects_stats(summ1)
    sum_stats_2 = struct.aspects_stats(summ2)
    struct.printOverview(sum_stats_1)
    struct.printOverview(sum_stats_2)
    out.printMessage('\nOpinions in the summary for each entity:')
    for i in summ_idx_1:
        out.printinfo("      %4d)   %s " % (i, source1[i]['opinions']))
    print()
    for i in summ_idx_2:
        out.printinfo("      %4d)   %s " % (i, source2[i]['opinions']))



def write_files(SOURCE1, SOURCE2, exec_code):
    json_results_filename = 'RESULTS/' + exec_code + '_' + SOURCE1 + '_' + SOURCE2 + '.json'
    f = open(json_results_filename, 'w')
    f.write(json.dumps(json_results, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False))
    f.close()

    f = open(f'OUTPUT/out_{exec_code}_{SOURCE1[:-1]}.txt', 'w')
    f.write(summary)
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
