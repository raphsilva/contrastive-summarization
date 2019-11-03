from probability import *
from options import POLARITY_SCALE
from write_files import get_variable_from_file
from write_files import overwrite_json

from options import options

MIN_INTENSITY_IN_SUMMARY = options['Statistic']['min intensity']
ALPHA = options['Statistic']['alpha']

cache_distance = get_variable_from_file('cache/distance.cache')
cache_SAM = get_variable_from_file('cache/SAM.cache')

if cache_distance == False:
    cache_distance = {}

if cache_SAM == False:
    cache_SAM = {}

normal_distribution_zero = normalDistributionZero()


def divergence_measure(d1, d2):
    return KLdivergence(d1, d2)


def remove_low_intensity(source):
    # Remove sentences with low intensity.
    # Will bypass any sentence which the intensity is lower than MIN_INTENS_IN_SUMMARY.
    for i in dict(source):
        if source[i]['intensity'] < MIN_INTENSITY_IN_SUMMARY:
            del source[i]
    return source


def sent(words_polarities):
    a = 0
    b = 0

    for i in words_polarities:
        a += i[1]
        b += abs(i[1])

    sent = POLARITY_SCALE * a / (b + ALPHA)
    sent_rounded = float('%.2g' % (sent))  # Rounded to 2 significant digits (to optimize use of cache)

    return sent_rounded


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
