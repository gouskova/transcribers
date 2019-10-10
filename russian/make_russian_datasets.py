#!/usr/bin/env python3
# coding: utf-8

'''
fixes various issues in the transcription of morpheme-boundary-marked data, for the purposes of studying russian affricates and clusters.

geminates are not pronounced as geminates except at morpheme boundaries

voicing assimilation is not working correctly across morpheme boundaries

t's'a is not pronounced palatalized, ever

replaces morpheme boundary with either nothing or with "¦" depending on needs
'''

import sys, os

basepath = os.path.dirname(os.path.dirname(os.path.dirname((os.getcwd()))))
sys.path.append(basepath)

#custom modules

from transcribers.russian import transcriber_russ as trus
import pynatclasses as pnc
#from morphology.russian.code import transcribe_morphemes as tmorph



mbsym = ' ¦ '


mb_agree_clusters = {}
for key in trus.agree_clusters:
    agreedkey = mbsym.join(key.split(" "))
    mb_agree_clusters[agreedkey] = mbsym.join(trus.agree_clusters[key].split(" "))  


#making the baseline file where everything is a cluster and there are no affricates

basefile = os.path.join(basepath, 'compseg', 'data', 'russian', 'LearningData_base.txt')




def make_learning_data(datadir, consonants, ctable, prenas=False):
    with open(basefile, 'r', encoding='utf-8') as infile:
        with open(os.path.join(datadir, 'LearningData.txt'), 'w', encoding='utf-8') as outfile:
            for word in infile:
                word = word.strip()
                for c in consonants:
                    word = word.replace(' '.join([c,c]), c)
                word = word.rstrip("|").replace(" | ", ' ').strip()
                word = trus.voicing(word)
                for thing in ctable:
                    word = word.replace(thing, ctable[thing])
                if prenas:
                    for thing in prenas:
                        word = word.replace(thing, prenas[thing])
                outfile.write(word+'\n')
    print('Done with '+ datadir)


# all clusters
clusterdir = os.path.join(basepath, 'compseg', 'data', 'russian', 'wds_t_s_t_sh')
consonants = pnc.get_consonants(os.path.join(clusterdir, 'Features.txt'))
clustertable = {
            "ʦ": "t s",
            "ʨ": "t ɕ",
            "ʥ": "d ʑ",
            "ʣ": "d z"}

make_learning_data(clusterdir, consonants, clustertable)

#ts is an affricate but ch is not:
clusterdir = os.path.join(basepath, 'compseg', 'data', 'russian', 'wds_ts_t_sh')
consonants = pnc.get_consonants(os.path.join(clusterdir, 'Features.txt'))
clustertable = {
            "ʦ": "ts",
            "ʨ": "t ɕ",
            "ʥ": "d ʑ",
            "ʣ": "dz"}

make_learning_data(clusterdir, consonants, clustertable)


#ch is an affricate but ts is not:
clusterdir = os.path.join(basepath, 'compseg', 'data', 'russian', 'wds_t_s_tsh')
consonants = pnc.get_consonants(os.path.join(clusterdir, 'Features.txt'))
clustertable = {
            "ʦ": "t s",
            "ʨ": "tɕ",
            "ʥ": "dʑ",
            "ʣ": "d z"}


make_learning_data(clusterdir, consonants, clustertable)


#all affricates:
clusterdir = os.path.join(basepath, 'compseg', 'data', 'russian', 'wds_ts_tsh')
consonants = pnc.get_consonants(os.path.join(clusterdir, 'Features.txt'))
clustertable = {
            "ʦ": "ts",
            "ʨ": "tɕ",
            "ʥ": "dʑ",
            "ʣ": "dz"}


make_learning_data(clusterdir, consonants, clustertable)


#prenas and affricates:
clusterdir = os.path.join(basepath, 'compseg', 'data', 'russian', 'wds_prenas_aff')
consonants = pnc.get_consonants(os.path.join(clusterdir, 'Features.txt'))
clustertable = {
            "ʦ": "ts",
            "ʨ": "tɕ",
            "ʥ": "dʑ",
            "ʣ": "dz"}

prenas = {"m p": "mp",
        "m b": "mb",
        "n t": "nt",
        "n d": "nd"}

make_learning_data(clusterdir, consonants, clustertable, prenas)


