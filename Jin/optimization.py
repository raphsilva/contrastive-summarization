import method

import structure as struct

import output_format as out

from pprint import pprint

INFINITY = 999999

from setup import LIM_SENTENCES
from setup import LIM_WORDS

from setup import GREEDY_CANDS_SELECTED
from setup import VERBOSE_MODE

from setup import DEBUG_MODE

from setup import METHOD

import random

RANDOM_SEED = 4

RANDOMIZE_DRAW = False  # If two candidates have the same score, chooses random (if true) or chooses the last found (false)


def random_seed():
    global RANDOM_SEED
    RANDOM_SEED = random.randint(0, 10000)
    # RANDOM_SEED = 4


from setup import KEY_MEASURE


def MakeContrastiveSummary(t1, t2, d1, d2, method='greedy', LIM_WORDS_1=LIM_WORDS, LIM_WORDS_2=LIM_WORDS):
    if method == 'greedy':
        return MakeContrastiveSummary_greedy(t1, t2, d1, d2, LIM_WORDS_1, LIM_WORDS_2)


def MakeContrastiveSummary_C(source1, source2, stats_source_1, stats_source_2, LIM_WORDS_1=LIM_WORDS,
                             LIM_WORDS_2=LIM_WORDS):
    candidate_options_1 = sorted(list(source1.keys()))
    candidate_options_2 = sorted(list(source2.keys()))
    random.seed(RANDOM_SEED)
    random.shuffle(candidate_options_1)
    random.shuffle(candidate_options_2)

    if METHOD == 'C':
        rank_1, rank_2 = method.rank_C(stats_source_1, stats_source_2)
    if METHOD == 'R':
        rank_1, rank_2 = method.rank_R(stats_source_1, stats_source_2)
    if METHOD == 'D':
        rank_1, rank_2 = method.rank_D(stats_source_1, stats_source_2)

    idx_summ_1 = []
    idx_summ_2 = []

    for i in rank_1:

        if i in idx_summ_1:
            continue

        idx_cand_1 = list(idx_summ_1) + [i]

        cand_1 = struct.idx_to_summ(source1, idx_cand_1)

        size_cand_1 = struct.word_count(cand_1)

        if size_cand_1 <= LIM_WORDS_1:
            idx_summ_1 = list(idx_cand_1)

        if len(idx_summ_1) >= LIM_SENTENCES:
            break

    for i in rank_2:

        if i in idx_summ_2:
            continue

        idx_cand_2 = list(idx_summ_2) + [i]

        cand_2 = struct.idx_to_summ(source2, idx_cand_2)

        size_cand_2 = struct.word_count(cand_2)

        if size_cand_2 <= LIM_WORDS_2:
            idx_summ_2 = list(idx_cand_2)

        if len(idx_summ_2) >= LIM_SENTENCES:
            break

    return idx_summ_1, idx_summ_2


def MakeContrastiveSummary_greedy(source1, source2, stats_source_1, stats_source_2, LIM_WORDS_1=LIM_WORDS,
                                  LIM_WORDS_2=LIM_WORDS):
    return MakeContrastiveSummary_C(source1, source2, stats_source_1, stats_source_2, LIM_WORDS_1, LIM_WORDS_2)


    # End of greedy algorithm to find best summary
