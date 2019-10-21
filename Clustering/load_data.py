from write_files import get_variable_from_file

from language import process_sentence
from language import makecache_remove_negs_adjs


# Reads input files
def read_input(filename):
    g = get_variable_from_file(filename)
    info = g['data']

    r = {}

    for i in info:
        n = {}

        n['id'] = i['id']

        n['opinions'] = sorted(i['opinions'])  # Sorted to help cache

        n['sentence'] = i['sentence']

        n['word_count'] = len((n['sentence']).split())  # Number of words

        n['text_info'] = process_sentence(i['sentence'])

        r[n['id']] = n

        makecache_remove_negs_adjs(n['sentence'])

    return r


def preprocess(data):
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
