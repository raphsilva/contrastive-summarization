from Statistic.method import sent
from common.write_files import get_variable_from_file


# Reads input files
def read_input(filename):
    g = get_variable_from_file(filename)
    info = g['data']

    r = {}

    for i in info:

        n = {}

        n['id'] = i['id']

        n['opinions'] = sorted(i['opinions'])  # Sorted to help cache

        n['verbatim'] = i['sentence']

        n['word_count'] = len((n['verbatim']).split())  # Number of words

        n['words'] = [i for i in n['verbatim'].split() if len(i) > 2]

        n['sent'] = {}
        for o in n['opinions']:
            if o[0] not in n['sent']:
                n['sent'][o[0]] = o[1]
            else:
                n['sent'][o[0]] += o[1]

        r[n['id']] = n
    return r

from language import process_sentence
from language import makecache_remove_negs_adjs

# Reads input files
def read_input_CLUSTERING(filename):


    g = get_variable_from_file(filename)
    info = g['data']

    r = {}

    for i in info:
        n = {}

        n['id'] = i['id']

        n['opinions'] = sorted(i['opinions'])  # Sorted to help cache

        n['verbatim'] = i['sentence']

        n['word_count'] = len((n['verbatim']).split())  # Number of words

        n['text_info'] = process_sentence(i['sentence'])

        r[n['id']] = n

        makecache_remove_negs_adjs(n['verbatim'])

    return r


def preprocess_CLUSTERING(data):
    r = {'+': [], '-': []}  # Data will be returned split by polarity

    for sample_id in data:

        sample = data[sample_id]

        general_pol = 0  # Will define general polarity of sentence
        for opinion in sample['opinions']:
            general_pol += opinion[1]
        if general_pol < 0:
            pol = '-'
        elif general_pol > 0:
            pol = '+'
        else:
            continue  # Ignores neutral opinions

        n = {}
        n['text_info'] = sample['text_info']
        n['id'] = sample_id

        r[pol].append(n)

    return r


# Reads input files
def read_input_STATISTIC(filename):
    g = get_variable_from_file(filename)
    info = g['data']

    r = {}

    for i in info:
        n = {}

        n['id'] = i['id']

        n['opinions'] = sorted(i['opinions'])  # Sorted to help cache

        n['verbatim'] = i['sentence']

        n['word_count'] = len((n['verbatim']).split())  # Number of words

        n['sent'] = opinionsToSent_STATISTIC(n['opinions'])

        n['intensity'] = opinionsToIntensity_STATISTIC(n['opinions'])

        r[n['id']] = n

    return r


def getAspectSent_STATISTIC(opinions, aspect):
    s = []
    for i in opinions:
        if i[0] == aspect:
            s.append((i[0], i[1]))
    return sent(s)


def opinionsToSent_STATISTIC(opinions):
    r = {}
    for i in opinions:
        if i[0] in r:
            continue
        r[i[0]] = getAspectSent_STATISTIC(opinions, i[0])

    return r


def opinionsToIntensity_STATISTIC(opinions):
    if len(opinions) == 0:
        return 0
    s = 0
    for o in opinions:
        s += abs(o[1])
    return s
