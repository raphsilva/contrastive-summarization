MAXSENT = 100

import structure as struct

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

    return 1 - p  # (p/len(c_source))


def representativiness(source, summ):
    points = 0

    opinions_source = get_opinions(source)
    opinions_summ = get_opinions(summ)

    # pprint(sorted(opinions_source))

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


def BAK_contrastiviness(source1, source2, summ1, summ2):
    opinions_source1 = [item for sublist in [source1[j]['opinions'] for j in source1] for item in sublist]
    opinions_source2 = [item for sublist in [source2[j]['opinions'] for j in source2] for item in sublist]

    opinions_summ1 = [item for sublist in [summ1[j]['opinions'] for j in summ1] for item in sublist]
    opinions_summ2 = [item for sublist in [summ2[j]['opinions'] for j in summ2] for item in sublist]

    points = 0

    # Compares source 1 with summ 2 and vice-versa.
    for opinions_source, opinions_opposite_source, opinions_opposite_summ in zip([opinions_source1, opinions_source2],
                                                                                 [opinions_source2, opinions_source1],
                                                                                 [opinions_summ2, opinions_summ1]):

        max_possible = 0

        for opinions1 in opinions_source:
            for opinions2 in opinions_opposite_source:
                if opinions1[0] == opinions2[0] and opinions1[1] * opinions2[1] < 0:
                    max_possible += 1
                    # break

        p = 0

        for o in opinions_source:
            for u in opinions_opposite_summ:
                if o[0] == u[0] and o[1] * u[1] < 0:
                    p += 1

        points += p / max_possible

    return points / 2


############# IMPLEMENTING ########################


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


############## TEST ################################################33

def representativiness_competitive(source, summ):
    points = 0

    opinions_source = [item for sublist in [source[j]['opinions'] for j in source] for item in sublist]
    opinions_summ = [item for sublist in [summ[j]['opinions'] for j in summ] for item in sublist]

    # pprint(opinions_source)
    # pprint(opinions_summ)

    # print()
    # print()
    # print()

    for o in opinions_source:
        for u in opinions_summ:
            if o[0] == u[0] and o[1] * u[1] >= 0:
                # print(o, u)
                points += 1
            elif o[0] == u[0] and o[1] * u[1] < 0:
                points -= 1

    # print(points)
    # print(points/len(opinions_source))

    return points / len(opinions_source)


def contrastiviness_competitive(source, summ):
    points = 0

    opinions_source = [item for sublist in [source[j]['opinions'] for j in source] for item in sublist]
    opinions_summ = [item for sublist in [summ[j]['opinions'] for j in summ] for item in sublist]

    # pprint(opinions_source)
    # pprint(opinions_summ)

    # print()
    # print()
    # print()

    for o in opinions_source:
        for u in opinions_summ:
            if o[0] == u[0] and o[1] * u[1] <= 0:
                # print(o, u)
                points += 1
            elif o[0] == u[0] and o[1] * u[1] < 0:
                # print(o, u)
                points -= 1

    # print(points)
    return points / len(opinions_source)


################################ DEPRECATED ############################


def sim_DEPREC(s1, s2):
    r = 0
    for i in s1:
        if i in s2:
            r += 1
    return r


def sim(a1, a2):
    t1 = struct.getTopics({0: a1})
    t2 = struct.getTopics({0: a2})

    inter = intersection(t1, t2)
    un = union(t1, t2)
    return len(inter) / len(un)


def pairing(sum1, sum2):
    r = 0
    for i in range(min(len(sum1), len(sum2))):
        r += sim(sum1[i], sum2[i])

    return r / (max(len(sum1), len(sum2)))


def comparability(sum1, sum2):
    t1 = []
    t2 = []
    for i in sum1:
        for o in sum1[i]['opinions']:
            if o[0] not in t1:
                t1.append(o[0])
    for i in sum2:
        for o in sum2[i]['opinions']:
            if o[0] not in t2:
                t2.append(o[0])
    inter = intersection(t1, t2)
    un = union(t1, t2)

    return len(inter) / len(un)


