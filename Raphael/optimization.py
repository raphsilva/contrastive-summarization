import method

import structure as struct
from structure import trinary_polarity

import output_format as out

from pprint import pprint

INFINITY = 999999

from setup import LIM_SENTENCES
from setup import LIM_WORDS

from setup import GREEDY_CANDS_SELECTED
from setup import VERBOSE_MODE

from setup import SENTENCE_IDEAL_LENGTH
from setup import INDEPENDENT_RANK

import random

RANDOMIZE_DRAW = False  # If two candidates have the same score, chooses random (if true) or chooses the last found (false)

RANDOM_SEED = 7


def random_seed():
    global RANDOM_SEED
    RANDOM_SEED = random.randint(0, 10000)



def summarize(t1, t2, d1, d2, method, mode='greedy'):
    if method == 'noncontrastive':
        r1 = makeSummarySingle(t1, d1, mode='greedy')
        r2 = makeSummarySingle(t2, d2, mode='greedy')
        return r1, r2

    if method == 'contrastive':
        return MakeContrastiveSummary(t1, t2, d1, d2, mode='greedy')


def makeSummarySingle(source, original_stats, mode='greedy'):
    if mode == 'brute':
        return makeSummary_brute(source, original_stats)
    elif mode == 'fast':
        return makeSummary_fast(source, original_stats)
    elif mode == 'greedy':
        return makeSummary_greedy(source, original_stats)


def MakeContrastiveSummary(t1, t2, d1, d2, mode='greedy'):
    if mode == 'greedy':
        return MakeContrastiveSummary_greedy(t1, t2, d1, d2)
    elif mode == 'random':
        return MakeContrastiveSummary_random(t1, t2)
    if mode == 'brute':
        return MakeContrastiveSummary_brute(t1, t2, d1, d2)
    if mode == 'fast':
        return MakeContrastiveSummary_fast(t1, t2, d1, d2)
    if mode == 'selection':
        return MakeContrastiveSummary_selection(t1, t2)
    if mode == 'alternate':
        return MakeContrastiveSummary_alternate(t1, t2)


from structure import get_opinions
from structure import get_contrastive_pairs


def contrastive_pair_count(pair, op1, op2):
    c1 = 0
    c2 = 0
    f1 = 0
    f2 = 0

    for o in op1:
        if o[0] == pair[0] and o[1] == pair[1]:
            f1 += 1 / len(op1)
            c1 += 1

    for o in op2:
        if o[0] == pair[0] and o[1] == pair[2]:
            f2 += 1 / len(op2)
            c2 += 1
    return c1 * c2


def get_contrastive_pairs_rank(source1, source2):
    if INDEPENDENT_RANK:
        return get_contrastive_pairs_rank_independent(source1, source2)  # ATTENTION

    op1 = get_opinions(source1)
    op2 = get_opinions(source2)

    contrpairs = get_contrastive_pairs(op1, op2)

    cpairs_stats = {i: 0 for i in contrpairs}
    for i in contrpairs:
        cpairs_stats[i] = contrastive_pair_count(i, op1, op2)

    contr_rank = [i[0] for i in sorted(cpairs_stats.items(), key=lambda kv: kv[1], reverse=True)]

    contr_rank_1 = [(i[0], i[1]) for i in contr_rank]
    contr_rank_2 = [(i[0], i[2]) for i in contr_rank]

    return contr_rank_1, contr_rank_2


def contrastive_pair_count_independent(pair, op):
    c1 = 0

    for o in op:
        if o[0] == pair[0] and o[1] == pair[1]:
            c1 += 1

    return c1


