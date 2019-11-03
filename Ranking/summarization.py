import common.structure as struct
from common.structure import trinary_polarity

INFINITY = 999999

from options import LIM_SENTENCES
from options import LIM_WORDS

# from options_c import LOW_PRIORITY_ASPECTS

from options import options

RANKING_MODE = options['Ranking']['strategy']
INDEPENDENT_RANK = options['Ranking']['independent']
SENTENCE_IDEAL_LENGTH = options['Ranking']['ideal length']

from common.structure import get_opinions
from common.structure import get_contrastive_pairs

import random
random.seed(0)


def make_contrastive_summary(source_1, source_2, mode):
    if mode == 'random':
        return make_summary_random(source_1, source_2)
    if mode == 'contrastive':
        return make_summary_contrastive(source_1, source_2)
    if mode == 'contrastive+representative':
        return make_summary_contrastive_and_representative(source_1, source_2)


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


def get_opinions_frequency(l):
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

    contrastive_pairs = get_contrastive_pairs(opinions_1, opinions_2)

    contrastive_opinions_1 = [(i[0], i[1]) for i in contrastive_pairs]
    contrastive_opinions_2 = [(i[0], i[2]) for i in contrastive_pairs]

    count_contrastive_opinions_1 = {i: 0 for i in contrastive_opinions_1}
    for i in contrastive_opinions_1:
        count_contrastive_opinions_1[i] = contrastive_pair_count_independent(i, opinions_1)

    count_contrastive_opinions_2 = {i: 0 for i in contrastive_opinions_2}
    for i in contrastive_opinions_2:
        count_contrastive_opinions_2[i] = contrastive_pair_count_independent(i, opinions_2)

    contr_rank_1 = [i[0] for i in sorted(count_contrastive_opinions_1.items(), key=lambda i: i[1], reverse=True)]
    contr_rank_2 = [i[0] for i in sorted(count_contrastive_opinions_2.items(), key=lambda i: i[1], reverse=True)]

    return contr_rank_1, contr_rank_2


def get_contrastive_pairs_rank_conjugated(source_1, source_2):
    opinions_1 = get_opinions(source_1)
    opinions_2 = get_opinions(source_2)

    contrastive_pairs = get_contrastive_pairs(opinions_1, opinions_2)

    count_contrastive_pairs = {i: 0 for i in contrastive_pairs}
    for i in contrastive_pairs:
        count_contrastive_pairs[i] = contrastive_pair_count(i, opinions_1, opinions_2)

    contr_rank = [i[0] for i in sorted(count_contrastive_pairs.items(), key=lambda i: i[1], reverse=True)]

    contr_rank_1 = [(i[0], i[1]) for i in contr_rank]
    contr_rank_2 = [(i[0], i[2]) for i in contr_rank]

    return contr_rank_1, contr_rank_2


def make_summary_contrastive(source_1, source_2):
    contr_rank_1, contr_rank_2 = get_contrastive_pairs_rank(source_1, source_2)

    summary_1 = make_summary_side_contrastive(source_1, contr_rank_1)
    summary_2 = make_summary_side_contrastive(source_2, contr_rank_2)

    summary_indexes_1 = [e['id'] for e in summary_1]
    summary_indexes_2 = [e['id'] for e in summary_2]

    return summary_indexes_1, summary_indexes_2


def make_summary_contrastive_and_representative(source_1, source_2):
    contr_rank_1, contr_rank_2 = get_contrastive_pairs_rank(source_1, source_2)

    opinions_1 = get_opinions(source_1)
    opinions_2 = get_opinions(source_2)

    opinions_frequency_1 = get_opinions_frequency(opinions_1)
    opinions_frequency_2 = get_opinions_frequency(opinions_2)

    repr_rank_1 = [i[0] for i in sorted(opinions_frequency_1.items(), key=lambda kv: kv[1], reverse=True)]
    repr_rank_2 = [i[0] for i in sorted(opinions_frequency_2.items(), key=lambda kv: kv[1], reverse=True)]

    summary_1 = make_summary_side_contrastive_and_representative(source_1, repr_rank_1, contr_rank_1)
    summary_2 = make_summary_side_contrastive_and_representative(source_2, repr_rank_2, contr_rank_2)

    summary_indexes_1 = [e['id'] for e in summary_1]
    summary_indexes_2 = [e['id'] for e in summary_2]

    return summary_indexes_1, summary_indexes_2


