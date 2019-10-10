#!/usr/bin/env python3
# coding: utf-8

import sys, os, re

basepath = os.path.split(os.getcwd())[0]
sys.path.append(basepath)

import generic_transcriber as gt

'''
removes stress marking, does not transcribe ach- and ich-laut; all rhotics are transcribed with the IPA uvular trill symbol
'''



def transcribe_wds(infile, outfile):
    gk = gt.transc_table('german_trans_key_all.txt')
    c4k   = gt.transc_table('german_trans_key_disc.txt')
    transkey={**gk, **c4k}
    with open(infile, 'r', encoding='utf-8') as f:
        with open(outfile, 'w', encoding='utf-8') as out:
            for line in f:
                #word = list(line.strip().split('\\')[4].replace('-', '').replace("'", "")) #for word celex list
                word = list(line.strip().split('\\')[3].replace('-', '').replace("'", "")) #for lemmas
                ipa = gt.transcribe_wd(transkey, word)
                out.write(f'{ipa}\n')

def transcribe_morphemes(infile, outfile):
    transmorphs = set()
    gk = gt.transc_table('german_trans_key_all.txt')
    celx = gt.transc_table('german_trans_key_celex.txt')
    transkey = {**gk, **celx}
    transkey["~"]=""
    with open(infile, 'r', encoding='utf-8') as f:
        for line in f:
            if len(line.strip().split('\t'))>8:    
                try:
                    morphemes = line.strip().split('\t')[8].replace("#", "¦").replace("+", "¦").split("¦")
                    for morph in morphemes:
                        morph = gt.transcribe_wd(transkey, list(morph))
                        transmorphs.add(morph)
                except IndexError:
                    print(line)
            else:
                pass 
    with open(outfile, 'w', encoding='utf-8') as out:
        for morph in sorted(transmorphs):
            out.write(f'{morph.replace(" :", "ː")}\n')



if __name__=='__main__':
#    infile = 'celex_german_phonology_words.txt'
    #infile = 'celex-german-phonology-lemmas.txt'
    #outfile = 'LearningData_celex_lemmas.txt'
    infile = sys.argv[1]
    outfile = sys.argv[2]
    if 'morphemes' in sys.argv:
        transcribe_morphemes(infile, outfile)
    else:
        transcribe_wds(infile, outfile)
    print('done')
