

def idx_to_summ(source, indexes):    
    s = {}
    c = 0
    for i in indexes:
        s[c] = dict(source[i])
        s[c]['id'] = i
        c += 1
    return s



def word_count(summ):
    r = 0
    for i in summ: 
        r += summ[i]['word_count']
    return r
