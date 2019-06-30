#!/usr/bin/env python3
# coding: utf-8

'''
slight modifications to the file from Schott's wordlist for greek (Ralf's dictionaries) to make it usable in UCLAPL research

also, some utilities for converting greek orthography into IPA
'''

import re, os


def writefeats(inset, outpath):
    '''
    makes a skeleton of a Features.txt file (one IPA character per line)
    '''
    outlist = []
    for wd in inset:
        segs = wd.split(' ')
        for seg in segs:
            if not seg in outlist:
                outlist.append(seg)
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sorted(outlist)))

def get_letters(inpath):
    '''
    finds all the letters in the word list that will need to be converted to IPA
    '''
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
    opens inpath, returns a giant list of words with spaces between chars 
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
    '''
    takes giant list of words and writes it to outpath
    '''
    with open(outpath, 'w', encoding='utf-8') as f:
        for wd in sorted(inset):
            f.write(wd+'\n')


def get_key(inpath):
    '''
    reads in transcription key
    '''
    with open(inpath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        out = {}.fromkeys(range(1,len(lines)+1))
        for k in out:
            line = lines[k-1].strip('\n').split('\t')
            out[k] = [line[0], line[1]]
    return out


def transcribe(word, tkey):
    '''
    "word" is a string
    'transkey' = is a dictionary of ordered substitions
    '''
    word = ' '.join(list(word.lower()))
    for k in tkey:
        word = word.replace(tkey[k][0], tkey[k][1]) 
    return word


def transcribe_words(inpath, outpath):
    tkey = get_key('transcription_key.txt')
    with open(inpath, 'r', encoding='utf-8') as f:
        with open(outpath, 'w', encoding='utf-8') as out:
            for line in f:
                word = line.strip().split(' ')[0].lower()
                word = word.rstrip('/fnbced')
                word = transcribe(word, tkey)
                out.write(word+'\n')
    print('done writing ld')


def reveng():
    '''
    tests my transcriptions against ralf/schott
    '''
    ralf = 'greek-dictionary_orig.txt'
    tkey = get_key('transcription_key.txt') 
    with open(ralf, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n').split('\t')
            wd = line[0]
            trans = ' '.join(list(line[1]))
            mytrans = transcribe(wd, tkey)
            if trans == mytrans:
                continue
            else:
                print(trans + '\t' + mytrans)
                continue

def cheat(ralfpath, crubapath, outpath):
    '''
    plucks all the words in an crubadan that are also in ralf/schott,  and writes them to LearningData.txt
    '''
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


def cmg(inpath, ortho=False):
    tkey = get_key('transcription_key.txt')
    with open(inpath, 'r', encoding='utf-8') as f:
        with open('LearningData_cmg.txt', 'w', encoding='utf-8') as out:
            for line in f:
                if line.startswith(' lex:'):
                    word = line.split(':')[1].strip()
                    if '/' in word:
                        word = word.split('/')[0].strip()
                    if ortho:
                        out.write(transcribe(word, tkey) + '\t' + word+ '\n')
                    else:
                        out.write(transcribe(word, tkey)+'\n')
    print("done")



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
    elif 'cmg' in sys.argv:
        cmg(os.path.expanduser('~/Dropbox/work/dictionaries/greek/greek_lexemes.txt'), ortho=True)
