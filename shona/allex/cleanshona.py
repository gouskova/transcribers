#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import itertools

workdir = os.getcwd()

files = [x for x in os.listdir(workdir) if x.startswith('shona')]

#collect all words into a list

vowels = ['i', 'e', 'a', 'o', 'u'] #looked at the corpus manually, all non-vowel-final words are English
shonadic={}

for x in files:
    wlist = open(x, 'r', encoding= 'utf-8')
    for line in wlist:
        word=line.strip().split(' ')[1].lower()
        finalseg = list(word)[-1]
#        if (not word in shonadic) and (finalseg in vowels):
        if 'q' in list(word):
                shonadic[word] = 'bad'
        elif finalseg in vowels:
                shonadic[word] = 'good'
        else:
                shonadic[word] = 'bad'
    wlist.close()
    
f = sorted([x for x in shonadic if shonadic[x] == 'bad'])
probfile = open('prob_loans.txt', 'w', encoding='utf-8')
for x in f:
    probfile.write(x+'\n')
probfile.close()

shonadic = [x for x in shonadic if shonadic[x]=='good']

print('length of shonadic ')
print(len(shonadic))


#obtain a list of shona segments that can be defined using our features

shonasegs = []
feats = open('/home/maria/git/phonotactics/data/shona/verbs/Features.txt', 'r', encoding='utf-8')
f =feats.readlines()[1:]
for line in f:
    seg = line.split('\t')[0]
    shonasegs.append(seg)
feats.close()

celex = open('/home/maria/git/transcribers/shona/shona_wd_corpus/celex_word_freq.txt', 'r', encoding='utf-8')
f = []
for line in celex:
    word = line.split('\\')[1]
    if not word in f:
        f.append(word.lower())
celex.close()

shonadic = list(sorted(set(shonadic)-set(f))) 

consonants = [x for x in shonasegs if not x in vowels]

shonadigraphs=['m h','n h','d h','b h','v h', 'c h','s h','p f','s v','z v','z h','b v','n y','d z','d y','t y', 't s']

#clusters = [a+' '+ b for (a,b) in list(itertools.product(consonants, repeat=2))]
#print('all 2-way combinations of consonants')
#print(len(clusters))


#these were identified with the help of git/phonotactics/code/datachecker.py, using extended Features.txt on prelim output of this very script

#garbagesegs = ['č','ɔ','è','ę','í','ɲ','ə','zvh','ɪ','ā','ː','ɛ','ĉ','β','ó','ŭ','é','ˌ','ō','ê','á','ī','ç','c','ɑ','ớ','ö','l','ú','ū','î','ḥ','â','ô','ŋ','ʊ','ì','à','å','ñ','ï','ë','ý','ă','ü','ã','tsh','ɾ','ž','ǔ','ʻ','ṅ','ð','ṃ','ł','ä','ɓ','š','ɡ', 'q']



#now break up every word into spaces according to the existing list of segs 

def spacify(wordlist, garbsave):
    '''
    takes in a raw word list, one word per line
    outputs something close to UCLAPL LearningData.txt--a dictionary of word and transcription pairs, where transcriptions are files separated by spaces
    '''
    trandic = {}
#    garbsegs = set(garbagesegs)
    for word in sorted(wordlist):
        orthoword=word
#        trandic[orthoword]={'transcription':'', 'garbage':len(set(word)&garbsegs)>0}
        trandic[orthoword]={'transcription':'', 'garbage':False}
        word = word.replace("-", "")
        word = word.replace("n'", "N")
        word = word.replace("ng", "Ng")
        word = word.replace(" ", "")
        for seg in word:
            word = word.replace(seg, seg+" ").strip()
        for digraph in shonadigraphs:
            word = word.replace(digraph, digraph.replace(" ",""))
        word = word.replace("ts v", 'tsv') #the two trigraphs
        word = word.replace("dz v", 'dzv')
        word = word.replace("zvh", "zv h")
        trandic[orthoword]['transcription']=word
    return sorted([trandic[x]['transcription'] for x in trandic])


def find_shona_clusters(wlist):
    '''
    assuming that any legal consonant sequences will also occur in nouns and verb stems listed in Chimhundu (that is, no local phonotactic exceptions in morphologically derived environments). none of the sources indicate that this assumption could be problematic

    '''
    clist = {}.fromkeys(clusters, False)
    for cl in clist:
        if clist[cl]==False:
            for wd in wlist:
                if cl in wd:
                    clist[cl]=True
    return sorted(list(set([x for x in clist if clist[x]==True])))



print('length before spacify: '+ str(len(shonadic)))
shonawds = spacify(shonadic, garbsave=False)
print('length after spacify: ' + str(len(shonawds)))

def rm_nonnat_clusters(wdic):
    nativelist = {}.fromkeys(wdic, True) #'keep' is True unless a cluster is found
    unattcl = []
    for wd in nativelist:
        if nativelist[wd]==True:
            for cl in unattcl:
                if cl in wd:
                    nativelist[wd]=False
    print('length of removed list')
    print(len([wd for wd in nativelist if nativelist[wd]==False]))
    return sorted([wd for wd in nativelist if nativelist[wd]==True])



print(shonasegs)

#for wd in shonawds:
#    w = wd.split(' ')
#    keep = True
#    for seg in w:
#        if seg not in shonasegs:
#            keep = False    
#    if not keep:
#        shonawds.remove(wd)



outfile = open("LearningData.txt", 'w', encoding='utf-8')
for wd in shonawds:
    outfile.write(wd+'\n')

outfile.close()



