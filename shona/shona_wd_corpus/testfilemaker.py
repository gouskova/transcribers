#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import os
import itertools
import random

workdir = os.getcwd()

'''
read in all the segments from the full features file
'''

def get_shona_segs(cv='all'):
    shonasegs = []
    feats = open('/home/maria/git/phonotactics/data/shona/verbs_chimhundu_ext_segs/Features.txt', 'r', encoding='utf-8')
    shonafeats =feats.readlines()[1:]
    for line in shonafeats:
        seg = line.split('\t')[0]
        shonasegs.append(seg)
    feats.close()
    vowels = ['a','e','i','o','u']
    if cv=='consonants':
        return list(set(shonasegs) - set(vowels))
    if cv=='all':
        return shonasegs

'''
make some harmonic and disharmonic vowel combos
'''

def make_vowel_pairs(pairtype):
    vowels = ['i', 'e', 'a', 'o', 'u']
    highV = ['i','u']
    midV = ['e','o']
    vcombos = [a + b for (a,b) in (list(itertools.product(vowels, repeat=2)))] 
    disharmcombos = [('a','e'), ('a','o'), ('o','i'), ('e','i'), ('u','e'),('i','o'), ('i','e'), ('u','o')]
    harmcombos = list(set(vcombos)-set(disharmcombos))
    if pairtype=="harmonic":
        return harmcombos
    if pairtype == 'disharmonic':
        return disharmcombos



'''
make some attested and unattested consonant clusters
'''

def make_consonant_clusters():
    shonasegs = get_shona_segs(cv='all')    
    consonants = get_shona_segs(cv='consonants')
    clusters = [a+' '+ b for (a,b) in list(itertools.product(consonants, repeat=2))]
    return clusters

def find_shona_clusters(wlist):
    '''
    assuming that any legal consonant sequences will also occur in nouns and verb stems listed in Chimhundu (that is, no local phonotactic exceptions in morphologically derived environments). none of the sources indicate that this assumption could be problematic

    '''
    clusters = make_consonant_clusters()
    clist = {}.fromkeys(clusters, False)
    for cl in clist:
        if clist[cl]==False:
            for wd in wlist:
                if cl in wd:
                    clist[cl]=True
    return sorted(list(set([x for x in clist if clist[x]==True])))


def make_leg_illeg_clusters(clustype):
    chimhundu = open(workdir+'/chimhundu.txt', 'r', encoding='utf-8')
    cleanwds = [x.strip('\n') for x in chimhundu.readlines()]
    clusters = make_consonant_clusters()
    attested = find_shona_clusters(cleanwds)
    chimhundu.close()
    unattested = [x for x in clusters if not x in attested]
    if clustype=='attested':
        return attested
    if clustype=='unattested':
        return unattested
        

def syllable(ctype, consonants, attclusters, unattclusters):
    vowels = ['a','e','i','o','u']
#    consonants=get_shona_segs(cv='consonants')
#    attclusters = make_leg_illeg_clusters('attested')
#    unattclusters = make_leg_illeg_clusters('unattested')
    words = {'word':'', 'vowels':'', 'consonants':''}
    if ctype=='singleton':
        syll=(random.choice(consonants)+ ' ' + random.choice(vowels), 'singleton')
    cslot = random.choice(["c", "cc"])
    if cslot=='c' and ctype == 'attested':
        syll=(random.choice(consonants)+ ' ' + random.choice(vowels), 'attested')
    if cslot =='cc' and ctype =='attested':
        syll=(random.choice(attclusters)+ ' ' + random.choice(vowels), 'attested')
    if cslot == 'cc' and ctype =='unattested':
        syll=(random.choice(unattclusters)+ ' ' + random.choice(vowels), 'unattested')
    if cslot=='c' and ctype=="unattested":
        syll=(random.choice(consonants)+' ' + random.choice(vowels), 'unattested')
    return syll

def make_words(maxwdlength, nwords, ctype):
    consonants = get_shona_segs(cv='consonants')
    attclusters = make_leg_illeg_clusters('attested')
    unattclusters = make_leg_illeg_clusters('unattested')
    disharmcombos = make_vowel_pairs('disharmonic')
    wds = {}
    while len(wds)<=nwords:
        wdlength = random.choice(range(1,maxwdlength+1))
        wd = []
        for _ in itertools.repeat(None, wdlength):
            syll = syllable(ctype, consonants, attclusters, unattclusters)
            wd.append(syll[0])
        wds[' '.join(wd)]={'vowels':'harmonic', 'consonants':ctype}
        for wd in wds:
            if wds[wd]['vowels'] !='disharmonic':
                vlist = ''.join([x for x in wd if x in ['a','e','i','o','u']])
                for pair in disharmcombos:
                    pair = ''.join(pair)
                    if pair in vlist:
                        wds[wd]['vowels']='disharmonic'

    return wds


def write_testfile(dics, outpath):
    outfile=open(outpath, 'w', encoding='utf-8')
    for dic in dics:
        for wd in dic:
            outfile.write("%s\t%s_%s\n" % (wd, dic[wd]['vowels'],dic[wd]['consonants']))
    outfile.close()


words1 = make_words(4, 5000, 'attested')
words2 = make_words(4, 5000, 'unattested')
words3 = make_words(4, 5000, 'singleton')

write_testfile([words3, words1, words2], '/home/maria/Desktop/TestingData.txt')
