import output_format


def idx_to_summ(source, indexes):
    return {i: source[i] for i in indexes}


# Rounds a number (to optimize use of cache and display of information)
def round_num(n):
    return float("%.2g" % n)  # rounds to 2 significant digits


def word_count(summ):
    r = 0
    for i in summ:
        r += summ[i]['word_count']
    return r


def compression(source, summ):
    return word_count(summ) / word_count(source)


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


def avgSent(info):
    if len(info) == 0:
        return 0

    a = 0
    c = 0
    for i in info:
        for o in info[i]['opinions']:
            a += o[1]
            c += 1

    return a / c


def bagOfWordsAndScores(info, measure):
    r = []
    for n in info:

        for a in info[n]['sent']:
            b = {}
            b['aspect'] = a
            b['value'] = info[n]['sent'][a]

            r.append(b)

    return r


def getGroupsPairsAspectSentim(info, measure):
    bow = bagOfWordsAndScores(info, measure)

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

        r[i['aspect']].append(p)

    return r


aspsentdistr_cache = {}

from setup import MAXPOLARITY


def trinary_polarity(num):
    if num < -0.25 * MAXPOLARITY:
        return -1
    if num > 0.25 * MAXPOLARITY:
        return +1
    return 0


# Calculate the (mean, stdev, probability) of each aspect
def aspects_stats(info):
    r = {}

    for i in info:
        n = {}
        for j in info[i]['sent']:
            n[j] = trinary_polarity(info[i]['sent'][j])
        r[i] = n
    return r
