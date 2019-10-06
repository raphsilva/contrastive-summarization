import metrics
from setup import DISCARD_TESTS, REPEAT_TESTS

hr = []
hc = []
hd = []
hh = []

h_words1 = []
h_words2 = []
h_sentences1 = []
h_sentences2 = []


def reset():
    global hr, hc, hd, hh, h_words1, h_words2, h_sentences1, h_sentences2
    hr = []
    hc = []
    hd = []
    hh = []

    h_words1 = []
    h_words2 = []
    h_sentences1 = []
    h_sentences2 = []


def new_sample(source1, source2, summ1, summ2):
    global hr, hc, hd, hh, h_words1, h_words2, h_sentences1, h_sentences2
    evals = {}

    evals['r1'] = 100 * metrics.representativiness(source1, summ1)
    evals['r2'] = 100 * metrics.representativiness(source2, summ2)
    evals['R'] = (evals['r1'] + evals['r2']) / 2

    evals['C'] = 100 * metrics.contrastiviness(source1, source2, summ1, summ2)

    evals['d1'] = 100 * metrics.diversity(source1, summ1)
    evals['d2'] = 100 * metrics.diversity(source2, summ2)

    evals['D'] = (evals['d1'] + evals['d2']) / 2

    evals['H'] = harmonic_mean([evals['R'], evals['C'], evals['D']])

    w1 = sum([summ1[i]['word_count'] for i in summ1])
    w2 = sum([summ2[i]['word_count'] for i in summ2])

    h_words1.append(w1)
    h_words2.append(w2)
    h_sentences1.append(len(summ1))
    h_sentences2.append(len(summ2))

    hr.append(evals['R'])
    hc.append(evals['C'])
    hd.append(evals['D'])
    hh.append(evals['H'])

    return evals


def overall_samples(SOURCE1, SOURCE2, exec_code, time_total, all_summaries):
    from statistics import stdev

    TABLE_RESULTS_FILENAME = 'RESULTS/table_results_' + exec_code + '.txt'  # Name of file that will save the results

    hr_medians = sorted(hr)[DISCARD_TESTS:-DISCARD_TESTS]
    hc_medians = sorted(hc)[DISCARD_TESTS:-DISCARD_TESTS]
    hd_medians = sorted(hd)[DISCARD_TESTS:-DISCARD_TESTS]
    hh_medians = sorted(hh)[DISCARD_TESTS:-DISCARD_TESTS]

    sthh = stdev(hh_medians)
    sthc = stdev(hc_medians)
    sthr = stdev(hr_medians)
    sthd = stdev(hd_medians)

    r = sum(hr) / len(hr)
    c = sum(hc) / len(hc)
    d = sum(hd) / len(hd)
    h = harmonic_mean([r, c, d])

    r_median_mean = sum(hr_medians) / len(hr_medians)
    c_median_mean = sum(hc_medians) / len(hc_medians)
    d_median_mean = sum(hd_medians) / len(hd_medians)
    h_median_mean = harmonic_mean([r, c, d])

    ht = sum(hh) / len(hh)

    results_msg = 'SCORES'
    results_msg += '\n\n'
    results_msg += '                R     C     D   harm mean '
    results_msg += '\n\n'
    results_msg += 'mean          %3.0lf   %3.0lf   %3.0lf   [ %3.0lf ]' % (r_median_mean, c_median_mean, d_median_mean, h_median_mean)
    results_msg += '\n\n'
    results_msg += 'stdevs       ~%3.0lf  ~%3.0lf  ~%3.0lf    ~%3.0lf' % (sthr, sthc, sthd, sthh)
    results_msg += '\n\n\n'
    results_msg += 'max           %3.0lf   %3.0lf   %3.0lf     %3.0lf' % ((max(hr_medians)), (max(hc_medians)), (max(hd_medians)), (max(hh_medians)))
    results_msg += '\n\n'
    results_msg += 'min           %3.0lf   %3.0lf   %3.0lf     %3.0lf' % ((min(hr_medians)), (min(hc_medians)), (min(hd_medians)), (min(hh_medians)))
    results_msg += '\n\n\n'

    avg_words1 = sum(h_words1) / len(h_words1)
    avg_words2 = sum(h_words2) / len(h_words2)
    avg_sentences1 = sum(h_sentences1) / len(h_sentences1)
    avg_sentences2 = sum(h_sentences2) / len(h_sentences2)

    results_msg += '\n\n'
    results_msg += ' avg words 1:  %6.2lf ' % (avg_words1)
    results_msg += '\n'
    results_msg += ' avg words 2:  %6.2lf ' % (avg_words2)
    results_msg += '\n\n'
    results_msg += ' avg sentences 1:  %6.2lf ' % (avg_sentences1)
    results_msg += '\n'
    results_msg += ' avg sentences 2:  %6.2lf ' % (avg_sentences2)
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

    return [r_median_mean, c_median_mean, d_median_mean]


def harmonic_mean(l):
    s = 0
    if min(l) == 0:
        return -1
    for i in l:
        s += 1 / i
    m = s / len(l)
    return 1 / m