def get_contrastive_pairs_rank_independent(source1, source2):
    op1 = get_opinions(source1)
    op2 = get_opinions(source2)

    contrpairs = get_contrastive_pairs(op1, op2)

    contrpairs_1 = [(i[0], i[1]) for i in contrpairs]
    contrpairs_2 = [(i[0], i[2]) for i in contrpairs]

    cpairs_stats_1 = {i: 0 for i in contrpairs_1}
    for i in contrpairs_1:
        cpairs_stats_1[i] = contrastive_pair_count_independent(i, op1)

    cpairs_stats_2 = {i: 0 for i in contrpairs_2}
    for i in contrpairs_2:
        cpairs_stats_2[i] = contrastive_pair_count_independent(i, op2)

    contr_rank_1 = [i[0] for i in sorted(cpairs_stats_1.items(), key=lambda kv: kv[1], reverse=True)]
    contr_rank_2 = [i[0] for i in sorted(cpairs_stats_2.items(), key=lambda kv: kv[1], reverse=True)]

    return contr_rank_1, contr_rank_2


def MakeContrastiveSummary_selection_side(source, opinions_rank, side):
    summ = []

    c_words = 0
    c_words_prev = -1

    desired_opinions = opinions_rank

    q_desired_opinions = list(desired_opinions)

    # Send generic to end of queue
    for i in reversed(range(len(q_desired_opinions))):
        if q_desired_opinions[i][0] == '_GENERIC':
            e = q_desired_opinions[i]
            del q_desired_opinions[i]
            q_desired_opinions.append(e)

    while c_words < LIM_WORDS:

        c_words_prev = c_words

        if q_desired_opinions == []:  # no more opinions found
            break

        p = q_desired_opinions.pop(0)  # this is a queue

        aspect = p[0]
        polarity = p[1]

        cand_sentences = []

        for i in source:

            if aspect not in source[i]['sent']:  # same aspect
                continue

            if source[i]['sent'][aspect] * polarity <= 0:  # same polarity
                continue

            if source[i] in summ:
                continue

            if c_words + source[i]['word_count'] <= LIM_WORDS:
                cand_sentences.append(source[i])

        best_size_diff = 9999

        if SENTENCE_IDEAL_LENGTH != 0:
            for s in cand_sentences:
                best_size_diff = min(best_size_diff, abs(SENTENCE_IDEAL_LENGTH - len(s['words'])))

        random.seed(RANDOM_SEED)
        random.shuffle(cand_sentences)

        for s in cand_sentences:

            if SENTENCE_IDEAL_LENGTH == 0 or abs(SENTENCE_IDEAL_LENGTH - len(s['words'])) == best_size_diff:

                summ.append(s)

                c_words += s['word_count']

                s_opinions = []

                for aspect in s['sent']:
                    s_opinions.append((aspect, trinary_polarity(s['sent'][aspect])))

                # Opinions covered in the selected sentence go to the end of queue
                for e in s_opinions:
                    if e in desired_opinions:
                        if e in q_desired_opinions:
                            q_desired_opinions.remove(e)
                        q_desired_opinions.append(e)

                break

    return summ



def MakeContrastiveSummary_selection(source1, source2):
    contr_rank_1, contr_rank_2 = get_contrastive_pairs_rank(source1, source2)

    summ1 = MakeContrastiveSummary_selection_side(source1, contr_rank_1, 1)
    summ2 = MakeContrastiveSummary_selection_side(source2, contr_rank_2, 2)

    summ1_idx = [e['id'] for e in summ1]
    summ2_idx = [e['id'] for e in summ2]

    return summ1_idx, summ2_idx


def get_elements_count(l):
    r = {i: 0 for i in l}
    for i in l:
        r[i] += 1 / len(l)
    return r


