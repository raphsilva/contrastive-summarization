import random
random.seed(0)


def get_topics(source):
    t = []
    for i in source:
        for o in source[i]:
            if o not in t:
                t.append(o)
    return t


def similarity(op1, op2):
    t1 = []
    t2 = []
    for i in op1:
        if i not in t1:
            t1.append(i)
    for i in op2:
        if i not in t2:
            t2.append(i)

    intersection = [i for i in t1 if i in t2]
    union = list(set(t1 + t2))

    r = len(intersection) / len(union)

    return r


def eval_C(summ1, summ2):
    s = 0
    k = min(len(summ1), len(summ2))
    for i in range(k):
        s += similarity(summ1[i]['sent']['corpus'], summ2[i]['sent']['corpus'])
    return s / k


def eval_R(source1, source2, summ1, summ2):
    t_e1 = get_topics(source1)
    t_e2 = get_topics(source2)
    t_r1 = get_topics(summ1)
    t_r2 = get_topics(summ2)

    union_E = list(set(t_e1 + t_e2))
    union_R = list(set(t_r1 + t_r2))

    return len(union_R) / len(union_E)


def eval_D(summ1, summ2):
    s1 = 0
    s2 = 0
    c1 = 0
    c2 = 0
    for i in summ1:
        for j in summ1:
            if i == j:
                continue
            s1 += similarity(summ1[i]['sent']['corpus'], summ1[j]['sent']['corpus'])
            c1 += 1
    for i in summ2:
        for j in summ2:
            if i == j:
                continue
            s2 += similarity(summ2[i]['sent']['corpus'], summ2[j]['sent']['corpus'])
            c2 += 1

    return 1 - 0.5 * (s1 / c1 + s2 / c2)


def rank_R(source1_stats, source2_stats):
    scores_1 = {}
    scores_2 = {}

    for i in source1_stats:
        s = 0
        for j in source1_stats:
            if j == i:
                continue
            s += similarity(source1_stats[i], source1_stats[j])
        scores_1[i] = s

    for i in source2_stats:
        s = 0
        for j in source2_stats:
            if j == i:
                continue
            s += similarity(source2_stats[i], source2_stats[j])
        scores_2[i] = s

    rank_1 = sorted(scores_1.keys(), key=lambda i: scores_1[i] + random.uniform(-0.001, 0.001), reverse=True)
    rank_2 = sorted(scores_2.keys(), key=lambda i: scores_2[i] + random.uniform(-0.001, 0.001), reverse=True)

    return rank_1, rank_2


def rank_D(source1_stats, source2_stats):
    scores_1 = {}
    scores_2 = {}

    for i in source1_stats:
        s = 0
        for j in source1_stats:
            if j == i:
                continue
            s -= similarity(source1_stats[i], source1_stats[j])
        scores_1[i] = s

    for i in source2_stats:
        s = 0
        for j in source2_stats:
            if j == i:
                continue
            s -= similarity(source2_stats[i], source2_stats[j])
        scores_2[i] = s

    rank_1 = sorted(scores_1.keys(), key=lambda i: scores_1[i] + random.uniform(-0.001, 0.001), reverse=True)
    rank_2 = sorted(scores_2.keys(), key=lambda i: scores_2[i] + random.uniform(-0.001, 0.001), reverse=True)

    return rank_1, rank_2


def rank_C(source1_stats, source2_stats):
    scores = {}
    for i in source1_stats:
        for j in source2_stats:
            scores[(i, j)] = similarity(source1_stats[i], source2_stats[j])

    rank = sorted(scores.keys(), key=lambda i: scores[i] + random.uniform(-0.001, 0.001), reverse=True)

    rank_1 = [i[0] for i in rank]
    rank_2 = [i[1] for i in rank]

    return rank_1, rank_2