# def divergence(t1, t2):
# return 0.5 * (divergenceFrom(t1, t2) + divergenceFrom(t2, t1))


def divergence(t1, t2):
    c = 0
    r = 0
    for i in t1:
        for o1 in t1[i]['opinions']:
            asp1 = o1[0]
            sent1 = o1[1]
            best = 0
            for j in t2:
                for o2 in t2[j]['opinions']:
                    asp2 = o2[0]
                    if asp2 != asp1:
                        continue
                    c += 1
                    sent2 = o2[1]
                    d = abs(sent1 - sent2) / (2 * MAXSENT)
                    if d > best:
                        best = d
            r += best

    if c == 0:
        return 0

    r /= c

    return r


def conformity(sum1, sum2):
    c = 0
    r = 0
    for i in sum1:
        for o1 in sum1[i]['opinions']:
            asp1 = o1[0]
            sent1 = o1[1]
            best = 1
            for j in sum2:
                for o2 in sum2[j]['opinions']:
                    asp2 = o2[0]
                    if asp2 != asp1:
                        continue
                    c += 1
                    sent2 = o2[1]
                    d = abs(sent1 - sent2) / (2 * MAXSENT)
                    if d < best:
                        best = d
            r += best

    if c == 0:
        return 0

    r /= c

    return 1 - r


def equity(source, summ):
    r = 0
    for i in source:
        for o1 in source[i]['opinions']:
            asp1 = o1[0]
            sent1 = o1[1]
            best = 2 * MAXSENT
            for j in summ:
                for o2 in summ[j]['opinions']:
                    asp2 = o2[0]
                    if asp1 != asp2:
                        continue
                    sent2 = o2[1]
                    d = abs(sent1 - sent2)
                    if d < best:
                        best = d
            r += best / (2 * MAXSENT)
    return 1 - r / len(source)


def OLD_diversity(sum1, sum2):
    sim1 = 0
    sim2 = 0
    c1 = 0
    c2 = 0
    for i in sum1:
        for j in sum1:
            if i == j:
                continue
            sim1 += sim(sum1[i], sum1[j])
            c1 += 1

    for i in sum2:
        for j in sum2:
            if i == j:
                continue
            sim2 += sim(sum2[i], sum2[j])
            c2 += 1

    sim1 /= c1 + .001
    sim2 /= c2 + .001

    print(" sims: ", sim1, sim2)

    return 1 - 0.5 * (sim1 + sim2)


def diversity_OLD(summ):
    r = 0
    c = 0
    for i in summ:
        for j in summ:
            if i == j:
                continue
            r += sim(summ[i], summ[j])
            c += 1

    r /= c + .001

    return 1 - r


def aggregation(sum1, sum2, maxsize):
    # Total de tópicos em relação à quantidade que poderia conter
    topics = []
    for i in sum1:
        for o1 in sum1[i]['opinions']:
            a1 = o1[0]
            if a1 not in topics:
                topics.append(a1)
    for i in sum2:
        for o2 in sum2[i]['opinions']:
            a2 = o2[0]
            if a2 not in topics:
                topics.append(a2)

    return len(topics) / maxsize


def getSum_DEPRECATED(source, sumIndexes):
    summary = {}
    for i in sumIndexes:
        source[i]['sourceID'] = i
        summary[len(summary)] = source[i]
    return summary


def union(l1, l2):
    u = []
    for i in l1:
        if i not in u:
            u.append(i)
    for j in l2:
        if i not in u:
            u.append(i)
    return u


def intersection(l1, l2):
    r = []
    for i in l1:
        if i in l2:
            r.append(i)
    return r


def independentRepresentativiness(source, summ):
    T1 = struct.getTopics(source)
    TP = struct.getTopics(summ)
    return len(TP) / len(T1)


