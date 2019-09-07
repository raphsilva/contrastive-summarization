import output_format
import statistics


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
        # print (i, source[i])
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
        if i == 'empresa' or i == 'EMPRESA' or i == '_NONE' or i[0] == 'X' or i[0] == 'x':
            continue
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
