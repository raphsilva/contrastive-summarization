import math


def show_summary(set1, set2, contrastive_pairs, part, PAR_SHOW='plain'):
    if PAR_SHOW == 'false':
        return

    if part == 1:
        header1 = '[+]'
        header2 = '[-]'
        print('\n\n')
    if part == 2:
        header1 = '[-]'
        header2 = '[+]'

    if PAR_SHOW == 'plain':
        show_summary_plain(set1, set2, contrastive_pairs)
    if PAR_SHOW == 'table' or PAR_SHOW == 'true':
        show_summary_table(set1, set2, contrastive_pairs, header1, header2)


def show_summary_plain(set1, set2, contrastive_pairs):
    """
    Function that exhibits the summary in form of a table with two columns: positive sentences and negative sentences.
    :param cell_length: [int] indicates how many characters will be in each cell at most.
    :return: none.
    """

    print('--------------')

    for (i1, i2) in contrastive_pairs:
        sentence1 = "%2d|" % (i1) + set1[i1]['sentence']
        sentence2 = "%2d|" % (i2) + set2[i2]['sentence']

        print("%s|%s" % (sentence1, sentence2), end="\n")


def show_summary_table(set1, set2, contrastive_pairs, header1='T1', header2='T2', cell_length=40):
    """
    Function that exhibits the summary in form of a table with two columns: positive sentences and negative sentences.
    :param cell_length: [int] indicates how many characters will be in each cell at most.
    :return: none.
    """

    column_headers = [header1, header2]

    header_line = " " + ("-" * cell_length) + " " + ("-" * cell_length) + " "

    header = ""
    header += header_line
    header += '\n'
    header += "|" + (' ' * ((cell_length - len(column_headers[0])) // 2)) + \
              column_headers[0] + (
                      ' ' * int(math.ceil(((cell_length - len(column_headers[0])) / 2))))
    header += "|" + (' ' * ((cell_length - len(column_headers[1])) // 2)) + \
              column_headers[1] + (
                      ' ' * int(math.ceil(((cell_length - len(column_headers[1])) / 2)))) + "|"
    header += '\n'
    header += header_line

    print(header)

    for (i1, i2) in contrastive_pairs:
        sentence1 = set1[i1]['sentence']
        sentence2 = set2[i2]['sentence']
        pos_idx = 0
        neg_idx = 0

        while pos_idx < len(sentence1) or neg_idx < len(sentence2):
            print("|", end="")

            coln = 0
            while pos_idx < len(sentence1) and coln < cell_length:

                # Break line
                next_space = sentence1[pos_idx:].find(' ')
                if next_space < 0:  # If there isn't another space, the next word is the last one.
                    next_space = len(sentence1[pos_idx:])  # The entire rest of the string must fit in the line.
                if next_space >= cell_length:  # If the word is larger than the column, it'll have to break in the middle.
                    pass
                elif next_space >= cell_length - coln:
                    break

                # Don't print space at the beginning of line
                if coln == 0 and sentence1[pos_idx] == ' ':
                    pos_idx += 1
                    continue

                print(sentence1[pos_idx], end="")
                pos_idx += 1
                coln += 1

            while coln < cell_length:
                print(" ", end="")
                coln += 1

            print("|", end="")

            coln = 0
            while neg_idx < len(sentence2) and coln < cell_length:

                # Break line
                next_space = sentence2[neg_idx:].find(' ')
                if next_space < 0:  # If there isn't another space, the next word is the last one.
                    next_space = len(sentence2[neg_idx:])  # The entire rest of the string must fit in the line.
                if next_space >= cell_length:  # If the word is larger than the column, it'll have to break in the middle.
                    pass
                elif next_space >= cell_length - coln:
                    break

                # Don't print space at the beginning of line
                if coln == 0 and sentence2[neg_idx] == ' ':
                    neg_idx += 1
                    continue

                print(sentence2[neg_idx], end="")
                neg_idx += 1
                coln += 1

            while coln < cell_length:
                print(" ", end="")
                coln += 1

            print("|")

        print(header_line)
