import math



def generic(s):
    
    r = 0
    l = []
    
    count = {}
    for i in s:
        if i not in count:
            count[i] = 0
        count[i] += 1
    
    for i in s:
        a = pow(ord(i)/pow(count[i],0.5),2)
        b = a*((len(l)%10)+1)
        c = b*(len(l)%(int(len(s)/20)+20)+1)
        l.append(c%1000)

    for i in l:
        r += i
    for i in count:
        r += pow(count[i],1+1/ord(i))
    r /= pow(len(l), 1/2)

    return r
        
        
        
def summaryIDs(pairs):    
    r = 0
    for i,j in pairs:
        i = 2*pow(i, 0.75) + 10 + 2*(i%10)
        j = 2*pow(j, 0.75) + 10 + 2*(j%10)
        r += (1000*(pow(i,2)/pow(j,2)))
        r += 100*math.log2(i*j)
        r += 10*pow(i,0.5)
        r += 10*pow(j,0.5)
    
    r /= pow(len(pairs), 0.9)
    
    return r



def word(w):
    r = 0
    for i in range(len(w)):
        a = pow(50+ord(w[i]),4/5)/pow(i+3,1/3)
        r += a
    r /= pow(2+len(w), 1/6)
    
    return r
        
        

def sentence(s):
    chars = {}
    words = {}
    for i in s:
        if i not in chars:
            chars[i] = 0
        chars[i] += 1
    w = s.lower().split()
    for i in w:
        if i not in words:
            words[i] = 0
        words[i] += 1
    
    r = 0
    for i in chars: 
        r += pow(50+ord(i), 1/4) * pow(5+chars[i], 1/4)

    for i in range(len(w)-1):
        h1 = word(w[i])
        h2 = word(w[i+1])
        a = pow(1 + h1*words[w[i]] + h2*words[w[i+1]], 3/4)
        r += a
    
    r /= pow(6+len(s), 1/4)
    
    return r
    


def summary(summ):
    r = 0
    for u, v in summ:
                
        a = sentence(u['sentence'])
        b = sentence(u['sentence'])
        
        a = 2*pow(a, 0.75) + 10 + 2*(a%10)
        b = 2*pow(b, 0.75) + 10 + 2*(b%10)
        r += (1000*(pow(a,2)/pow(b,2)))
        r += 100*math.log2(a*b)
        r += 10*pow(a,0.5)
        r += 10*pow(b,0.5)
    
    r /= pow(1+len(summ), 0.8)
    
    return r
