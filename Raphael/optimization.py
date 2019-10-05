import structure as struct
from structure import trinary_polarity

INFINITY = 999999

from setup import LIM_SENTENCES
from setup import LIM_WORDS

from setup import SENTENCE_IDEAL_LENGTH
from setup import INDEPENDENT_RANK

import random

RANDOMIZE_DRAW = False  # If two candidates have the same score, chooses random (if true) or chooses the last found (false)

RANDOM_SEED = 7


def random_seed():
    global RANDOM_SEED
    RANDOM_SEED = random.randint(0, 10000)


def MakeContrastiveSummary(t1, t2, mode):
    if mode == 'random':
        return MakeContrastiveSummary_random(t1, t2)
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


def contrastive_pair_count_independent(pair, op):
    c1 = 0

    for o in op:
        if o[0] == pair[0] and o[1] == pair[1]:
            c1 += 1

    return c1


def get_elements_count(l):
    r = {i: 0 for i in l}
    for i in l:
        r[i] += 1 / len(l)
    return r


def get_contrastive_pairs_rank(source1, source2):
    if INDEPENDENT_RANK:
        return get_contrastive_pairs_rank_independent(source1, source2)
    else:
        return get_contrastive_pairs_rank_conjugated(source1, source2)


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


def get_contrastive_pairs_rank_conjugated(source1, source2):
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


def MakeContrastiveSummary_selection(source1, source2):
    contr_rank_1, contr_rank_2 = get_contrastive_pairs_rank(source1, source2)

    summ1 = MakeContrastiveSummary_selection_side(source1, contr_rank_1)
    summ2 = MakeContrastiveSummary_selection_side(source2, contr_rank_2)

    summ1_idx = [e['id'] for e in summ1]
    summ2_idx = [e['id'] for e in summ2]

    return summ1_idx, summ2_idx


def MakeContrastiveSummary_alternate(source1, source2):
    contr_rank_1, contr_rank_2 = get_contrastive_pairs_rank(source1, source2)

    op1 = get_opinions(source1)
    op2 = get_opinions(source2)

    op_c_1 = get_elements_count(op1)
    op_c_2 = get_elements_count(op2)

    # contr_rank = [i[0] for i in sorted(cpairs_c.items(), key=lambda kv: kv[1], reverse=True)]
    repr1_rank = [i[0] for i in sorted(op_c_1.items(), key=lambda kv: kv[1], reverse=True)]
    repr2_rank = [i[0] for i in sorted(op_c_2.items(), key=lambda kv: kv[1], reverse=True)]

    summ1 = MakeContrastiveSummary_alternate_side(source1, repr1_rank, contr_rank_1)
    summ2 = MakeContrastiveSummary_alternate_side(source2, repr2_rank, contr_rank_2)

    summ1_idx = [e['id'] for e in summ1]
    summ2_idx = [e['id'] for e in summ2]

    return summ1_idx, summ2_idx


def MakeContrastiveSummary_selection_side(source, opinions_rank):
    summ = []

    c_words = 0

    desired_opinions = opinions_rank

    q_desired_opinions = list(desired_opinions)

    # Send generic to end of queue
    for i in reversed(range(len(q_desired_opinions))):
        if q_desired_opinions[i][0] == '_GENERIC':
            e = q_desired_opinions[i]
            del q_desired_opinions[i]
            q_desired_opinions.append(e)

    while c_words < LIM_WORDS:

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


def MakeContrastiveSummary_alternate_side(source, repr_rank, contr_rank):
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


def MakeContrastiveSummary_random(source1, source2):
    from random import sample

    idx1 = source1.keys()
    idx2 = source2.keys()

    # Choose random indexes for the summary, with size equal to the limit of sentences.
    summ1_idx = sample(idx1, LIM_SENTENCES)
    summ2_idx = sample(idx2, LIM_SENTENCES)

    # Build summary
    summ1 = struct.idx_to_summ(source1, summ1_idx)
    summ2 = struct.idx_to_summ(source2, summ2_idx)

    # Remove sentences until the sumary size respects the limit of words.
    while struct.word_count(summ1) > LIM_WORDS and len(summ1_idx) > 0:
        summ1_idx = summ1_idx[:-1]
        summ1 = struct.idx_to_summ(source1, summ1_idx)
    while struct.word_count(summ2) > LIM_WORDS and len(summ2_idx) > 0:
        summ2_idx = summ2_idx[:-1]
        summ2 = struct.idx_to_summ(source2, summ2_idx)

    return summ1_idx, summ2_idx