def MakeContrastiveSummary_alternate_side(source, repr_rank, contr_rank, side):
    summ = []

    c_words = 0

    q_contr = [i for i in contr_rank if i[1] != 0]
    q_repr = [i for i in repr_rank if i[1] != 0]

    # Send generic to end of queue
    for Q in [q_contr, q_repr]:
        for i in reversed(range(len(Q))):
            if Q[i][0] == '_GENERIC':
                e = Q[i]
                del Q[i]
                Q.append(e)

    turn = 0

    while c_words < LIM_WORDS:

        c_words_prev = c_words

        if q_contr == [] and q_repr == []:  # no more opinions found
            break

        if turn % 2 == 0:
            q_turn = q_contr
        if turn % 2 == 1:
            q_turn = q_repr

        turn += 1

        if q_turn == []:
            continue

        # p = q_turn.pop(0) # this is a queue
        p = q_turn[0]  # ATTENTION changed after tests (original above), but shouldn't change results for those cases.

        aspect = p[0]
        polarity = p[1]

        cand_sentences = []

        for i in source:

            if aspect not in source[i]['sent']:  # same aspect
                continue

            if source[i]['sent'][aspect] * polarity <= 0:  # same polarity
                continue

            if source[i] in summ:
                continue

            if c_words + source[i]['word_count'] <= LIM_WORDS:
                oo = [(i[0], 100 * i[1]) for i in q_turn]

                cand_sentences.append(source[i])

        if len(cand_sentences) == 0:  # No more sentences for this opinions
            del q_turn[0]

        cand_sentences = cand_sentences[::-1]

        best_size_diff = 9999

        if SENTENCE_IDEAL_LENGTH != 0:
            for s in cand_sentences:
                best_size_diff = min(best_size_diff, abs(SENTENCE_IDEAL_LENGTH - len(s['words'])))

        random.seed(RANDOM_SEED)
        random.shuffle(cand_sentences)

        for s in cand_sentences:

            # if True or abs(SENTENCE_IDEAL_LENGTH-len(s['words'])) == best_size_diff:
            if SENTENCE_IDEAL_LENGTH == 0 or abs(SENTENCE_IDEAL_LENGTH - len(s['words'])) == best_size_diff:

                summ.append(s)

                c_words += s['word_count']

                s_opinions = []

                for aspect in s['sent']:
                    s_opinions.append((aspect, trinary_polarity(s['sent'][aspect])))

                # Opinions covered in the selected sentence go to the end of queue
                for e in s_opinions:

                    if e in contr_rank:
                        if e in q_contr:
                            q_contr.remove(e)
                        q_contr.append(e)

                    if e in repr_rank:
                        if e in q_repr:
                            q_repr.remove(e)
                        q_repr.append(e)

                break

    return summ


def MakeContrastiveSummary_alternate(source1, source2):
    random.seed(RANDOM_SEED)

    contr_rank_1, contr_rank_2 = get_contrastive_pairs_rank(source1, source2)

    op1 = get_opinions(source1)
    op2 = get_opinions(source2)

    op_c_1 = get_elements_count(op1)
    op_c_2 = get_elements_count(op2)

    # contr_rank = [i[0] for i in sorted(cpairs_c.items(), key=lambda kv: kv[1], reverse=True)]
    repr1_rank = [i[0] for i in sorted(op_c_1.items(), key=lambda kv: kv[1], reverse=True)]
    repr2_rank = [i[0] for i in sorted(op_c_2.items(), key=lambda kv: kv[1], reverse=True)]

    summ1 = MakeContrastiveSummary_alternate_side(source1, repr1_rank, contr_rank_1, 1)
    summ2 = MakeContrastiveSummary_alternate_side(source2, repr2_rank, contr_rank_2, 2)

    summ1_idx = [e['id'] for e in summ1]
    summ2_idx = [e['id'] for e in summ2]

    return summ1_idx, summ2_idx


def MakeContrastiveSummary_random(source1, source2):
    from random import sample

    idx1 = source1.keys()
    idx2 = source2.keys()

    idx_cand_1 = sample(idx1, LIM_SENTENCES)
    idx_cand_2 = sample(idx2, LIM_SENTENCES)

    summ_cand_1 = struct.idx_to_summ(source1, idx_cand_1)
    summ_cand_2 = struct.idx_to_summ(source2, idx_cand_2)

    while struct.word_count(summ_cand_1) > LIM_WORDS and len(idx_cand_1) > 0:
        idx_cand_1 = idx_cand_1[:-1]
        summ_cand_1 = struct.idx_to_summ(source1, idx_cand_1)
    while struct.word_count(summ_cand_2) > LIM_WORDS and len(idx_cand_2) > 0:
        idx_cand_2 = idx_cand_2[:-1]
        summ_cand_2 = struct.idx_to_summ(source2, idx_cand_2)

    return idx_cand_1, idx_cand_2


