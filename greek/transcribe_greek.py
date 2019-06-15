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


def transcribe_greek_ortho(word, transkey, digraphkey):
    '''
    strip /f, /n 
    '''
    word = word.rstrip('/fnbced')
    for seg in word:
        pass

if __name__=='__main__':
    import sys
    if 'ralf' in sys.argv:
        inpath = 'greek-dictionary.txt'
        x = spacify(inpath)
        writeld(x, 'LearningData.txt')
        writefeats(x, 'Features.txt')
    elif 'sourceforge_greek.txt' in sys.argv:
        get_letters('sourceforge_greek.txt')
