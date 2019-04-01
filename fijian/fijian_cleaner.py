#! /usr/bin/env python3
# -*- coding:utf-8 -*-

'''
cleans the an crubadan corpus for fijian a bit.

all consonant-final words are removed.
all words with 'h' are removed.

then english words are identified by intersecting list with Celex.

hyphens, hashtags, ampersands removed. spaces added.
'''


import os,sys, itertools

basepath = os.path.dirname(os.getcwd())

celex = os.path.join(basepath, 'shona', 'shona_wd_corpus', 'celex_word_freq.txt')


english = []

with open(celex, 'r', encoding='utf-8') as f:
    for line in f:
        word = line.split('\\')[1]
        english.append(word.lower())
    english = set([x for x in english if len(x)>2 and not "'" in x])


fiji_raw = []
fiji_cons = ['n', 's', 'k', 'm', 'r', 'v', 'y', 'g', 'd', 't', 'q', 'l', 'j', 'w', 'c', 'b', 'f', 'h', 'p', "'"]

clusters = [''.join(x) for x in itertools.product(fiji_cons, repeat=2)]
clusters.remove('dr')
print(clusters)

with open(os.path.join(basepath, 'fijian', 'fj-words.txt'), 'r', encoding='utf-8') as f:
    for line in f:
        cluster = False
        word = line.strip().split(' ')[0].lower().strip('@#')
        for clust in clusters:
            if clust in word:
                cluster = True 
        if (not cluster) and (not word=='') and (not 'h' in word) and (word[-1] in ['a','e','i','o','u']):
            fiji_raw.append(word)
    fiji_raw = set(fiji_raw)



print(len(english & fiji_raw))
fijian = fiji_raw - english

print(len(fijian))

with open(os.path.join(basepath, 'fijian', 'fijian_crubadan.txt'), 'w', encoding='utf-8') as f:
    for word in sorted(list(fijian)):
        f.write(' '.join(list(word.replace('-','')))+ '\n')



