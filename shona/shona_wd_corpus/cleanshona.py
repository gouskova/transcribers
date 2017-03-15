#!usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import itertools

workdir = os.getcwd()

files = [x for x in os.listdir(workdir) if x.startswith('shona')]

shonadic=[]

for file in files:
    wlist = open(file, 'r', encoding= 'utf-8')
    for line in wlist:
        line=line.strip('\n').split(' ')
        for word in line:
            word = word.strip('^,.!?:;').lower()
            if word.isalpha() and not word in shonadic:
                shonadic.append(word)
    wlist.close()


shonasegs = []
feats = open('/home/maria/git/phonotactics/data/shona/verbs_chimhundu_ext_segs/Features.txt', 'r', encoding='utf-8')
shonafeats =feats.readlines()[1:]
for line in shonafeats:
    seg = line.split('\t')[0]
    shonasegs.append(seg)
feats.close()


#filtering out the non-shona words, hopefully
vowels = ['i', 'e', 'a', 'o', 'u']

consonants = [x for x in shonasegs if not x in vowels]
shonadigraphs=['m h','n h','d h','b h','v h', 'c h','s h','p f','s v','z h','z v','b v','n y','d z','d y','t y', 't s']

clusters = [a+' '+ b for (a,b) in list(itertools.product(consonants, repeat=2))]

outfile = open("LearningData.txt", 'w', encoding='utf-8')
orthofile = open("shona_wds_ortho_key.txt", 'w', encoding='utf-8')

def spacify(wordlist):
    trandic = {}
    attcl = []
    for word in sorted(wordlist):
        if "x" in word or "q" in word:
            continue
        else:
            orthoword = word
            word = word.replace("-", "")
            word = word.replace("\s", "") #spaces left from removing hyphens
            word = word.replace("n'", "N")
            word = word.replace("ng", "Ng")
            word = word.replace(" ", "")
            for seg in word:
                word = word.replace(seg, seg+" ").strip()
                word = word.replace("  ", " ")
            for digraph in shonadigraphs:
                word = word.replace(digraph, digraph.replace(" ",""))
                word = word.replace("ts v", 'tsv')
                word = word.replace("dz v", 'dzv')
                word = word.replace("  ", " ")
            #trying to find non-shona words by tracking clusters
            trandic[orthoword]={'transcription':'', 'consclusters':[]}
            trandic[orthoword]['transcription'] = word
            for cl in clusters:
                if cl in word:
                    trandic[orthoword]['consclusters'].append(cl)
                    if not cl in attcl:
                        attcl.append(cl)
                else:
                    trandic[orthoword]['consclusters']=[]
    return (trandic,clusters)


shonawds = spacify(shonadic)[0]	

#print(len(shonawds))

#print(spacify(shonadic)[1])


for orthoword in sorted(shonawds.keys()):
    orthofile.write(orthoword + '\t' + shonawds[orthoword]['transcription'] +'\t' + ','.join(shonawds[orthoword]['consclusters'])+'\n')
    outfile.write(shonawds[orthoword]['transcription']+'\n')

outfile.close()
orthofile.close()