def MakeContrastiveSummary_greedy(source1, source2, stats_source_1, stats_source_2, LIM_WORDS_1=LIM_WORDS,
                                  LIM_WORDS_2=LIM_WORDS):
    best_score = -INFINITY

    total_candidates = len(source1) * len(source2)  # number of new candidates at each iteration

    top_candidates = [(([], []), -INFINITY)]

    candidate_options_1 = sorted(list(source1.keys()))
    candidate_options_2 = sorted(list(source2.keys()))
    random.seed(RANDOM_SEED)
    random.shuffle(candidate_options_1)
    random.shuffle(candidate_options_2)

    for s in range(1, LIM_SENTENCES + 1):

        if len(top_candidates[0][0][0]) < s - 1 and len(top_candidates[0][0][1]) < s - 1:
            pprint(top_candidates)
            out.printMessage('\nWon\'t find any larger summary', s)
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

                pr = (s - 1) / LIM_SENTENCES + (c_searched_paths - 1) / search_paths / LIM_SENTENCES + c / len(
                    source1) / search_paths / LIM_SENTENCES
                out.printProgress(" %6.2lf%%   ( path %3d/%d  of  size  %2d/%d )  %16.2lf" % (
                    100 * pr, c_searched_paths, search_paths, s, LIM_SENTENCES, best_score), end="\r")
                out.printdebug()

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

                    idx_cand_2 = best_prev[1] + [j]

                    summ_cand_2 = struct.idx_to_summ(source2, idx_cand_2)

                    size_cand_2 = struct.word_count(summ_cand_2)

                    if size_cand_2 > LIM_WORDS_2:
                        continue

                    stats_cand_2 = struct.aspects_stats(summ_cand_2)

                    score = method.score_comp_summ(source1, source2, summ_cand_1, summ_cand_2)

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

    if VERBOSE_MODE:
        out.printinfo('Best score: ', best_score)

    best_summ1 = top_candidates[0][0][0]
    best_summ2 = top_candidates[0][0][1]

    return best_summ1, best_summ2

    # End of greedy algorithm to find best summary


