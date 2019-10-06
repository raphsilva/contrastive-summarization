import structure as struct
from structure import trinary_polarity

INFINITY = 999999

from setup import LIM_SENTENCES
from setup import LIM_WORDS

from setup import LOW_PRIORITY_ASPECTS

from setup import SENTENCE_IDEAL_LENGTH
from setup import INDEPENDENT_RANK

from structure import get_opinions
from structure import get_contrastive_pairs

import random

RANDOMIZE_DRAW = False  # If two candidates have the same score, chooses random (if true) or chooses the last found (false)

RANDOM_SEED = 7


def random_seed():
    global RANDOM_SEED
    RANDOM_SEED = random.randint(0, 10000)


def MakeContrastiveSummary(source_1, source_2, mode):
    if mode == 'random':
        return make_summary_random(source_1, source_2)
    if mode == 'selection':
        return make_summary_selection(source_1, source_2)
    if mode == 'alternate':
        return make_summary_alternate(source_1, source_2)




def contrastive_pair_count(pair, opinions_1, opinions_2):
    c1 = 0
    c2 = 0

    for o in opinions_1:
        if o[0] == pair[0] and o[1] == pair[1]:
            c1 += 1

    for o in opinions_2:
        if o[0] == pair[0] and o[1] == pair[2]:
            c2 += 1

    return c1 * c2


def contrastive_pair_count_independent(pair, opinions):
    c = 0

    for o in opinions:
        if o[0] == pair[0] and o[1] == pair[1]:
            c += 1

    return c


def get_elements_count(l):
    r = {i: 0 for i in l}
    for i in l:
        r[i] += 1 / len(l)
    return r


def get_contrastive_pairs_rank(source_1, source_2):
    if INDEPENDENT_RANK:
        return get_contrastive_pairs_rank_independent(source_1, source_2)
    else:
        return get_contrastive_pairs_rank_conjugated(source_1, source_2)


def get_contrastive_pairs_rank_independent(source_1, source_2):
    opinions_1 = get_opinions(source_1)
    opinions_2 = get_opinions(source_2)

    contrpairs = get_contrastive_pairs(opinions_1, opinions_2)

    contrpairs_1 = [(i[0], i[1]) for i in contrpairs]
    contrpairs_2 = [(i[0], i[2]) for i in contrpairs]

    cpairs_stats_1 = {i: 0 for i in contrpairs_1}
    for i in contrpairs_1:
        cpairs_stats_1[i] = contrastive_pair_count_independent(i, opinions_1)

    cpairs_stats_2 = {i: 0 for i in contrpairs_2}
    for i in contrpairs_2:
        cpairs_stats_2[i] = contrastive_pair_count_independent(i, opinions_2)

    contr_rank_1 = [i[0] for i in sorted(cpairs_stats_1.items(), key=lambda kv: kv[1], reverse=True)]
    contr_rank_2 = [i[0] for i in sorted(cpairs_stats_2.items(), key=lambda kv: kv[1], reverse=True)]

    return contr_rank_1, contr_rank_2


def get_contrastive_pairs_rank_conjugated(source_1, source_2):
    opinions_1 = get_opinions(source_1)
    opinions_2 = get_opinions(source_2)

    contrpairs = get_contrastive_pairs(opinions_1, opinions_2)

    cpairs_stats = {i: 0 for i in contrpairs}
    for i in contrpairs:
        cpairs_stats[i] = contrastive_pair_count(i, opinions_1, opinions_2)

    contr_rank = [i[0] for i in sorted(cpairs_stats.items(), key=lambda kv: kv[1], reverse=True)]

    contr_rank_1 = [(i[0], i[1]) for i in contr_rank]
    contr_rank_2 = [(i[0], i[2]) for i in contr_rank]

    return contr_rank_1, contr_rank_2


def make_summary_selection(source_1, source_2):
    contr_rank_1, contr_rank_2 = get_contrastive_pairs_rank(source_1, source_2)

    summary_1 = MakeContrastiveSummary_selection_side(source_1, contr_rank_1)
    summary_2 = MakeContrastiveSummary_selection_side(source_2, contr_rank_2)

    summary_indexes_1 = [e['id'] for e in summary_1]
    summary_indexes_2 = [e['id'] for e in summary_2]

    return summary_indexes_1, summary_indexes_2


