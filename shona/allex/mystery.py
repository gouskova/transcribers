#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import itertools

workdir = os.getcwd()
vowels = ['i', 'e', 'a', 'o', 'u'] #looked at the corpus manually, all non-vowel-final words are English

def findshonasegs():
    shonasegs = []
    feats = open('/home/maria/git/phonotactics/data/shona/verbs/Features.txt', 'r', encoding='utf-8')
    f =feats.readlines()[1:]
    for line in f:
        seg = line.split('\t')[0].strip()
        shonasegs.append(seg)
    feats.close()
    return shonasegs
 

consonants = [x for x in findshonasegs() if not x in vowels]
shonadigraphs=['m h','n h','d h','b h','v h', 'c h','s h','p f','s v','z v','z h','b v','n y','d z','d y','t y', 't s']

def rawshona():
    shonadic={}
    files = [x for x in os.listdir(workdir) if x.startswith('shona')]
    for x in files:
        wlist = open(x, 'r', encoding= 'utf-8')
        for line in wlist:
            word=line.strip().split(' ')[1].lower()
            finalseg = list(word)[-1]
            if finalseg in vowels:
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
    print('length of raw ALLEX Shona corpus ')
    print(len(shonadic))
    return shonadic

   
def intersectcelex(inlist):
    celex = open('/home/maria/git/transcribers/shona/shona_wd_corpus/celex_word_freq.txt', 'r', encoding='utf-8')
    f = []
    for line in celex:
        word = line.split('\\')[1]
        if not word in f:
            f.append(word.lower())
    celex.close()
    outlist = list(sorted(set(inlist)-set(f))) 
    return outlist


#now break up every word into spaces according to the existing list of segs 

def spacify(wordlist):
    '''
    takes in a raw word list, one word per line
    outputs something close to UCLAPL LearningData.txt--a dictionary of word and transcription pairs, where transcriptions are files separated by spaces
    '''
    trandic = {}
    print('length of shona wordlist before spacifying: ')
    print('\t' + str(len(trandic)))
    for word in sorted(wordlist):
        orthoword=word
        word = word.replace("-", "")
        word = word.replace("n'", "N")
        word = word.replace("ng", "Ng")
        word = word.replace(" ", "")
        word = ' '.join(list(word))
        for digraph in shonadigraphs:
            word = word.replace(digraph, digraph.replace(" ",""))
        word = word.replace("ts v", 'tsv') #there are only two trigraphs
        word = word.replace("dz v", 'dzv')
        word = word.replace('zvh', 'z vh')
        trandic[orthoword]=word
    print('length of shona wordlist after spacifying: ')
    print('\t' + str(len([trandic[x] for x in trandic])))
    return sorted([trandic[x] for x in trandic])


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




def rm_nonnat_clusters(wdic):
    '''
    input is a python dictionary of transcriptions; the value is whether to 'keep' the item (True/False)
    e.g. {'p a k a': False}
    '''
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


def removeforeignsegs(wdic):
    '''
    look through the list and see if anything in it doesn't match the feature file inventory. words like that get nixed
    '''
    segs = set(findshonasegs())
    outdic = []
    for word in wdic:
        wsegs = set(word.split(' '))
        if wsegs.issubset(segs): 
                outdic.append(word)
        else:
                continue
                #print(word)
    return outdic
                
def removescanerrors(wdic):
    outdic = []
    garb = []
    for word in wdic:
        if len(word)>20:
            print(word)
            garb.append(word)
        else:
            outdic.append(word)
    print(len(garb)
    return outdic

def writeoutfile(shonawds):
    outfile = open("LearningData.txt", 'w', encoding='utf-8')
    for wd in shonawds:
        outfile.write(wd+'\n')
    outfile.close()


def cleanshona():
    f = removescanerrors(removeforeignsegs(spacify(intersectcelex(rawshona()))))
    writeoutfile(f)