def MakeContrastiveSummary_greedy_SELECT(source1, source2, stats_source_1, stats_source_2):
    best_score = -INFINITY

    total_candidates = len(source1) * len(source2)  # number of new candidates at each iteration

    top_candidates = [(([], []), -INFINITY)]

    opinions_source1 = []
    for j in source1:
        for i in source1[j]['sent']:
            opinions_source1.append((i, source1[j]['sent'][i]))

    opinions_source2 = []
    for j in source2:
        for i in source2[j]['sent']:
            opinions_source2.append((i, source2[j]['sent'][i]))

    all_possibles = []

    for op1 in opinions_source1:
        for op2 in opinions_source2:
            pol1 = (op1[1])
            pol2 = (op2[1])
            if op1[0] == op2[0] and pol1 == -pol2:
                asp_cont = (op1[0], pol1, pol2)  # This aspect has the possibility to form a possible contrastive pair.

                if asp_cont not in all_possibles:
                    all_possibles.append(asp_cont)

    for s in range(1, LIM_SENTENCES + 1):

        if len(top_candidates[0][0][0]) < s - 1 and len(top_candidates[0][0][1]) < s - 1:
            pprint(top_candidates)
            out.printMessage('\nWon\'t find any larger summary', s)
            break

        search_paths = len(top_candidates)
        c_searched_paths = 0

        best_for_size_prev = [i[0] for i in top_candidates]

        for best_prev in best_for_size_prev:
            c_searched_paths += 1

            idx_best_for_size1 = best_prev[0]
            idx_best_for_size2 = best_prev[1]

            c = 0

            for i in source1:

                c += 1

                pr = (s - 1) / LIM_SENTENCES + (c_searched_paths - 1) / search_paths / LIM_SENTENCES + c / len(
                    source1) / search_paths / LIM_SENTENCES
                out.printProgress(" %6.2lf%%   ( path %3d/%d  of  size  %2d/%d )  %16.2lf" % (
                    100 * pr, c_searched_paths, search_paths, s, LIM_SENTENCES, best_score), end="\r")
                out.printdebug()

                if i in idx_best_for_size1:
                    continue  # Opinion already chosen.

                idx_cand_1 = idx_best_for_size1 + [i]

                summ_cand_1 = struct.idx_to_summ(source1, idx_cand_1)

                size_cand_1 = struct.word_count(summ_cand_1)

                if size_cand_1 > LIM_WORDS:
                    continue  # Candidate not considered because it is too long.

                for j in source2:

                    if j in idx_best_for_size2:
                        continue

                    idx_cand_2 = best_prev[1] + [j]

                    summ_cand_2 = struct.idx_to_summ(source2, idx_cand_2)

                    size_cand_2 = struct.word_count(summ_cand_2)

                    if size_cand_2 > LIM_WORDS:
                        continue

                    opinions_summ1 = []
                    for j in summ_cand_1:
                        for i in summ_cand_1[j]['sent']:
                            opinions_summ1.append((i, summ_cand_1[j]['sent'][i]))

                    opinions_summ2 = []
                    for j in summ_cand_2:
                        for i in summ_cand_2[j]['sent']:
                            opinions_summ2.append((i, summ_cand_2[j]['sent'][i]))

                    d = 0

                    for p in all_possibles:
                        if (p[0], p[1]) in opinions_summ1:
                            d += 0.5
                        if (p[0], p[2]) in opinions_summ2:
                            d += 0.5

                    score = d / len(all_possibles)

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

    if VERBOSE_MODE:
        out.printinfo('Best score: ', best_score)

    best_summ1 = top_candidates[0][0][0]
    best_summ2 = top_candidates[0][0][1]

    return best_summ1, best_summ2

    # End of greedy algorithm to find best summary


def MakeContrastiveSummary_brute(source1, source2, stats_source_1, stats_source_2):
    import itertools

    best = -INFINITY
    best_summ1 = []
    best_summ2 = []

    p = 0

    tg1 = len(source1) + (LIM_SENTENCES - 1)  # Includes possibilities of none
    tg2 = len(source2) + (LIM_SENTENCES - 1)
    togo = 1
    for i in range(LIM_SENTENCES):
        togo *= tg1
        tg1 -= 1
    for i in range(LIM_SENTENCES):
        togo *= tg2
        tg2 -= 1
    print("togo = ", togo, len(source1), len(source2), LIM_SENTENCES)

    for L1 in range(0, LIM_SENTENCES + 1):

        for subset1 in itertools.combinations(list(source1.keys()), L1):

            if len(subset1) == 0:
                continue
            if len(subset1) > LIM_SENTENCES:
                break

            for L2 in range(0, LIM_SENTENCES + 1):
                for subset2 in itertools.combinations(list(source2.keys()), L2):

                    if len(subset2) == 0:
                        continue
                    if len(subset2) > LIM_SENTENCES:
                        break

                    cand1 = {i: source1[i] for i in subset1}
                    cand2 = {i: source2[i] for i in subset2}

                    if struct.word_count(cand1) > LIM_WORDS:
                        continue
                    if struct.word_count(cand2) > LIM_WORDS:
                        continue

                    summ_cand_1 = struct.idx_to_summ(source1, cand1)
                    summ_cand_2 = struct.idx_to_summ(source2, cand2)

                    stats_cand_1 = struct.aspects_stats(summ_cand_1)
                    stats_cand_2 = struct.aspects_stats(summ_cand_2)

                    score = method.score_comp_summ(stats_source_1, stats_source_2, stats_cand_1, stats_cand_2)

                    score /= LIM_SENTENCES  # Normalize by limit of sentences (doesn't affect anything, only makes it prettier)

                    p += 1
                    if p % 1000 == 0:
                        pr = float(p / togo)
                        out.printProgress("  %6.2lf%%   %10s %10s   %6.2lf   /   %10s %10s %6.2lf" % (
                            100 * pr, subset1, subset2, score, best_summ1, best_summ2, best))

                    if score >= best:
                        best = score
                        best_summ1 = subset1
                        best_summ2 = subset2

    sum1 = getSum(source1, list(best_summ1))
    sum2 = getSum(source2, list(best_summ2))

    return best_summ1, best_summ2


