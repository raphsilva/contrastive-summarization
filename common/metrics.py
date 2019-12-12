MAXSENT = 100

from common.structure import get_contrastive_pairs
from common.structure import get_opinions as structure_get_opinions


def get_opinions(info):
    opinions = structure_get_opinions(info)
    return [i for i in opinions if i[0]]


def representativiness(source, summ):
    points = 0

    opinions_source = get_opinions(source)
    opinions_summ = get_opinions(summ)

    c_source = {i: 0 for i in opinions_source}

    for i in opinions_source:
        c_source[i] += 1 / len(opinions_source)

    counted = []
    for i in opinions_summ:
        if i in counted:
            continue
        points += c_source[i]
        counted.append(i)

    return points


cache_contrastiviness = {}


def contrastiviness(source1, source2, summ1, summ2):
    opinions_source1 = get_opinions(source1)
    opinions_source2 = get_opinions(source2)

    opinions_summ1 = get_opinions(summ1)
    opinions_summ2 = get_opinions(summ2)

    key_cache = repr(opinions_source1) + repr(opinions_source2) + repr(summ1) + repr(summ2)
    if key_cache in cache_contrastiviness:
        return cache_contrastiviness[key_cache]

    points = 0

    # Compares source 1 with summ 2 and vice-versa.
    for opinions_source, opinions_opposite_source, opinions_summ, opinions_opposite_summ in zip([opinions_source1, opinions_source2], [opinions_source2, opinions_source1], [opinions_summ1, opinions_summ2], [opinions_summ2, opinions_summ1]):

        contrastive_pairs = get_contrastive_pairs(opinions_source, opinions_opposite_source)

        c = 0
        for p in contrastive_pairs:
            if (p[0], p[1]) in opinions_summ:
                c += .5

            if (p[0], p[2]) in opinions_opposite_summ:
                c += .5

        points += c / len(contrastive_pairs)

    r = points / 2

    cache_contrastiviness[key_cache] = r

    return r


def diversity(source, summ):
    opinions_source = get_opinions(source)
    opinions_summ = get_opinions(summ)

    opinions_source = list(set(opinions_source))  # Remove duplicates
    opinions_summ = list(set(opinions_summ))

    return len(opinions_summ) / len(opinions_source)
