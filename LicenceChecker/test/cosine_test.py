
def word2vec(word):
    from collections import Counter
    from math import sqrt

    # count the characters in word
    cw = Counter(word)
    # precomputes a set of the different characters
    sw = set(cw)
    # precomputes the "length" of the word vector
    lw = sqrt(sum(c*c for c in cw.values()))

    # return a tuple
    return cw, sw, lw

def cosdis(v1, v2):
    # which characters are common to the two words?
    common = v1[1].intersection(v2[1])
    # by definition of cosine distance we have
    return sum(v1[0][ch]*v2[0][ch] for ch in common)/v1[2]/v2[2]
    



a = 'safasfeqefscwaeeafweeaeawaw'
b = 'strdfadsdfdswdoptykop;lvhopijresokpghwji7'
c = 'optykop;lvhopijresokpghwji7' 
a = "AGPL"
b = "APACHE"
va = word2vec(a)
vb = word2vec(b)
vc = word2vec(c) 
print (cosdis(va,vb))