def makeSummary_fast(source, stats_source):
    best_score = -INFINITY

    idx_best = []

    score_gain = [[i, -INFINITY] for i in source]

    for s in range(1, LIM_SENTENCES + 1):

        best_score_prev = best_score
        idx_best_prev = idx_best

        if len(idx_best_prev) < s - 1:
            # print('not finding best', len(idx_best_prev), s-1)
            break

        score_gain = sorted(score_gain, key=lambda x: x[1], reverse=True)

        for i in range(int(len(score_gain))):

            # If already chose a new element for the summary, doesn't continue searching
            if len(idx_best_prev) >= 1 and len(idx_best) > len(idx_best_prev):
                break

            p = score_gain[i]

            c = p[0]

            idx_cand = idx_best_prev + [c]

            summ_cand = struct.idx_to_summ(source, idx_cand)

            size_cand = struct.word_count(summ_cand)

            if size_cand > LIM_WORDS:
                continue

            stats_cand = struct.aspects_stats(summ_cand)

            score = method.score_repr_summ(stats_source, stats_cand)

            g = score - best_score_prev
            score_gain[i][1] += g

            if score > best_score:
                best_score = score
                idx_best = idx_cand
    return idx_best


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
            # print('not finding best', len(idx_best_prev), s-1)
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

            stats_cand1 = struct.aspects_stats(summ_cand1)

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

                stats_cand2 = struct.aspects_stats(summ_cand2)

                score = method.score_comp_summ(stats_source1, stats_source2, stats_cand1, stats_cand2)

                g = score - best_score_prev
                score_gain2[j][1] += g
                score_gain1[i][1] += g / len(score_gain2)

                if score > best_score:
                    best_score = score
                    idx_best1 = idx_cand1
                    idx_best2 = idx_cand2

    print()
    return idx_best1, idx_best2


def makeSummary_greedy(source, stats_source):
    best_score = -INFINITY

    total_candidates = len(source)

    top_candidates = [([], -INFINITY)]

    idx_best_for_size = {}
    idx_best_for_size[0] = []

    for s in range(1, LIM_SENTENCES + 1):

        if len(top_candidates[0][0]) < s - 1:
            if VERBOSE_MODE:
                print()
                pprint(top_candidates)
                out.printMessage('\nWon\'t find any larger summary', s)
            break

        best_for_size_prev = [i[0] for i in top_candidates]

        search_paths = len(top_candidates)
        c_searched_paths = 0

        for best_prev in best_for_size_prev:
            c_searched_paths += 1

            idx_best_for_size = best_prev

            c = 0

            for candidate_opinion in source:
                c += 1
                pr = (s - 1) / LIM_SENTENCES + (c_searched_paths - 1) / search_paths / LIM_SENTENCES + c / len(
                    source) / search_paths / LIM_SENTENCES
                out.printProgress(" %6.2lf%%   ( path %3d/%d  of  size  %2d/%d )  %16.2lf" % (
                    100 * pr, c_searched_paths, search_paths, s, LIM_SENTENCES, best_score), end="\r")
                out.printdebug()

                i = candidate_opinion

                sent_density = source[candidate_opinion]['intensity']['aspects'] / source[candidate_opinion][
                    'word_count']

                if i in idx_best_for_size:  # Candidate opinion already in the summary
                    continue

                idx_cand = idx_best_for_size + [i]

                summ_cand = struct.idx_to_summ(source, idx_cand)

                size_cand = struct.word_count(summ_cand)

                if size_cand > LIM_WORDS:
                    continue

                stats_cand = struct.aspects_stats(summ_cand)

                score = method.score_repr_summ(source, summ_cand)

                prob = 10 / len(source)
                draw = random.uniform(0, 1)

                if len(top_candidates) < GREEDY_CANDS_SELECTED:  # There's space for more candidates

                    top_candidates.append((idx_cand, score))
                    top_candidates = sorted(top_candidates, key=lambda x: x[1], reverse=True)

                    out.printdebug("   ADDING TO FILL ", idx_cand)
                    out.printdebug("   score: ", score)
                    out.printdebug("   best: ", best_score)
                    out.printdebug("   size: ", size_cand)
                    out.printdebug()


                elif score >= top_candidates[0][-1]:

                    # If score is best than the worst top candidate, the worse is replaced by the new.
                    # If score is equal than the worst top candidate, it may be replaced or not based on random decision

                    x = len(top_candidates) - 1
                    while x > 0 and top_candidates[x][1] < score:
                        x -= 1

                    top_candidates.insert(x, (idx_cand, score))

                    del top_candidates[-1]

                    out.printdebug("   best candidate:  ", idx_cand)
                    out.printdebug("   score: ", score)
                    out.printdebug("   size: ", size_cand)
                    out.printdebug()

                best_score = top_candidates[0][1]

    best_idx = top_candidates[0][0]

    return best_idx


