import Statistic.method as method
import common.console_output as out
import common.structure as struct

INFINITY = 999999

from OPTIONS import LIM_SENTENCES
from OPTIONS import LIM_WORDS

GREEDY_CANDS_SELECTED = 1

import random
random.seed(0)


def summarize(t1, t2, d1, d2, method):
    if method == 'single':
        r1 = makeSummarySingle(t1, d1)
        r2 = makeSummarySingle(t2, d2)
        return r1, r2

    if method == 'contrastive':
        return MakeContrastiveSummary(t1, t2, d1, d2)


def makeSummarySingle(source, original_stats, LIM_WORDS=LIM_WORDS):
    return makeSummary_greedy(source, original_stats, LIM_WORDS)


def MakeContrastiveSummary(t1, t2, d1, d2, LIM_WORDS_1=LIM_WORDS, LIM_WORDS_2=LIM_WORDS):
    return MakeContrastiveSummary_greedy(t1, t2, d1, d2, LIM_WORDS_1, LIM_WORDS_2)


def MakeContrastiveSummary_greedy(source1, source2, stats_source_1, stats_source_2, LIM_WORDS_1=LIM_WORDS,
                                  LIM_WORDS_2=LIM_WORDS):
    best_score = -INFINITY

    # total_candidates = len(source1) * len(source2)  # number of new candidates at each iteration

    top_candidates = [(([], []), -INFINITY)]

    candidate_options_1 = sorted(list(source1.keys()))
    candidate_options_2 = sorted(list(source2.keys()))

    random.shuffle(candidate_options_1)
    random.shuffle(candidate_options_2)

    for s in range(1, LIM_SENTENCES + 1):

        if len(top_candidates[0][0][0]) < s - 1 and len(top_candidates[0][0][1]) < s - 1:
            break

        search_paths = len(top_candidates)
        c_searched_paths = 0

        best_for_size_prev = [i[0] for i in top_candidates]

        for best_prev in best_for_size_prev:
            c_searched_paths += 1

            idx_best_for_size1 = best_prev[0]
            idx_best_for_size2 = best_prev[1]

            c = 0

            for i in candidate_options_1:

                c += 1

                if i in idx_best_for_size1:
                    continue  # Opinion already chosen.

                idx_cand_1 = idx_best_for_size1 + [i]

                summ_cand_1 = struct.idx_to_summ(source1, idx_cand_1)

                size_cand_1 = struct.word_count(summ_cand_1)

                if size_cand_1 > LIM_WORDS_1:
                    continue  # Candidate not considered because it is too long.

                stats_cand_1 = struct.aspects_stats(summ_cand_1)

                for j in candidate_options_2:

                    if j in idx_best_for_size2:
                        continue

                    idx_cand_2 = idx_best_for_size2 + [j]
                    summ_cand_2 = struct.idx_to_summ(source2, idx_cand_2)

                    size_cand_2 = struct.word_count(summ_cand_2)

                    if size_cand_2 > LIM_WORDS_2:
                        continue

                    stats_cand_2 = struct.aspects_stats(summ_cand_2)

                    score = method.SAM_contrastive(stats_source_1, stats_source_2, stats_cand_1,
                                                   stats_cand_2)

                    if size_cand_1 + size_cand_2 > (LIM_WORDS_1 + LIM_WORDS_2):
                        continue

                    if len(top_candidates) < GREEDY_CANDS_SELECTED:

                        top_candidates.append(((idx_cand_1, idx_cand_2), score))
                        top_candidates = sorted(top_candidates, key=lambda x: x[1], reverse=True)

                        out.printdebug("   ADDING TO FILL ", idx_cand_1, idx_cand_2)
                        out.printdebug("   score: ", score)
                        out.printdebug("   best: ", best_score)
                        out.printdebug("   sizes: ", size_cand_1, size_cand_2)
                        out.printdebug()

                    elif score >= top_candidates[0][-1]:
                        x = len(top_candidates) - 1
                        while x > 0 and top_candidates[x][1] < score:
                            x -= 1

                        top_candidates.insert(x, ((idx_cand_1, idx_cand_2), score))

                        del top_candidates[-1]

                        out.printdebug("   best candidates:  ", idx_cand_1, idx_cand_2)
                        out.printdebug("   score: ", score)
                        out.printdebug("   sizes: ", size_cand_1, size_cand_2)
                        out.printdebug()

                    best_score = top_candidates[0][1]

    best_summ1 = top_candidates[0][0][0]
    best_summ2 = top_candidates[0][0][1]

    return best_summ1, best_summ2


def makeSummary_greedy(source, stats_source, LIM_WORDS=LIM_WORDS):
    best_score = -INFINITY

    # total_candidates = len(source)

    top_candidates = [([], -INFINITY)]

    idx_best_for_size = {}
    idx_best_for_size[0] = []

    candidate_options = sorted(list(source.keys()))

    random.shuffle(candidate_options)

    for s in range(1, LIM_SENTENCES + 1):

        if len(top_candidates[0][0]) < s - 1:
            break  # Won't find any larger summary

        best_for_size_prev = [i[0] for i in top_candidates]

        search_paths = len(top_candidates)
        c_searched_paths = 0

        for best_prev in best_for_size_prev:
            c_searched_paths += 1

            idx_best_for_size = best_prev

            c = 0

            for i in candidate_options:
                c += 1
                pr = (s - 1) / LIM_SENTENCES + (c_searched_paths - 1) / search_paths / LIM_SENTENCES + c / len(
                    source) / search_paths / LIM_SENTENCES
                # out.printProgress(" %6.2lf%%   ( path %3d/%d  of  size  %2d/%d )  %16.2lf" % (
                #     100 * pr, c_searched_paths, search_paths, s, LIM_SENTENCES, best_score), end="\r")

                if i in idx_best_for_size:  # Candidate opinion already in the summary
                    continue

                idx_cand = idx_best_for_size + [i]

                summ_cand = struct.idx_to_summ(source, idx_cand)

                size_cand = struct.word_count(summ_cand)

                if size_cand > LIM_WORDS:
                    continue

                stats_cand = struct.aspects_stats(summ_cand)
                score = method.SAM(stats_source, stats_cand)

                if len(top_candidates) < GREEDY_CANDS_SELECTED:  # There's space for more candidates

                    top_candidates.append((idx_cand, score))
                    top_candidates = sorted(top_candidates, key=lambda x: x[1], reverse=True)

                    out.printdebug()
                    out.printdebug("   ADDING TO FILL ", idx_cand)
                    out.printdebug("   score: ", score)
                    out.printdebug("   best: ", best_score)
                    out.printdebug("   size: ", size_cand)
                    out.printdebug()

                elif score >= top_candidates[0][-1]:

                    x = len(top_candidates) - 1
                    while x > 0 and top_candidates[x][1] < score:
                        x -= 1

                    top_candidates.insert(x, (idx_cand, score))

                    del top_candidates[-1]

                    out.printdebug()
                    out.printdebug("   best candidate:  ", idx_cand)
                    out.printdebug("   score: ", score)
                    out.printdebug("   size: ", size_cand)
                    out.printdebug()

                best_score = top_candidates[0][1]

    best_idx = top_candidates[0][0]

    return best_idx
