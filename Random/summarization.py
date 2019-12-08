import common.structure as struct

from OPTIONS import LIM_SENTENCES
from OPTIONS import LIM_WORDS

import random
random.seed(0)


def make_contrastive_summary(source_1, source_2):
    return make_summary_random(source_1, source_2)


def make_summary_random(source_1, source_2):
    from random import sample

    indexes_1 = source_1.keys()
    indexes_2 = source_2.keys()

    # Choose random indexes for the summary, with size equal to the limit of sentences.
    summary_indexes_1 = sample(indexes_1, LIM_SENTENCES)
    summary_indexes_2 = sample(indexes_2, LIM_SENTENCES)

    # Build summary
    summary_1 = struct.get_summary_from_indexes(source_1, summary_indexes_1)
    summary_2 = struct.get_summary_from_indexes(source_2, summary_indexes_2)

    # Remove sentences until the summary size respects the limit of words.
    while struct.count_words(summary_1) > LIM_WORDS and len(summary_indexes_1) > 0:
        summary_indexes_1 = summary_indexes_1[:-1]
        summary_1 = struct.get_summary_from_indexes(source_1, summary_indexes_1)
    while struct.count_words(summary_2) > LIM_WORDS and len(summary_indexes_2) > 0:
        summary_indexes_2 = summary_indexes_2[:-1]
        summary_2 = struct.get_summary_from_indexes(source_2, summary_indexes_2)

    return summary_indexes_1, summary_indexes_2
