from language import removeNegsAndAdjs


# in order to gain efficiency timewise, if a ϕ or ψ is calculated, it's stored
# so it wouldn't be necessary to calculate it again
cache_phi = {}
cache_psi = {}


def omega(u, v):
    """
    Term Similarity Function (ω) of two words.
    :param u: [str] word to be compared.
    :param v: [str] word to be compared.
    :return: [float] value in range [0, 1].
    """
    
    # using Word Overlap
    if u == v:
        return 1
    else:
        return 0







def phi(text_info_1, text_info_2):
    global cache_phi
    """
    Given two opinionated sentences with the same polarity, the content similarity function φ(s1,s2) ∈ [0,1] measures the overall content similarity of s1 and s2.
    """
    
    if len(text_info_1) * len(text_info_2) == 0:
        return 0
    
    idx = str(text_info_1)+'::'+str(text_info_2)
    

    # if ϕ(sentence1, sentence2) isn't calculated yet
    if idx not in cache_phi.keys():

        # implementing the formula from the article
        sum_sentence1 = 0.0
        for word1 in text_info_1:
            max_omega = 0.0
            for word2 in text_info_2:
                max_omega = max(max_omega, omega(word1, word2))
            sum_sentence1 += max_omega

        sum_sentence2 = 0.0
        for word2 in text_info_2:
            max_omega = 0.0
            for word1 in text_info_1:
                max_omega = max(max_omega, omega(word1, word2))
            sum_sentence2 += max_omega

        cache_phi[idx] = float(sum_sentence1 + sum_sentence2) / (len(text_info_1) + len(text_info_2))

    #print(text_info_1)
    #print(text_info_2)
    #print(cache_phi[idx])
    #print()
    #input()

    return cache_phi[idx]




def psi(text_info_1, text_info_2):
    """
    Given two opinionated sentences s1 and s2 with opposite polarities, the contrastive similarity function ψ(s1,s2) ∈ [0,1] measures the similarity of s1 and s2 excluding their difference in sentiment.
    """


    if len(text_info_1) * len(text_info_2) == 0:
        return 0
    
    text_info_1 = removeNegsAndAdjs(text_info_1)
    text_info_2 = removeNegsAndAdjs(text_info_2)
    
    idx = str(text_info_1)+'::'+str(text_info_2)
    
    r = phi(text_info_1, text_info_2)

    cache_psi[idx] = r

    return r