def makeSummary_greedy_DEPREC(source, stats_source):
    print('RUNNING DEPREC VERSION 557')

    best_score = -INFINITY

    idx_best_for_size = {}
    idx_best_for_size[0] = []

    for s in range(1, LIM_SENTENCES + 1):

        idx_best_for_size[s] = idx_best_for_size[s - 1]

        for candidate_opinion in source:

            i = candidate_opinion

            if i in idx_best_for_size[s - 1]:  # Candidate opinion already in the summary
                continue

            idx_cand = idx_best_for_size[s - 1] + [i]

            summ_cand = struct.idx_to_summ(source, idx_cand)

            size_cand = struct.word_count(summ_cand)

            if size_cand > LIM_WORDS:
                continue

            stats_cand = struct.aspects_stats(summ_cand)

            score = method.score_repr_summ(stats_source, stats_cand)

            score /= LIM_SENTENCES  # Normalize by limit of sentences (doesn't affect anything, only makes it prettier)

            if score >= best_score:
                best_score = score
                idx_best_for_size[s] = idx_cand

                out.printdebug('*', idx_cand, score)

            else:
                out.printdebug(idx_cand, score)

    best_idx = idx_best_for_size[LIM_SENTENCES]

    return best_idx


def makeSummary_brute(source, stats_source):
    import itertools
    from scipy.special import comb

    best_score = -INFINITY
    best_idx = []

    # Variables to display progress
    pr_cur = 0
    pr_tot = 0
    for i in range(1, LIM_SENTENCES + 1):
        pr_tot += comb(len(source), i)  # Counts all possible combinations

    for L1 in range(1, LIM_SENTENCES + 1):  # For each possible size of summary

        for idx_cand in itertools.combinations(list(source.keys()), L1):  # For each possible subset of that size

            summ_cand = struct.idx_to_summ(source, idx_cand)

            stats_cand = struct.aspects_stats(summ_cand)

            score = method.score_repr_summ(stats_source, stats_cand)

            score /= LIM_SENTENCES  # Normalize by limit of sentences (doesn't affect anything, only makes it prettier)

            if score >= best_score:
                best_score = score
                best_idx = idx_cand

            # Display progress information
            pr_cur += 1
            pr = pr_cur / pr_tot
            if pr_cur % 100 == 0:
                out.printProgress("  %6.2lf%% " % (100 * pr), end="\r")
                out.printdebug(" cur subset: %20s   score:  %6.2lf   /  best subset: %10s  score: %6.5lf" % (
                    idx_cand, score, best_idx, best_score))

    return best_idx
