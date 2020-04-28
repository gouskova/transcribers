#!/usr/bin/env python3
# coding: utf-8

'''
takes in the list of 50,000 unigrams in An Crubadan's French/France corpus, extracts their transcriptions from Schott's list, and records them into a LearningData_crubadan.txt file
'''


with open('french-dictionary.txt', 'r', encoding='utf-8') as f:
    transkey = {}
    for line in f:
        transkey[line.split('\t')[0].lower()] = line.split('\t')[1].strip('\n')


counter = 0
with open('crubadan_french.txt', 'r', encoding='utf-8') as f:
    with open('LearningData_crubadan.txt', 'w', encoding='utf-8') as o:
        for line in f:
            if line.strip('\n').lower() in transkey:
                o.write(transkey[line.strip('\n').lower()]+'\n')
            else:
                print(line.strip('\n').lower())
                counter +=1


print(str(counter))