def make_summary_alternate(source_1, source_2):
    contr_rank_1, contr_rank_2 = get_contrastive_pairs_rank(source_1, source_2)

    opinions_1 = get_opinions(source_1)
    opinions_2 = get_opinions(source_2)

    op_c_1 = get_elements_count(opinions_1)
    op_c_2 = get_elements_count(opinions_2)

    repr_rank_1 = [i[0] for i in sorted(op_c_1.items(), key=lambda kv: kv[1], reverse=True)]
    repr_rank_2 = [i[0] for i in sorted(op_c_2.items(), key=lambda kv: kv[1], reverse=True)]

    summary_1 = MakeContrastiveSummary_alternate_side(source_1, repr_rank_1, contr_rank_1)
    summary_2 = MakeContrastiveSummary_alternate_side(source_2, repr_rank_2, contr_rank_2)

    summary_indexes_1 = [e['id'] for e in summary_1]
    summary_indexes_2 = [e['id'] for e in summary_2]

    return summary_indexes_1, summary_indexes_2


def MakeContrastiveSummary_selection_side(source, contr_rank):
    summary = []

    count_words = 0

    desired_opinions = contr_rank

    q_desired_opinions = list(desired_opinions)

    # Send low priority aspects to end of queue
    for i in reversed(range(len(q_desired_opinions))):
        if q_desired_opinions[i][0] in LOW_PRIORITY_ASPECTS:
            e = q_desired_opinions[i]
            del q_desired_opinions[i]
            q_desired_opinions.append(e)

    while count_words < LIM_WORDS:

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

            if source[i] in summary:
                continue

            if count_words + source[i]['word_count'] <= LIM_WORDS:
                cand_sentences.append(source[i])

        best_size_diff = INFINITY

        if SENTENCE_IDEAL_LENGTH != 0:
            for s in cand_sentences:
                best_size_diff = min(best_size_diff, abs(SENTENCE_IDEAL_LENGTH - len(s['words'])))

        random.seed(RANDOM_SEED)
        random.shuffle(cand_sentences)

        for s in cand_sentences:

            if SENTENCE_IDEAL_LENGTH == 0 or abs(SENTENCE_IDEAL_LENGTH - len(s['words'])) == best_size_diff:

                summary.append(s)

                count_words += s['word_count']

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

    return summary


def MakeContrastiveSummary_alternate_side(source, repr_rank, contr_rank):
    summary = []

    count_words = 0

    q_contr = [i for i in contr_rank if i[1] != 0]  # Queue that considers contrastivity.
    q_repr = [i for i in repr_rank if i[1] != 0]  # Queue that considers representativity.

    # Send low priority aspects to end of queue
    for Q in [q_contr, q_repr]:
        for i in reversed(range(len(Q))):
            if Q[i][0] in LOW_PRIORITY_ASPECTS:
                e = Q[i]
                del Q[i]
                Q.append(e)

    turn = 0

    while count_words < LIM_WORDS:

        if q_contr == [] and q_repr == []:  # no more opinions found
            break

        if turn % 2 == 0:
            q_turn = q_contr
        if turn % 2 == 1:
            q_turn = q_repr

        turn += 1

        if q_turn == []:
            continue

        p = q_turn[0]

        aspect = p[0]
        polarity = p[1]

        cand_sentences = []

        for i in source:

            if aspect not in source[i]['sent']:  # same aspect
                continue

            if source[i]['sent'][aspect] * polarity <= 0:  # same polarity
                continue

            if source[i] in summary:
                continue

            if count_words + source[i]['word_count'] <= LIM_WORDS:
                cand_sentences.append(source[i])

        if len(cand_sentences) == 0:  # No more sentences for this opinions
            del q_turn[0]

        cand_sentences = cand_sentences[::-1]

        best_size_diff = INFINITY

        if SENTENCE_IDEAL_LENGTH != 0:
            for s in cand_sentences:
                best_size_diff = min(best_size_diff, abs(SENTENCE_IDEAL_LENGTH - len(s['words'])))

        random.seed(RANDOM_SEED)
        random.shuffle(cand_sentences)

        for s in cand_sentences:

            if SENTENCE_IDEAL_LENGTH == 0 or abs(SENTENCE_IDEAL_LENGTH - len(s['words'])) == best_size_diff:

                summary.append(s)

                count_words += s['word_count']

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

    return summary


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

    # Remove sentences until the sumary size respects the limit of words.
    while struct.count_words(summary_1) > LIM_WORDS and len(summary_indexes_1) > 0:
        summary_indexes_1 = summary_indexes_1[:-1]
        summary_1 = struct.get_summary_from_indexes(source_1, summary_indexes_1)
    while struct.count_words(summary_2) > LIM_WORDS and len(summary_indexes_2) > 0:
        summary_indexes_2 = summary_indexes_2[:-1]
        summary_2 = struct.get_summary_from_indexes(source_2, summary_indexes_2)

    return summary_indexes_1, summary_indexes_2
