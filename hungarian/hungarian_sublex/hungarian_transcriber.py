#!/usr/bin/env python3
# coding: utf-8

'''
custom module for converting the hungarian data file from sublexical.phonologist.org into IPA. that data file has a mix of phonology and orthography
'''
import re

def transkey():
    tkey= {}
    with open('transkey.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for x in range(1, len(lines)+1):
            tkey[x] = lines[x-1].strip().split('\t')
    return tkey


def transcribe_wd(word, tkey):
    for x in sorted(tkey):
        word = word.replace(tkey[x][0], tkey[x][1])
    #s rules
    word = word.replace('s ', 'ʃ ')
    word = re.sub('s$', 'ʃ', word)
    word = word.replace('sz', 's')
    word = word.replace('c', 't s')
    word = word.replace('ty', 'c')
    return word


def transcribe_wds(inpath, outpath, tkey):
    with open(inpath, 'r', encoding='utf-8') as f:
        with open(outpath, 'w', encoding='utf-8') as out:
            for line in f:
                out.write(transcribe_wd(line.strip(), tkey)+'\n')
    print('Done')
                


if __name__=='__main__':
    tkey = transkey()
    inpath = 'training.txt'
    outpath = 'LearningData_nouns.txt'
    transcribe_wds(inpath, outpath, tkey)
