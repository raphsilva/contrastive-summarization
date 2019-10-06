import json

from setup import LIM_SENTENCES  # Sets the maximum number of SENTENCES in each side of the summary
from setup import LIM_WORDS  # Sets the maximum number of WORDS in each side of the summary
from setup import MIN_INTENSITY_IN_SUMMARY  # Sets the minimum intensity that a sentence in the summary has to have
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


def end_of_process(time_total):
    results['meta']['run time'] = round(time_total, 2)


def write_files(SOURCE1, SOURCE2, exec_code):
    f = open('RESULTS/' + SOURCE1 + '_' + SOURCE2 + '_' + exec_code + '.json', 'w')
    f.write(json.dumps(results, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False))
    f.close()
