import output_format
from setup import MAXPOLARITY


def trinary_polarity(num):
    if num < -0.25 * MAXPOLARITY:
        return -1
    if num > 0.25 * MAXPOLARITY:
        return +1
    return 0


cache_get_opinions = {}


def get_opinions(source):
    key_cache = repr(source)
    if key_cache in cache_get_opinions:
        return cache_get_opinions[key_cache]

    r = []
    for j in source:

        for aspect in source[j]['sent']:

            polarity = source[j]['sent'][aspect]
            polarity = trinary_polarity(polarity)

            if polarity == 0:
                continue

            r.append((aspect, polarity))

    cache_get_opinions[key_cache] = r

    return r


def get_contrastive_pairs(opinions_source1, opinions_source2, REPETITION=False):
    r = []

    for op1 in opinions_source1:
        for op2 in opinions_source2:
            pol1 = op1[1]
            pol2 = op2[1]
            if op1[0] == op2[0] and pol1 == -pol2 and pol1 != 0:
                asp_cont = (op1[0], pol1, pol2)  # This aspect has the possibility to form a possible contrastive pair.

                if asp_cont not in r or REPETITION == True:
                    r.append(asp_cont)

    return r


def get_summary_from_indexes(source, indexes):
    return {i: source[i] for i in indexes}


def count_words(summ):
    r = 0
    for i in summ:
        r += summ[i]['word_count']
    return r
