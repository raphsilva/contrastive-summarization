MAXSENT = 100

from similarity import psi, phi

BYPASS_ASPECTS = ['EMPRESA', 'PRODUTO', '_GENERIC', '_NONE', 'x', 'X']


def get_opinions(source):
    r = []
    for j in source:

        for opinion in source[j]['opinions']:

            polarity = trinary_polarity(opinion[1])
            aspect = opinion[0]

            if aspect in BYPASS_ASPECTS:
                continue

            if polarity == 0:
                continue

            r.append((aspect, polarity))

    return r


def representativiness_2(source, summ):
    opinions_source = get_opinions(source)
    opinions_summ = get_opinions(summ)

    c_source = {i: 0 for i in opinions_source}
    c_summ = {i: 0 for i in opinions_source}

    for i in opinions_source:
        c_source[i] += 1 / len(opinions_source)
    for i in opinions_summ:
        c_summ[i] += 1 / len(opinions_summ)

    p = 0
    for i in c_source:
        p += abs(c_summ[i] - c_source[i]) / 2
    print()

    return 1 - p


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


def trinary_polarity(num):
    if num < -25:
        return -1
    if num > 25:
        return +1
    return 0


def diversity(source, summ):
    opinions_source = get_opinions(source)
    opinions_summ = get_opinions(summ)

    opinions_source = list(set(opinions_source))  # Remove duplicates
    opinions_summ = list(set(opinions_summ))

    return len(opinions_summ) / len(opinions_source)


def contrastiviness(source1, source2, summ1, summ2):
    opinions_source1 = get_opinions(source1)
    opinions_source2 = get_opinions(source2)

    opinions_summ1 = get_opinions(summ1)
    opinions_summ2 = get_opinions(summ2)

    points = 0

    for opinions_source, opinions_opposite_source, opinions_summ, opinions_opposite_summ in zip(
            [opinions_source1, opinions_source2], [opinions_source2, opinions_source1],
            [opinions_summ1, opinions_summ2], [opinions_summ2, opinions_summ1]):

        all_possibles = []

        for op1 in opinions_source:
            for op2 in opinions_opposite_source:
                pol1 = (op1[1])
                pol2 = (op2[1])
                if op1[0] == op2[0] and pol1 == -pol2 and pol1 != 0:
                    asp_cont = (
                        op1[0], pol1, pol2)  # This aspect has the possibility to form a possible contrastive pair.

                    if asp_cont not in all_possibles:
                        all_possibles.append(asp_cont)

        debug_found_1 = []
        debug_found_2 = []

        c = 0
        for p in all_possibles:
            if (p[0], p[1]) in opinions_summ:
                c += .5

                if (p[0], p[1]) not in debug_found_1:
                    debug_found_1.append((p[0], p[1]))

            if (p[0], p[2]) in opinions_opposite_summ:
                c += .5

                if (p[0], p[2]) not in debug_found_2:
                    debug_found_2.append((p[0], p[2]))

        points += c / len(all_possibles)

    return points / 2


def representativeness_sim(source, summ):
    """
    The representativeness of a contrastive opinion summary S, denoted as r(S), measures how well the summary S represents the opinions expressed by the sentences in both X and Y .
    :return: [float] representativeness of the generated summary.
    """

    source_text_info = [source[s]['text_info'] for s in source]

    summ_text_info = [summ[s]['text_info'] for s in [i for i in summ]]

    score = 0

    for sX in source_text_info:
        best_value = 0
        for u in summ_text_info:
            best_value = max(best_value, phi(sX, u))
        score += best_value

    score /= len(source)

    return score


def contrastiveness_sim(summ1, summ2):
    """
    The contrastiveness of a contrastive opinion summary S, denoted as c(S), measures how well each u matches up with v in the summary.
    :return: [float] contrastiveness of the generated summary.
    """

    sumc = 0

    for u in summ1:

        for v in summ2:

            if summ1[u]['pair'] == summ2[v]['pair']:  # if these are paired

                p = psi(summ1[u]['text_info'], summ2[v]['text_info'])
                sumc += p

    return sumc / len(summ1)


def precision(summ1, summ2):
    """
    The precision of a summary with k contrastive sentence pairs is the percentage of the k pairs that are agreed by a human annotator. If a retrieved pair exists in an evaluator’s paired-cluster source, we assume that the pair is agreed by the annotator (i.e., “relevant”).
    :return: [float] precision of the generated summary.
    """

    c_match = 0

    for u in summ1:
        c1 = [i[0] for i in summ1[u]['opinions']]  # gets aspects

        for v in summ2:
            if summ1[u]['pair'] != summ2[v]['pair']:
                continue

            c2 = [i[0] for i in summ2[v]['opinions']]  # gets aspects

            if any(i in c1 for i in c2):
                c_match += 1

    return c_match / len(summ1)


def aspect_coverage(source, summ):
    """
    The aspect coverage of a summary is the percentage of human-aligned clusters covered in the summary. If a pair of sentences appears in a human-aligned pair of clusters, we would assume that the aligned cluster is covered.
    :return: [float] aspect coverage of the generated summary.
    """

    covered_clusters = []
    all_clusters = []

    # Get all possible clusters (a cluster is identified by the aspect it represents)

    for u in source:
        cs = [i[0] for i in source[u]['opinions']]  # gets aspects
        for c in cs:
            if c not in all_clusters:
                all_clusters.append(c)

    # Get all clusters that were covered in the summary
    for u in summ:

        aspects = [i[0] for i in summ[u]['opinions']]  # gets aspects

        for a in aspects:
            if a not in covered_clusters:
                covered_clusters.append(a)

    return len(covered_clusters) / len(all_clusters)

    return points / len(opinions_source)