def representativiness_DEPREC(source1, sum1, source2, sum2):
    T1 = struct.getTopics(source1)
    T2 = struct.getTopics(source2)
    TP = struct.getTopics(sum1)
    TQ = struct.getTopics(sum2)

    T12 = union(T1, T2)
    TPQ = union(TP, TQ)

    return len(TPQ) / (len(T12))


def contrastiviness_repr(source1, source2, summ1, summ2):
    opinions_source1 = [item for sublist in [source1[j]['opinions'] for j in source1] for item in sublist]
    opinions_source2 = [item for sublist in [source2[j]['opinions'] for j in source2] for item in sublist]

    opinions_summ1 = [item for sublist in [summ1[j]['opinions'] for j in summ1] for item in sublist]
    opinions_summ2 = [item for sublist in [summ2[j]['opinions'] for j in summ2] for item in sublist]

    points = 0

    # Compares source 1 with summ 2 and vice-versa.
    for opinions_source, opinions_opposite_source, opinions_opposite_summ in zip([opinions_source1, opinions_source2],
                                                                                 [opinions_source2, opinions_source1],
                                                                                 [opinions_summ2, opinions_summ1]):

        all_possibles = []

        idx1_used = []
        idx2_used = []

        for idx1 in range(len(opinions_source)):
            if idx1 in idx1_used:
                continue
            op1 = opinions_source[idx1]
            for idx2 in range(len(opinions_opposite_source)):
                if idx2 in idx2_used:
                    continue
                op2 = opinions_opposite_source[idx2]
                pol1 = trinary_polarity(op1[1])
                pol2 = trinary_polarity(op2[1])
                if op1[0] == op2[0] and pol1 == -pol2:
                    asp_cont = (op1[0], pol1)  # This aspect has the possibility to form a possible contrastive pair.

                    all_possibles.append(asp_cont)

                    idx1_used.append(idx1)
                    idx2_used.append(idx2)

        pairs_formed = []

        idx1_used = []
        idx2_used = []

        for idx1 in range(len(opinions_source)):
            if idx1 in idx1_used:
                continue
            op1 = opinions_source[idx1]
            for idx2 in range(len(opinions_opposite_summ)):
                if idx2 in idx2_used:
                    continue

                op2 = opinions_opposite_summ[idx2]
                pol1 = trinary_polarity(op1[1])
                pol2 = trinary_polarity(op2[1])
                if op1[0] == op2[0] and pol1 == -pol2:
                    asp_cont = (
                        op1[0], pol1, pol2)  # This aspect has the possibility to form a possible contrastive pair.
                    pairs_formed.append(asp_cont)
                    idx1_used.append(idx1)
                    idx2_used.append(idx2)

        p = 0
        for o in all_possibles:
            for u in pairs_formed:
                if o[0] == u[0] and o[1] * u[1] >= 0:
                    p += 1
                    break

        points += p / len(all_possibles)

    return points / 2


def representativiness_aspect(source, summ):
    points = 0

    opinions_source = [item for sublist in [source[j]['opinions'] for j in source] for item in sublist]
    opinions_summ = [item for sublist in [summ[j]['opinions'] for j in summ] for item in sublist]

    for o in opinions_source:
        for u in opinions_summ:
            if o[0] == u[0] and o[1] * u[1] >= 0:
                points += 1
                break

    return points / len(opinions_source)


def contrastiviness_aspect(source, summ):
    points = 0

    opinions_source = [item for sublist in [source[j]['opinions'] for j in source] for item in sublist]
    opinions_summ = [item for sublist in [summ[j]['opinions'] for j in summ] for item in sublist]

    for o in opinions_source:
        for u in opinions_summ:
            if o[0] == u[0] and o[1] * u[1] <= 0:
                # print(o, u)
                points += 1
                break

    return points / len(opinions_source)
