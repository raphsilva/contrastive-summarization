from probability import *

import re
import string

from setup import ALPHA
from probability import *
from setup import MAXPOLARITY
from setup import POLARITY_ATTRIBUTION
from writefiles import get_variable_from_file
from writefiles import overwrite_json


# from language import stem
# from language import getSentimentLexicon
# from language import negation_words

# from language import getSentimentLexicon_ontopt
# from language import getSentimentLexicon_sqrt


#
# def set_ALPHA(value):
#     global ALPHA
#     ALPHA = value
#     return ALPHA


def divergence_measure(d1, d2):
    # return integralDivergence(d1, d2)
    # return hellingerDistance(d1, d2)
    return KLdivergence(d1, d2)


def pol_ontopt(term):
    if term in possible_aspects:
        return 0
    if term in sentiment_lexicon_ontopt:
        return sentiment_lexicon_ontopt[term]
    return 0


def pol_sqrt(term):
    if term in possible_aspects:
        return 0
    if term in sentiment_lexicon_sqrt:
        return sentiment_lexicon_sqrt[term]
    return 0


ww = {}


def lex_sent(term):
    term = term.lower()
    term = re.sub('[' + string.punctuation + ']', '', term)  # Remove punctuation
    if POLARITY_ATTRIBUTION == 'complex':
        if term in possible_aspects:
            return 0
    r = 0
    if term in sentiment_lexicon:
        r = sentiment_lexicon[term]

    return MAXPOLARITY * r


def find_polarities(words):
    if POLARITY_ATTRIBUTION != 'complex':

        return [(i, lex_sent(i)) for i in words]

    elif POLARITY_ATTRIBUTION == 'complex':

        neg_pos = []
        if any(i in negation_words for i in words):

            l = []

            for i in range(len(words)):
                if words[i] in negation_words:
                    neg_pos.append(i)

            for i in range(len(words)):
                if i in neg_pos:
                    continue  # won't keep negation words
                if any(i - j <= 3 and i - j > 0 for j in neg_pos):
                    l.append((words[i], -lex_sent(words[i])))
                else:
                    l.append((words[i], lex_sent(words[i])))
        else:
            l = [(i, lex_sent(i)) for i in words]

        return l


# def OLD_lex_sent(term):
#     if term in sentiments.keys():
#         return sentiments[term]
#     return 0
#
#
# def OLD_lex_intens(term):
#     if term in modifiers.keys():
#         return modifiers[term]
#     return 0
#
#
# def OLD_intensity(sentence):
#     r = 0
#     mod = 1
#     for i in sentence:
#         r += abs(lex_sent(i))
#     for i in sentence:
#         if lex_intens(i) != 0:
#             mod *= abs(lex_intens(i))
#     return int(r * mod)
#
#
# def OLD_sum_lex_sent(sentence):
#     r = 0
#     mod = 1
#     for i in sentence:
#         r += lex_sent(i)
#     for i in sentence:
#         if lex_intens(i) != 0:
#             mod *= lex_intens(i)
#     return int(r * mod)


def sent(words_polarities):
    a = 0
    b = 0

    for i in words_polarities:
        a += i[1]
        b += abs(i[1])

    sent = MAXPOLARITY * a / (b + ALPHA)
    sent_rounded = float('%.2g' % (sent))  # Rounded to 2 significant digits (to optimize use of cache)

    return sent_rounded


# def OLD_mean_summ_sent(S, info):
#     r = 0
#     for i in S:
#         r += sent(info[i]['sentence'])
#     r = r / len(S)
#     return int(r)


def mismatch(S, S_rating, info):
    a = S_rating - mean_summ_sent(S, info)
    return a * a / MAXPOLARITY


def SM(source, candidate):
    return mismatch(source, candidate)


cache_distance = get_variable_from_file('cache/distance.cache')
cache_SAM = get_variable_from_file('cache/SAM.cache')

if cache_distance == False:
    cache_distance = {}

if cache_SAM == False:
    cache_SAM = {}

normal_distribution_zero = normalDistributionZero()


def SAM(source, candidate):
    global cache_distance, cache_SAM

    key_SAM = repr(source) + repr(candidate)

    if key_SAM in cache_SAM:
        return cache_SAM[key_SAM]

    score = 0
    debug_score = {}

    for aspect in candidate:

        c_mean = candidate[aspect]['mean']
        c_std = candidate[aspect]['std']
        c_prob = candidate[aspect]['prob']

        if aspect not in source:
            key_distance = repr([0, 0, 0, c_mean, c_std, c_prob])
            if key_distance in cache_distance:  # acess entropy cache
                distance = cache_distance[key_distance]

            else:
                normalSource = normal_distribution_zero
                normalCandid = normalDistribution(c_mean, c_std, c_prob)
                distance = -divergence_measure(normalCandid, normalSource)  # calculate entropy
                cache_distance[key_distance] = distance  # save entropy to cache
            score += distance  # add up entropy to make the score
            debug_score[aspect] = distance

        else:
            s_mean = source[aspect]['mean']
            s_std = source[aspect]['std']
            s_prob = source[aspect]['prob']

            key_distance = repr([s_mean, s_std, s_prob, c_mean, c_std, c_prob])

            if key_distance in cache_distance:  # acess entropy cache
                distance = cache_distance[key_distance]

            else:
                normalSource = normalDistribution(s_mean, s_std, s_prob)
                normalCandid = normalDistribution(c_mean, c_std, c_prob)
                distance = -divergence_measure(normalCandid, normalSource)  # calculate entropy
                cache_distance[key_distance] = distance  # save entropy to cache
            score += distance  # add up entropy to make the score
            debug_score[aspect] = distance


    for aspect in source:
        if aspect not in candidate:

            s_mean = source[aspect]['mean']
            s_std = source[aspect]['std']
            s_prob = source[aspect]['prob']

            key_distance = repr([s_mean, s_std, s_prob, 0, 0, 0])

            if key_distance in cache_distance:
                distance = cache_distance[key_distance]  # acess entropy cache

            else:
                normalSource = normalDistribution(s_mean, s_std, s_prob)
                normalCandid = normal_distribution_zero
                distance = -divergence_measure(normalCandid, normalSource)  # calculate entropy
                cache_distance[key_distance] = distance  # save entropy to cache
            score += distance  # add up entropy to make the score
            debug_score[aspect] = distance

    score = float('%.4g' % (score))

    cache_SAM[key_SAM] = score
    return score


def SAM_contrastive(original_stats_1, original_stats_2, stats_cand_1, stats_cand_2):
    score11 = +SAM(original_stats_1, stats_cand_1)
    score22 = +SAM(original_stats_2, stats_cand_2)
    score12 = -SAM(original_stats_1, stats_cand_2)
    score21 = -SAM(original_stats_2, stats_cand_1)

    score = (
                        score11 + score12 + score21 + score22) / 4  # Using average instead of sum (doesn't affect anything, only makes it prettier)

    score = float('%.4g' % (score))

    return score


def save_caches():
    overwrite_json('cache/SAM.cache', cache_SAM)
    overwrite_json('cache/distance.cache', cache_distance)
