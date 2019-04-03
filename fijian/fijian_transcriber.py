#! /usr/bin/env python3
# *-* coding:utf-8 *-*

import os, sys

basepath = os.path.dirname(os.getcwd())
sys.path.append(basepath)

import generic_transcriber

ipadic = generic_transcriber.transc_table('fijian_ipa_key.txt')

seg_digraphs = {'d i': 'nʤ i', 'd r': 'nr', 't i': 'ʧ i'}
#has affricates, prenasalized stops

clust_digraphs = {'d i': 'n d ʒ i', 'd r': 'n r', 't i': 't ʃ i'}
#has no complex segs

affr_digraphs = {'d i': 'n ʤ i', 'd r': 'n r', 't i': 'ʧ i'}
#has affricates but not prenasalized stops

def transcribe_seg(word):
    word = word.replace("j", "ʧ")
    for dig in seg_digraphs:
        word = word.replace(dig, seg_digraphs[dig])
    word = word.replace("b", "mb")
    word = word.replace("d", "nd")
    word = word.replace("q", "ŋɡ")
    for let in ipadic:
        word = word.replace(let, ipadic[let])
    return word


def transcribe_clust(word):
    word = word.replace("j", "t ʃ") 
    for dig in clust_digraphs:
        word = word.replace(dig, clust_digraphs[dig])
    word = word.replace("b", "m b")
    word = word.replace("q", "ŋ ɡ")
    word = word.replace("d", "n d")
    word = word.replace("n n", "n")
    for let in ipadic:
        word = word.replace(let, ipadic[let])
    return word



def transcribe_affr(word):
    word = word.replace("j", "ʧ")
    for dig in affr_digraphs:
        word = word.replace(dig, affr_digraphs[dig])
    word = word.replace("b", "m b")
    word = word.replace("d", "n d")
    word = word.replace("q", "ŋ ɡ")
    for let in ipadic:
        word = word.replace(let, ipadic[let])
    return word


def transcribe_wd(word, kind):
    if kind == 'seg':
        return transcribe_seg(word)
    if kind == 'clust':
        return transcribe_clust(word)
    if kind == 'affr':
        return transcribe_affr(word)


def transcribe_corpus(infile, outfile, kind):
    with open(infile, 'r', encoding='utf-8') as fi:
        with open(outfile, 'w', encoding='utf-8') as out:
            for line in fi:
                out.write(transcribe_wd(line, kind))
    print('done')


if __name__=='__main__':
    infile = os.path.join(os.getcwd(), sys.argv[1])
    outfile = os.path.join(os.getcwd(), '_'.join(['LearningData', sys.argv[2]+'.txt']))
    transcribe_corpus(infile, outfile, sys.argv[2])
    

