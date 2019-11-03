import method

import common.structure as struct

INFINITY = 999999

from options import LIM_SENTENCES

from options import options
METHOD = options['Similarity']['strategy']

import random
random.seed(0)


def MakeContrastiveSummary(source1, source2, stats_source_1, stats_source_2, LIM_WORDS_1,
                           LIM_WORDS_2):
    candidate_options_1 = sorted(list(source1.keys()))
    candidate_options_2 = sorted(list(source2.keys()))

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
