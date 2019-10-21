from method import sent

from write_files import get_variable_from_file


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

        n['sent'] = opinionsToSent(n['opinions'])

        n['intensity'] = opinionsToIntensity(n['opinions'])

        r[n['id']] = n

    return r


def getAspectSent(opinions, aspect):
    s = []
    for i in opinions:
        if i[0] == aspect:
            s.append((i[0], i[1]))
    return sent(s)


def opinionsToSent(opinions):
    r = {}
    for i in opinions:
        if i[0] in r:
            continue
        r[i[0]] = getAspectSent(opinions, i[0])

    return r


def opinionsToIntensity(opinions):
    if len(opinions) == 0:
        return 0
    s = 0
    for o in opinions:
        s += abs(o[1])
    return s
