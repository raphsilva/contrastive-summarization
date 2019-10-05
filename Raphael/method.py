from probability import *
from setup import KEY_MEASURE
from setup import MAXPOLARITY
from writefiles import get_variable_from_file
from writefiles import underwrite_file


def set_ALPHA(value):
    global ALPHA
    ALPHA = value
    return ALPHA


def divergence_measure(d1, d2):
    return KLdivergence(d1, d2)


def sent(words_polarities):
    a = 0
    b = 0

    for i in words_polarities:
        a += i[1]
        b += abs(i[1])

    sent = MAXPOLARITY * a / (b + ALPHA)
    sent_rounded = float('%.2g' % (sent))  # Rounded to 2 significant digits (to optimize use of cache)

    return sent_rounded


def OLD_mean_summ_sent(S, info):
    r = 0
    for i in S:
        r += sent(info[i]['sentence'])
    r = r / len(S)
    return int(r)


cache_distance = get_variable_from_file('cache/distance.cache')
cache_SAM = get_variable_from_file('cache/SAM.cache')

if cache_distance == False:
    cache_distance = {}

if cache_SAM == False:
    cache_SAM = {}

normal_distribution_zero = normalDistributionZero()

########################################################################


import evaluation as evaluation


def score_repr_summ(source, candidate):
    return evaluation.representativiness(source, candidate, KEYMEASURE=KEY_MEASURE)


def score_comp_summ(source1, source2, candidate1, candidate2):
    r1 = evaluation.representativiness(source1, candidate1, KEYMEASURE=KEY_MEASURE)
    r2 = evaluation.representativiness(source2, candidate2, KEYMEASURE=KEY_MEASURE)
    c = evaluation.contrastiviness(source1, source2, candidate1, candidate2, KEYMEASURE=KEY_MEASURE)
    r = 0.5 * (r1 + r2)
    a = 2 * (c * r) / (c + r)
    return a


def score_representativity(source1, source2, candidate1, candidate2):
    r1 = evaluation.representativiness(source1, candidate1, KEYMEASURE=KEY_MEASURE)
    r2 = evaluation.representativiness(source2, candidate2, KEYMEASURE=KEY_MEASURE)
    return (r1 + r2) / 2


def save_caches():
    underwrite_file('cache/SAM.cache', cache_SAM)
    underwrite_file('cache/distance.cache', cache_distance)
