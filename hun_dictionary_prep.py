#!usr/bin/env python2.7
# encoding: utf8
# -*- coding: utf-8 -*

# This is a script prepping a newline-eliminated .txt file into a proper input format for transcriber_hun.py

#====================================================
# Basic housekeeping: the original file I had is a dictionary, so quite a lot of words had superscript numbers to indicate different meanings; hyphenated compounds were also ruled out
#====================================================
import csv
wordlist = []
wordlength = 0
with open('C:\Users\ildi\Dropbox\NYELVESZET\PROJECTS\Tiers\Transcriber_hun\hun_dict_SzAB.csv') as f:
    reader = csv.reader(f, delimiter="\t")
    for row in reader:
        word = row[0]
        word = word.replace('1', '')
        word = word.replace('2', '')
        word = word.replace('3', '')
        word = word.replace('4', '')
        word = word.replace('5', '')
        if word not in wordlist:
            if len(word) > 1 and word != 'cs' and word != 'dz' and word != 'dzs' and word != 'gy' and word != 'ly' and word != 'ny' and word != 'sz' and word != 'ty' and word != 'zs' and '-' not in word:
                wordlength += len(word)
                wordlist.append(word)

print(str(len(wordlist)) + " words remaining")
#print wordlist[:100]
print float(wordlength)/len(wordlist)

#====================================================
# Filtering out compounds and derived words: fake_suffixes is a collection of "words" that as second parts result in fake positives for compounds
#====================================================
roots = []
rootlength = wordlength

fake_suffixes = ['oda', 'dia', 'ha', 'ja', 'se', 'ne', 'le', 'de', 'ad', 'na', 'ma', 'la', 'tematika', 'ex', 'ú']
preverbs = ['meg', 'le', 'fel', 'föl', 'be', 'ki', 'szét', 'össze', 'vissza', 'hozzá', 'rá', 'neki', 'át', 'oda', 'ide']
suffixes = []
# comment the line below out if you don't want to rule out derivative suffixes
suffixes = ['zat', 'zet', 'ság', 'ség', 'ó', 'ő', 'adék', 'omány', 'emény', 'os', 'es', 'ás', 'és', 'i']

for potential_compound in wordlist:
    length = len(potential_compound)
    roots.append(potential_compound)
    for n in range(length):
        potential_prefix = str(potential_compound[0:n])
        potential_suffix = str(potential_compound[n:length])
        if potential_prefix in wordlist and (potential_suffix in wordlist or potential_suffix in suffixes) and potential_suffix not in fake_suffixes:
            #print potential_compound
            roots.remove(potential_compound)
            rootlength = rootlength - len(potential_compound)
            break

print(str(len(roots)) + " words remaining")
#print roots[:100]
print float(rootlength)/len(roots)

#====================================================
# write roots into a .csv file that can be an input to the transcriber
#====================================================
with open('hun_roots.csv', 'wb') as roots_csv:
    writer = csv.writer(roots_csv)
    for root in roots:
        writer.writerows(root)
