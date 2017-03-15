#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''
Using the xml libraries for this was more trouble than it was worth, considering the shona text is mixed in with the english text anyway.

doing it the dumb way instead.

'''

import os

basepath = os.getcwd()

#read in all the words from the shona wikipedia dump. if there's more than one file, it will look for the most recent one (that's why [-1]):

wikidump = open([x for x in os.listdir(basepath) if x.endswith('xml')][-1], 'r', encoding='utf-8')
raw = []

#out = open('shona_wiki_raw.txt', 'w', encoding='utf-8')
garbage= []

for line in wikidump:
    line = line.strip().split(' ')
    for word in line:
        if word.endswith("&lt;br"):
            word = word[0:-6]
        if word.startswith("&quot;"):
            word = word[6:]
        if word.endswith("&quot"):
            word = word[0:-5]
        word=word.strip("][.,:;!?*()'").lower()
        word = word.replace("n'", "nq") #the n' thing is used for a segment in the orthog.
        if word.isalpha():
            word = word.replace('nq', "n'")
            raw.append(word)
#           out.write(word+'\n')
        else:
            garbage.append(word)
wikidump.close()
#out.close()

garbage = sorted(set(garbage))

garbfile = open('garbage_from_shona_wiki.txt', 'w', encoding='utf-8')
for word in garbage:
    garbfile.write(word+'\n')
garbfile.close()


#read in the celex wordform list for english:

celex = open('celex_word_freq.txt', 'r', encoding='utf-8')
english = []

for line in celex:
    word = line.split("\\")[1]
    if not word in english:
        english.append(word.lower())


rawset = set(raw)
print('the length of the raw shona list is: ')
print(len(rawset))

#intersect them:
engsubset = set(english) & rawset
print(list(engsubset)[0:300])


print('the length of the shona list minus Celex english words is: ')
shona_cleaned = sorted(rawset - engsubset)
print(len(shona_cleaned))

vowels = ['a', 'e', 'i', 'o', 'u'] 

#because real shona words don't end in consonants or "y":
shona_cleaned = [word for word in shona_cleaned if word[-1] in vowels]


print('the length of cleaned shona list after c-pruning: ')
print(len(shona_cleaned))

cleanshona = open('shona_wiki_clean.txt', 'w', encoding='utf-8')
for word in sorted(shona_cleaned):
    cleanshona.write(word+'\n')

cleanshona.close()



    

