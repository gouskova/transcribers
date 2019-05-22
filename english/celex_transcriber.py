#!usr/bin/env python3
# -*- coding: utf-8 -*-

'''
there are two English wordlists with transcriptions: CMU and CELEX

The CMU list has a bunch of names and weird stuff in it, so it needs to be filtered for frequency. (The filtered version distributed with Hayes and White's paper has some mistakes in it)

The CELEX list has British English transcriptions, but on the plus side, it has syllabification breaks and CV skeleta. and frequencies, too

CELEX seems to be a better transcription overall, especially since it preserves the few morphological pseudocontrasts between affricates and stop-fric sequences

'''
#for importing transcribers module
import sys, os, re

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
englishpath = os.path.join(basedir, 'english')
sys.path = ['', basedir] + sys.path

import generic_transcriber as gtr


#now let's look at this celex transcription
path = 'celex_wordforms.txt'

celexdic = {}
ipakey = gtr.transc_table('celex_table.txt')

digraphs = ['a ʊ', 'a ɪ', 'e ɪ', 'o ʊ',  'ɔ ɪ',  'd ʒ', 't ʃ']


with open(path, 'r', encoding='utf-8') as f:
    for line in f:
        stuff = line.split("\\")
        ortho = stuff[1]
        if ortho.startswith("'") or " " in ortho:
            continue
        else:
            lemmafreq=stuff[3]
            #sylltrans = stuff[-1].strip()
            sylltrans = stuff[8].strip() #the last one is sometimes a variant pronunciation
            IPA = gtr.transcribe_wd(ipakey, sylltrans)
            for seq in digraphs:
                if seq in IPA:
                    IPA = IPA.replace(seq, seq.replace(' ', ''))
            IPA = IPA.replace("l ,", "ə l")
            IPA = IPA.replace("n ,", "ə n")
            IPA = IPA.replace("m ,", "ə m")
            IPA = IPA.replace("ŋ ,", "ə n")
            IPA = IPA.replace('ə ʊ', 'oʊ')
            IPA = IPA.replace('ɹ *', "")
            IPA = IPA.strip('[]').replace(':', "")
            IPA = IPA.replace(' ] [',  '')
            IPA = IPA.replace('  ', ' ')
            if not ortho in celexdic:
                celexdic[ortho]={'lemmafreq':lemmafreq, 'sylltrans':sylltrans, 'IPA': IPA}
            else:
                continue

with open('LearningData_w_ortho.txt', 'w', encoding='utf-8') as f:
    for word in sorted(celexdic):
        f.write(celexdic[word]['IPA'].strip()+'\t'+word+'\n') 

with open('LearningData.txt', 'w', encoding='utf-8') as f:
    for word in sorted(celexdic):
        f.write(celexdic[word]['IPA'].strip()+'\n') 

basedir = os.path.dirname(basedir)
phonopath = os.path.join(basedir, 'compseg/data/english')

print("Phonopath:" + phonopath)

#with open(os.path.join(phonopath, 'wds_t_s_tsh/LearningData.txt'), 'w', encoding='utf-8') as f:
#    for word in sorted(celexdic):
#        f.write(celexdic[word]['IPA'].strip()+'\n')

#with open(os.path.join(phonopath, 'wds_ts_tsh/LearningData.txt'), 'w', encoding='utf-8') as f:
#    for word in sorted(celexdic):
#        f.write(celexdic[word]['IPA'].replace('t s', 'ts').replace('d z', 'dz').strip()+'\n')

        
#with open(os.path.join(phonopath, 'wds_t_s_t_sh/LearningData.txt'), 'w', encoding='utf-8') as f:
with open(os.path.join(phonopath, 'LearningData_retrac.txt'), 'w', encoding='utf-8') as f:
    for word in sorted(celexdic):
        #f.write(celexdic[word]['IPA'].replace('tʃ', 't ʃ').replace('dʒ', 'd ʒ').strip()+'\n')
        f.write(celexdic[word]['IPA'].replace('tʃ', 't˗ ʃ').replace('dʒ', 'd˗ ʒ').strip()+'\n')

with open(os.path.join(phonopath, 'LearningData_orig.txt'), 'w', encoding='utf-8') as f:
    for word in sorted(celexdic):
        #f.write(celexdic[word]['IPA'].replace('tʃ', 't ʃ').replace('dʒ', 'd ʒ').strip()+'\n')
        f.write(celexdic[word]['IPA'].replace('tʃ', 't ʃ').replace('dʒ', 'd ʒ').strip()+'\n')


#with open(os.path.join(phonopath, 'wds_ts_t_sh/LearningData.txt'), 'w', encoding='utf-8') as f:
#    for word in sorted(celexdic):
#        f.write(celexdic[word]['IPA'].replace('tʃ', 't ʃ').replace('dʒ', 'd ʒ').replace('t s', 'ts').replace('d z', 'dz').strip()+'\n')

