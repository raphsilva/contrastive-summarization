import metrics
from setup import DISCARD_TESTS
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


def overall_samples():

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
        'r': r_scores_without_outliers,
        'c': c_scores_without_outliers,
        'd': d_scores_without_outliers,
        'h': h_scores_without_outliers
    }
    e['means'] = {
        'r': r_mean,
        'c': c_mean,
        'd': d_mean,
        'h': h_mean
    }
    e['stdevs'] = {
        'r': r_stdev,
        'c': c_stdev,
        'd': d_stdev,
        'h': h_stdev
    }
    e['avg_sizes'] = {
        'words_1': avg_words1,
        'words_2': avg_words2,
        'sentences_1': avg_sentences1,
        'sentences_2': avg_sentences2
    }

    return e


def harmonic_mean(l):
    s = 0
    if min(l) == 0:
        return -1
    for i in l:
        s += 1 / i
    m = s / len(l)
    return 1 / m
