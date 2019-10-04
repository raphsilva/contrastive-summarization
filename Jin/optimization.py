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



def MakeContrastiveSummary_fast(source1, source2, stats_source1, stats_source2):
    best_score = -INFINITY

    idx_best1 = []
    idx_best2 = []

    score_gain1 = [[i, -INFINITY] for i in source1]
    score_gain2 = [[i, -INFINITY] for i in source2]

    for s in range(1, LIM_SENTENCES + 1):

        best_score_prev = best_score
        idx_best_prev1 = idx_best1
        idx_best_prev2 = idx_best2

        if max(len(idx_best_prev1), len(idx_best_prev2)) < s - 1:
            break

        score_gain1 = sorted(score_gain1, key=lambda x: x[1], reverse=True)
        score_gain2 = sorted(score_gain2, key=lambda x: x[1], reverse=True)

        for i in range(int(len(score_gain1))):

            pr = (s - 1) / LIM_SENTENCES + i / len(score_gain1) / LIM_SENTENCES
            out.printProgress("  %6.2lf%% " % (100 * pr), end='\r')

            if len(idx_best_prev1) >= 1 and len(idx_best1) > len(idx_best_prev1):
                break

            p1 = score_gain1[i]

            cand1 = p1[0]

            if cand1 in idx_best1:
                continue

            idx_cand1 = list(idx_best_prev1) + [cand1]

            summ_cand1 = struct.idx_to_summ(source1, idx_cand1)

            size_cand1 = struct.word_count(summ_cand1)

            if size_cand1 > LIM_WORDS:
                continue

            stats_cand1 = struct.aspects_stats(summ_cand1, KEY_MEASURE)

            for j in range(int(len(score_gain2))):

                if len(idx_best_prev2) >= 1 and len(idx_best2) > len(idx_best_prev2):
                    break

                p2 = score_gain2[j]

                cand2 = p2[0]

                if cand2 in idx_best2:
                    continue

                idx_cand2 = list(idx_best_prev2) + [cand2]

                summ_cand2 = struct.idx_to_summ(source2, idx_cand2)

                size_cand2 = struct.word_count(summ_cand2)

                if size_cand1 + size_cand2 > LIM_WORDS:
                    continue

                stats_cand2 = struct.aspects_stats(summ_cand2, KEY_MEASURE)

                score = method.score(stats_source1, stats_source2, stats_cand1, stats_cand2)

                score /= LIM_SENTENCES  # Normalize by limit of sentences (doesn't affect anything, only makes it prettier)

                g = score - best_score_prev
                score_gain2[j][1] += g
                score_gain1[i][1] += g / len(score_gain2)

                if score > best_score:
                    best_score = score
                    idx_best1 = idx_cand1
                    idx_best2 = idx_cand2

    print()
    return idx_best1, idx_best2
