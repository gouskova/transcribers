#!usr/bin/env python3
# -*- coding: utf-8 -*-

# This is a script filtering out foreign (greek and latin) words and polimorphemic words from newline-eliminated .csv file (for phonotactic purposes)

#====================================================
#A function for making a flat list out of a .txt file of affixes and their allomorphs
#====================================================

def make_flat_dict(infile):
    dictionary=[]
    for line in infile:
        morph_soup=line.strip('\n').split(', ')
        for morph in morph_soup:
            dictionary.append(morph)
    return dictionary


#====================================================
#Reading in the affix files as flat lists and the wordlist
#====================================================

import os
workdir = os.path.expanduser("C:/Users/ildi/Dropbox/NYELVESZET/GitHub/transcribers/hungarian/preparation/")
os.chdir(workdir)

import csv
wordlist = []
rootlist = []
rootlength = 0
wordlength = 0
with open('C:/Users/ildi/Dropbox/NYELVESZET/GitHub/transcribers/hungarian/preparation/hun_wordlist.csv', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter="\t")
    for row in reader:
        word = row[0]
        wordlength += len(word)
        wordlist.append(word.strip())

with open('C:/Users/ildi/Dropbox/NYELVESZET/GitHub/transcribers/hungarian/preparation/hun_roots.csv', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter="\t")
    for row in reader:
        word = row[0]
        rootlength += len(word)
        rootlist.append(word.strip())

bound_stems1 = []
with open('C:/Users/ildi/Dropbox/NYELVESZET/GitHub/transcribers/hungarian/preparation/hun_bound_stems_automatic.csv', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter="\t")
    for row in reader:
        word = row[0]
        wordlength += len(word)
        bound_stems1.append(word.strip())

preverbs_file = open("hun_preverbs.txt", 'r', encoding='utf-8')
preverbs = make_flat_dict(preverbs_file)

prefixes_file = open("hun_prefixes.txt", 'r', encoding='utf-8')
prefixes = make_flat_dict(prefixes_file)

derivational_suffixes_file = open("hun_derivational_suffixes.txt", 'r', encoding='utf-8')
derivational_suffixes = make_flat_dict(derivational_suffixes_file)

inflectional_suffixes_file = open("hun_inflectional_suffixes.txt", 'r', encoding='utf-8')
inflectional_suffixes = make_flat_dict(inflectional_suffixes_file)

prefix_banlist_file = open("hun_prefix_banlist.txt", 'r', encoding='utf-8')
prefix_banlist = make_flat_dict(prefix_banlist_file)

suffix_banlist_file = open("hun_suffix_banlist.txt", 'r', encoding='utf-8')
suffix_banlist = make_flat_dict(suffix_banlist_file)

bound_stems2_file = open("hun_bound_stems_misc.txt", 'r', encoding='utf-8')
bound_stems2 = make_flat_dict(bound_stems2_file)

bound_stems3_file = open("hun_bound_stems_epenthetic.txt", 'r', encoding='utf-8')
bound_stems3 = make_flat_dict(bound_stems3_file)

stem_alternants = bound_stems1 + bound_stems2 + bound_stems3

prefix_list = preverbs + prefixes
super_prefix_list = prefix_list + wordlist + stem_alternants

suffix_list = derivational_suffixes + inflectional_suffixes
super_suffix_list = suffix_list + wordlist
super_duper_suffix_list = super_suffix_list + stem_alternants


#====================================================
# Filtering out compounds and derived words: fake_suffixes is a collection of "words" that as second parts result in fake positives for compounds
#====================================================

roots = []

for word in wordlist:
    length = len(word)
    roots.append(word)
    print(word)
    if len(word) > 9:
        roots.remove(word)
    if word in roots:
        for banned_prefix in prefix_banlist:
            if word.startswith(banned_prefix):
                roots.remove(word)
                print("\t\t banned_prefix")
                break

    if word in roots:
        if "x" in word:
            roots.remove(word)
            print("\t\t x")

    if word in roots:
        #print(word)
        for banned_suffix in suffix_banlist:
            if word.endswith(banned_suffix):
                roots.remove(word)
                print("\t\t banned_suffix")
                break

    if word in roots:
        #print(word)
        for m in range(0,length):
            morph1a = word[0:m]
            morph2a = word[m:length+1]
            if morph1a in super_prefix_list and morph2a in super_suffix_list:
                roots.remove(word)
                print("\t\t dimorphemic")
                break

    if word in roots:
        #print(word)
        find = False
        for n in range(0,length-1):
            for o in range(n+1,length):
                #print(str(n)+ " and " + str(o))
                morph1b = word[0:n]
                morph2b = word[n:o]
                morph3b = word[o:length+1]
                if morph1b in super_prefix_list and morph2b in super_duper_suffix_list and morph3b in super_suffix_list:
                    roots.remove(word)
                    print("\t\t trimorphemic")
                    find = True
                    break
            if find == True:
                break

rootlength = 0
for root in roots:
    rootlength += len(root)

print(str(len(roots)) + " words remaining")
#print(roots[:100])
print("total string length:" + str(rootlength))
print(float(rootlength)/len(roots))

#====================================================
# write roots into a .csv file that can be an input to the transcriber
#====================================================

with open('hun_roots.csv', 'w', newline='', encoding='utf-8') as roots_csv:
    writer = csv.writer(roots_csv)
    writer.writerows(zip(roots))
