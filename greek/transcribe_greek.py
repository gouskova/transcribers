#!/usr/bin/env python3
# coding: utf-8

'''
slight modifications to the file from Schott's wordlist for greek (Ralf's dictionaries) to make it usable in UCLAPL research

also, some utilities for converting greek orthography into 
'''

import re


def writefeats(inset, outpath):
    outlist = []
    for wd in inset:
        segs = wd.split(' ')
        for seg in segs:
            if not seg in outlist:
                outlist.append(seg)
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sorted(outlist)))

def get_letters(inpath):
    outlist = set()
    with open(inpath, 'r', encoding='utf-8') as f:
        for line in f:
            word = set(line.strip('\n').lower())
            outlist=word|outlist
    with open('transcription_key.txt', 'w', encoding='utf-8') as out:
        out.write('\n'.join(sorted(list(outlist))))
    print("done collecting letters")


def spacify(inpath):
    '''
    returns a list of words 
    '''
    out = set() 
    with open(inpath, 'r', encoding='utf-8') as f:
        for line in f:
            wd = ' '.join(list(line.rstrip('\n')))
            wd = wd.replace("ʎ ʎ", "ʎ") #mistake in the orig transcription file 
            wd = wd.replace('ɪ', 'i')
            wd = wd.replace("ŋ g", "g")
            out.add(wd)
    return out


def writeld(inset, outpath):
    with open(outpath, 'w', encoding='utf-8') as f:
        for wd in sorted(inset):
            f.write(wd+'\n')


def get_key(inpath):
    out = {}
    with open(inpath, 'r', encoding='utf-8') as f:
        for line in f:
            segs = line.strip().split('\t')
            out[segs[0]] = segs[1]
    return out


def transcribe(word, digraphs, unis):
    for seg in word:
        word = ''.join([digraphs[seq] if seq in digraphs else seq for seq in word])
        word = ' '.join([unis[seg] if seg in unis else seg for seg in word])
    return word


def transcribe_words(inpath, outpath):
    digraphs = get_key('digraphs.txt')
    unis = get_key('transcription_key.txt')
    with open(inpath, 'r', encoding='utf-8') as f:
        with open(outpath, 'w', encoding='utf-8') as out:
            for line in f:
                word = line.strip().split(' ')[0].lower()
                word = word.rstrip('/fnbced')
                word = transcribe(word, digraphs, unis)
                out.write(word+'\n')
    print('done writing ld')


def cheat(ralfpath, crubapath, outpath):
    out = {}
    with open(ralfpath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n').split('\t')
            wd = line[0]
            trans = ' '.join(list(line[1]))
            trans = trans.replace("ʎ ʎ", "ʎ") #mistake in the orig transcription file 
            trans = trans.replace('ɪ', 'i')
            trans = trans.replace("ŋ g", "g")
            out[wd] = trans
    with open(crubapath, 'r', encoding='utf-8') as f:
        with open(outpath, 'w', encoding='utf-8') as outf:
            for line in f:
                wd = line.rstrip('\n').split(' ')[0]
                if wd in out:
                    outf.write(out[wd]+'\n')
                else:
                    print(wd)



if __name__=='__main__':
    import sys
    if 'ralf' in sys.argv:
        inpath = 'greek-dictionary.txt'
        x = spacify(inpath)
        writeld(x, 'LearningData.txt')
        writefeats(x, 'Features.txt')
    elif 'sourceforge_greek.txt' in sys.argv:
        get_letters('sourceforge_greek.txt')
    elif 'crubadan' in sys.argv:
        #transcribe_words('greek_an_crubadan.txt', 'LearningData_crub.txt')
        cheat('greek-dictionary_orig.txt', 'greek_an_crubadan.txt', 'LearningData_crub.txt')
