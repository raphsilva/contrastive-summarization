import statistics

from OPTIONS import POLARITY_SCALE


def trinary_polarity(num):
    if num < -0.25 * POLARITY_SCALE:
        return -1
    if num > 0.25 * POLARITY_SCALE:
        return +1
    return 0


cache_get_opinions = {}


def get_opinions(source):
    key_cache = repr(source)
    if key_cache in cache_get_opinions:
        return cache_get_opinions[key_cache]
    r = []
    for j in source:

        for opinion in source[j]['opinions']:

            polarity = trinary_polarity(opinion[1])
            aspect = opinion[0]

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


import common.console_output as output_format


def idx_to_summ_SIMILARITY(source, indexes):
    r = {}
    pair_ID = 0
    for i in indexes:
        r[i] = source[i]
        r[i]['pair'] = pair_ID
        pair_ID += 1

    return r


def idx_to_summ(source, indexes):
    return {i: source[i] for i in indexes}


def get_summ_closest_to_scores(scores, map_scores_summary):
    def sqdiff(l1, l2):  # To determine difference between two summaries scores
        r = 0
        for i in range(len(l1)):
            r += pow(l1[i] - l2[i], 2)
        return r

    fairness_rank = sorted(map_scores_summary.keys(), key=lambda k: sqdiff(k, scores))

    summ_idx_f_1 = map_scores_summary[fairness_rank[0]][0]
    summ_idx_f_2 = map_scores_summary[fairness_rank[0]][1]

    return summ_idx_f_1, summ_idx_f_2


# Rounds a number
def round_num(n):
    return float("%.2g" % n)  # rounds to 2 significant digits


def word_count(summ):
    r = 0
    for i in summ:
        r += summ[i]['word_count']
    return r


def printOverview(distribution):
    for i in sorted(distribution, key=lambda x: distribution[x]['prob']):
        output_format.printinfo(
            "%-20s %3d %3d %8.4lf" % (i, distribution[i]['mean'], distribution[i]['std'], distribution[i]['prob']))
    print()


def getTopics(source):
    aspects = []
    for i in source:
        for j in source[i]['opinions']:
            if j[0] not in aspects:
                aspects.append(j[0])
    return aspects


def bagOfWordsAndScores(info):
    r = []
    for n in info:

        for a in info[n]['sent']:
            b = {}
            b['aspect'] = a
            # b['sentiment']  =   info[n]['opinions'][a]
            b['value'] = info[n]['sent'][a]
            # b['intensity']  =   info[n]['intensity']

            r.append(b)

    # pprint(r)
    # input()

    return r


def getGroupsPairsAspectSentim(info):
    bow = bagOfWordsAndScores(info)

    # /bow/ contains the representation of sentences using only one aspect, one sentiment, and the scores related to them.
    # Example:
    ''' [
        {'aspect': 'câmera', 'intensity': 50, 'sent': 83, 'sentiment': 'bom'},
        {'aspect': 'câmera', 'intensity': 75, 'sent': 88, 'sentiment': 'bom'},
        {'aspect': 'design', 'intensity': 60, 'sent': -85, 'sentiment': 'feio'}
    ] '''

    r = {}

    for i in bow:
        if i['aspect'] not in r.keys():
            r[i['aspect']] = []

        p = {}
        p['value'] = i['value']
        # p['intensity'] = i['intensity']

        r[i['aspect']].append(p)

    return r


aspsentdistr_cache = {}


# Calculate the (mean, stdev, probability) of each aspect
def aspects_stats(info):
    r = {}
    pairs = getGroupsPairsAspectSentim(info)

    if str(pairs) in aspsentdistr_cache:  # Tempo de execução caiu de 4'30" para 1'40" no força bruta tamanho 3.
        return aspsentdistr_cache[str(pairs)]

    # /pairs/ are tuples compound by an aspect and a list of every occurency of the aspect.
    # Example:
    ''' {
        'computador': [{'intensity': 80, 'sent': -88}],
        'cor': [{'intensity': 80, 'sent': -88},
                {'intensity': 60, 'sent': -85},
                {'intensity': 80, 'sent': -88}] 
    }'''

    total = 0
    for i in pairs:
        total += len(pairs[i])

    # if total < 10:
    # total = 10

    for i in pairs:

        if i not in r:
            r[i] = {'prob': round_num(len(pairs[i]) / total)}
            # if len(info) < 20:
            # r[i] = {'prob': 0.1*round_num(len(pairs[i])/total)}
        mean = statistics.mean([j['value'] for j in pairs[i]])
        r[i]['mean'] = round_num(mean)
        try:
            std = statistics.stdev([j['value'] for j in pairs[i]])
            r[i]['std'] = round_num(std)
        except:  # If stdev is not defined for that case
            r[i]['std'] = 0

        r[i]['std'] = max(20, r[i]['std'])

    aspsentdistr_cache[str(pairs)] = r

    return r


# Calculate the (mean, stdev, probability) of each aspect
def aspects_stats_SIMILARITY(info):
    r = {}

    for i in info:
        n = {}
        for j in info[i]['sent']:
            n[j] = trinary_polarity(info[i]['sent'][j])
        r[i] = n
    return r
