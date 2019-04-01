#! /usr/bin/env python3
# *-* coding:utf-8 *-*

import os, sys

basepath = os.path.dirname(os.getcwd())
sys.path.append(basepath)

import generic_transcriber

ipadic = generic_transcriber.transc_table('fijian_ipa_key.txt')

digraphs = {'d i': 'n ʤ i', 'd r': 'n r', 't i': 'ʧ i'}


def transcribe_wd(word):
    word.replace("j", "ʧ") 
    for dig in digraphs:
        word = word.replace(dig, digraphs[dig])
    for let in ipadic:
        word = word.replace(let, ipadic[let])
    return word

def transcribe_corpus(infile, outfile):
    with open(infile, 'r', encoding='utf-8') as fi:
        with open(outfile, 'w', encoding='utf-8') as out:
            for line in fi:
                out.write(transcribe_wd(line))
    print('done')


if __name__=='__main__':
    if len(sys.argv)>1:
        infile = os.path.join(os.getcwd(), sys.argv[1])
        outfile = os.path.join(os.getcwd(), sys.argv[2])
    else:
        infile = os.path.join(os.getcwd(), "fijian_crubadan.txt")
        outfile = os.path.join(os.getcwd(), "LearningData.txt")
    transcribe_corpus(infile, outfile)

