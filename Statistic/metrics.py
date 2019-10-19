MAXSENT = 100

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

    return 1 - p  # (p/len(c_source))


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

    # Compares source 1 with summ 2 and vice-versa.
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
