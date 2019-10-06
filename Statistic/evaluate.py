import metrics
from setup import DISCARD_TESTS, REPEAT_TESTS
from statistics import stdev


r_scores = []
c_scores = []
d_scores = []
h_scores = []

qnt_words_1 = []
qnt_words_2 = []
qnt_sentences_1 = []
qnt_sentences_2 = []


def reset():
    global r_scores, c_scores, d_scores, h_scores, qnt_words_1, qnt_words_2, qnt_sentences_1, qnt_sentences_2
    r_scores = []
    c_scores = []
    d_scores = []
    h_scores = []
    qnt_words_1 = []
    qnt_words_2 = []
    qnt_sentences_1 = []
    qnt_sentences_2 = []


def new_sample(source1, source2, summ1, summ2):
    global r_scores, c_scores, d_scores, h_scores, qnt_words_1, qnt_words_2, qnt_sentences_1, qnt_sentences_2
    scores = {}

    scores['r1'] = 100 * metrics.representativiness(source1, summ1)
    scores['r2'] = 100 * metrics.representativiness(source2, summ2)
    scores['R'] = (scores['r1'] + scores['r2']) / 2

    scores['C'] = 100 * metrics.contrastiviness(source1, source2, summ1, summ2)

    scores['d1'] = 100 * metrics.diversity(source1, summ1)
    scores['d2'] = 100 * metrics.diversity(source2, summ2)

    scores['D'] = (scores['d1'] + scores['d2']) / 2

    scores['H'] = harmonic_mean([scores['R'], scores['C'], scores['D']])

    w1 = sum([summ1[i]['word_count'] for i in summ1])
    w2 = sum([summ2[i]['word_count'] for i in summ2])

    qnt_words_1.append(w1)
    qnt_words_2.append(w2)
    qnt_sentences_1.append(len(summ1))
    qnt_sentences_2.append(len(summ2))

    r_scores.append(scores['R'])
    c_scores.append(scores['C'])
    d_scores.append(scores['D'])
    h_scores.append(scores['H'])

    return scores


def overall_samples(SOURCE1, SOURCE2, exec_code, time_total, all_summaries):
    
    TABLE_RESULTS_FILENAME = 'RESULTS/table_results_' + exec_code + '.txt'  # Name of file that will save the results

    r_scores_without_outliers = sorted(r_scores)[DISCARD_TESTS:-DISCARD_TESTS]
    c_scores_without_outliers = sorted(c_scores)[DISCARD_TESTS:-DISCARD_TESTS]
    d_scores_without_outliers = sorted(d_scores)[DISCARD_TESTS:-DISCARD_TESTS]
    h_scores_without_outliers = sorted(h_scores)[DISCARD_TESTS:-DISCARD_TESTS]

    r_stdev = stdev(r_scores_without_outliers)
    c_stdev = stdev(c_scores_without_outliers)
    d_stdev = stdev(d_scores_without_outliers)
    h_stdev = stdev(h_scores_without_outliers)

    r_mean = sum(r_scores_without_outliers) / len(r_scores_without_outliers)
    c_mean = sum(c_scores_without_outliers) / len(c_scores_without_outliers)
    d_mean = sum(d_scores_without_outliers) / len(d_scores_without_outliers)
    h_mean = harmonic_mean([r_mean, c_mean, d_mean])

    results_msg = 'SCORES'
    results_msg += '\n\n'
    results_msg += '                R     C     D   harm mean '
    results_msg += '\n\n'
    results_msg += 'mean          %3.0lf   %3.0lf   %3.0lf   [ %3.0lf ]' % (r_mean, c_mean, d_mean, h_mean)
    results_msg += '\n\n'
    results_msg += 'stdevs       ~%3.0lf  ~%3.0lf  ~%3.0lf    ~%3.0lf' % (r_stdev, c_stdev, d_stdev, h_stdev)
    results_msg += '\n\n\n'
    results_msg += 'max           %3.0lf   %3.0lf   %3.0lf     %3.0lf' % ((max(r_scores_without_outliers)), (max(c_scores_without_outliers)), (max(d_scores_without_outliers)), (max(h_scores_without_outliers)))
    results_msg += '\n\n'
    results_msg += 'min           %3.0lf   %3.0lf   %3.0lf     %3.0lf' % ((min(r_scores_without_outliers)), (min(c_scores_without_outliers)), (min(d_scores_without_outliers)), (min(h_scores_without_outliers)))
    results_msg += '\n\n\n'

    avg_words1 = sum(qnt_words_1) / len(qnt_words_1)
    avg_words2 = sum(qnt_words_2) / len(qnt_words_2)
    avg_sentences1 = sum(qnt_sentences_1) / len(qnt_sentences_1)
    avg_sentences2 = sum(qnt_sentences_2) / len(qnt_sentences_2)

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

    return [r_mean, c_mean, d_mean]


def harmonic_mean(l):
    s = 0
    if min(l) == 0:
        return -1
    for i in l:
        s += 1 / i
    m = s / len(l)
    return 1 / m
