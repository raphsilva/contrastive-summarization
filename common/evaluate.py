from statistics import stdev

import common.metrics as metrics
from OPTIONS import DISCARD_TESTS

r_scores = []
c_scores = []
d_scores = []
h_scores = []

qnt_words_1 = []
qnt_words_2 = []
qnt_sentences_1 = []
qnt_sentences_2 = []


def reset():
    global r_scores, c_scores, d_scores, h_scores
    global qnt_words_1, qnt_words_2, qnt_sentences_1, qnt_sentences_2

    r_scores = []
    c_scores = []
    d_scores = []
    h_scores = []
    qnt_words_1 = []
    qnt_words_2 = []
    qnt_sentences_1 = []
    qnt_sentences_2 = []


def new_sample(source1, source2, summ1, summ2):
    global r_scores, c_scores, d_scores, h_scores
    global qnt_words_1, qnt_words_2, qnt_sentences_1, qnt_sentences_2

    r1 = 100 * metrics.representativiness(source1, summ1)
    r2 = 100 * metrics.representativiness(source2, summ2)
    R = (r1 + r2) / 2

    C = 100 * metrics.contrastiviness(source1, source2, summ1, summ2)

    d1 = 100 * metrics.diversity(source1, summ1)
    d2 = 100 * metrics.diversity(source2, summ2)

    D = (d1 + d2) / 2

    H = harmonic_mean([R, C, D])

    w1 = sum([summ1[i]['word_count'] for i in summ1])
    w2 = sum([summ2[i]['word_count'] for i in summ2])

    qnt_words_1.append(w1)
    qnt_words_2.append(w2)
    qnt_sentences_1.append(len(summ1))
    qnt_sentences_2.append(len(summ2))

    r_scores.append(R)
    c_scores.append(C)
    d_scores.append(D)
    h_scores.append(H)

    return {'R': R, 'C': C, 'D': D, 'H': H}


def source():
    r_scores_without_outliers = sorted(r_scores)[DISCARD_TESTS:-DISCARD_TESTS]
    c_scores_without_outliers = sorted(c_scores)[DISCARD_TESTS:-DISCARD_TESTS]
    d_scores_without_outliers = sorted(d_scores)[DISCARD_TESTS:-DISCARD_TESTS]
    h_scores_without_outliers = sorted(h_scores)[DISCARD_TESTS:-DISCARD_TESTS]

    r_mean = sum(r_scores_without_outliers) / len(r_scores_without_outliers)
    c_mean = sum(c_scores_without_outliers) / len(c_scores_without_outliers)
    d_mean = sum(d_scores_without_outliers) / len(d_scores_without_outliers)
    h_mean = harmonic_mean([r_mean, c_mean, d_mean])

    r_stdev = stdev(r_scores_without_outliers)
    c_stdev = stdev(c_scores_without_outliers)
    d_stdev = stdev(d_scores_without_outliers)
    h_stdev = stdev(h_scores_without_outliers)

    avg_words1 = sum(qnt_words_1) / len(qnt_words_1)
    avg_words2 = sum(qnt_words_2) / len(qnt_words_2)
    avg_sentences1 = sum(qnt_sentences_1) / len(qnt_sentences_1)
    avg_sentences2 = sum(qnt_sentences_2) / len(qnt_sentences_2)

    e = {}
    e['scores'] = {
        'R': r_scores,
        'C': c_scores,
        'D': d_scores,
        'H': h_scores
    }
    e['means'] = {
        'R': r_mean,
        'C': c_mean,
        'D': d_mean,
        'H': h_mean
    }
    e['stdevs'] = {
        'R': r_stdev,
        'C': c_stdev,
        'D': d_stdev,
        'H': h_stdev
    }
    e['avg_sizes'] = {
        'words_1': avg_words1,
        'words_2': avg_words2,
        'sentences_1': avg_sentences1,
        'sentences_2': avg_sentences2
    }

    print('\n     %5d %5d %5d %5d\n\n' % (r_mean, c_mean, d_mean, h_mean))

    return e


def harmonic_mean(l):
    s = 0
    if min(l) == 0:
        return -1
    for i in l:
        s += 1 / i
    m = s / len(l)
    return 1 / m