def make_summary_side_contrastive(source, contr_rank):
    summary = []

    count_words = 0

    desired_opinions = contr_rank

    q_desired_opinions = list(desired_opinions)

    # Send low priority aspects to end of queue
    for candidate_sentence in reversed(range(len(q_desired_opinions))):
        if q_desired_opinions[candidate_sentence][0] in LOW_PRIORITY_ASPECTS:
            e = q_desired_opinions[candidate_sentence]
            del q_desired_opinions[candidate_sentence]
            q_desired_opinions.append(e)

    while count_words < LIM_WORDS:

        if q_desired_opinions == []:  # No more opinions found.
            break

        desired_opinion = q_desired_opinions.pop(0)  # Gets first element of queue.

        desired_aspect = desired_opinion[0]
        desired_polarity = desired_opinion[1]

        possible_sentences = []  # Will save all sentences which are desired to be included in the summary at this step.

        for candidate_sentence in source:

            if desired_aspect not in source[candidate_sentence]['sent']:
                continue  # Candidate doesn't have the aspect that the algorithm is lookink for.

            if source[candidate_sentence]['sent'][desired_aspect] * desired_polarity <= 0:
                continue  # Candidate doesn't have the polarity that the algorithm is lookink for.

            if source[candidate_sentence] in summary:
                continue  # Candidate is already in the summary

            if count_words + source[candidate_sentence]['word_count'] <= LIM_WORDS:  # Check if candidate will exceed the limit of words of the summary.
                possible_sentences.append(source[candidate_sentence])

        # Find the length of candidate sentences which is closest to the defined ideal length.
        best_length_diff = INFINITY
        if SENTENCE_IDEAL_LENGTH != None:
            for s in possible_sentences:
                best_length_diff = min(best_length_diff, abs(SENTENCE_IDEAL_LENGTH - len(s['words'])))

        random.shuffle(possible_sentences)

        for s in possible_sentences:

            # Will pick the first sentence in `possible_sentences` that has the closest length to the ideal length.
            if SENTENCE_IDEAL_LENGTH == None or abs(SENTENCE_IDEAL_LENGTH - len(s['words'])) == best_length_diff:

                summary.append(s)

                count_words += s['word_count']

                s_opinions = []

                for desired_aspect in s['sent']:
                    s_opinions.append((desired_aspect, trinary_polarity(s['sent'][desired_aspect])))

                # Opinions covered in the selected sentence go to the end of queue
                for e in s_opinions:
                    if e in desired_opinions:
                        if e in q_desired_opinions:
                            q_desired_opinions.remove(e)
                        q_desired_opinions.append(e)

                break  # Stops after one sentence is chosen.

    return summary


def make_summary_side_contrastive_and_representative(source, repr_rank, contr_rank):
    summary = []

    count_words = 0

    q_contr = [i for i in contr_rank if i[1] != 0]  # Queue that considers contrastivity.
    q_repr = [i for i in repr_rank if i[1] != 0]  # Queue that considers representativity.

    # Send low priority aspects to end of queue
    for Q in [q_contr, q_repr]:
        for candidate_sentence in reversed(range(len(Q))):
            if Q[candidate_sentence][0] in LOW_PRIORITY_ASPECTS:
                e = Q[candidate_sentence]
                del Q[candidate_sentence]
                Q.append(e)

    turn = 0  # Keeps track of which queue will choose the next opinion.

    while count_words < LIM_WORDS:

        if q_contr == [] and q_repr == []:  # No more opinions found.
            break

        if turn % 2 == 0:
            q_turn = q_contr
        if turn % 2 == 1:
            q_turn = q_repr

        turn += 1

        if q_turn == []:
            continue

        desired_opinion = q_turn[0]  # Gets first element of queue.

        desired_aspect = desired_opinion[0]
        desired_polarity = desired_opinion[1]

        possible_sentences = []  # Will save all sentences which are desired to be included in the summary at this step.

        for candidate_sentence in source:

            if desired_aspect not in source[candidate_sentence]['sent']:
                continue  # Candidate doesn't have the aspect that the algorithm is lookink for.

            if source[candidate_sentence]['sent'][desired_aspect] * desired_polarity <= 0:
                continue  # Candidate doesn't have the polarity that the algorithm is lookink for.

            if source[candidate_sentence] in summary:
                continue  # Candidate is already in the summary

            if count_words + source[candidate_sentence]['word_count'] <= LIM_WORDS:  # Check if candidate will exceed the limit of words of the summary.
                possible_sentences.append(source[candidate_sentence])

        if len(possible_sentences) == 0:  # No more sentences for this opinions
            del q_turn[0]

        # Find the length of candidate sentences which is closest to the defined ideal length.
        best_length_diff = INFINITY
        if SENTENCE_IDEAL_LENGTH != None:
            for s in possible_sentences:
                best_length_diff = min(best_length_diff, abs(SENTENCE_IDEAL_LENGTH - len(s['words'])))

        random.shuffle(possible_sentences)

        for s in possible_sentences:

            # Will pick the first sentence in `possible_sentences` that has the closest length to the ideal length.
            if SENTENCE_IDEAL_LENGTH == None or abs(SENTENCE_IDEAL_LENGTH - len(s['words'])) == best_length_diff:

                summary.append(s)

                count_words += s['word_count']

                s_opinions = []

                for desired_aspect in s['sent']:
                    s_opinions.append((desired_aspect, trinary_polarity(s['sent'][desired_aspect])))

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

                break  # Stops after one sentence is chosen.

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

    # Remove sentences until the summary size respects the limit of words.
    while struct.count_words(summary_1) > LIM_WORDS and len(summary_indexes_1) > 0:
        summary_indexes_1 = summary_indexes_1[:-1]
        summary_1 = struct.get_summary_from_indexes(source_1, summary_indexes_1)
    while struct.count_words(summary_2) > LIM_WORDS and len(summary_indexes_2) > 0:
        summary_indexes_2 = summary_indexes_2[:-1]
        summary_2 = struct.get_summary_from_indexes(source_2, summary_indexes_2)

    return summary_indexes_1, summary_indexes_2
