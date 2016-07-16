#!usr/bin/env python3
# -*- coding: utf-8 -*-

import os
workdir = os.path.expanduser("C:/Users/ildi/Dropbox/NYELVESZET/GitHub/transcribers/hungarian/preparation/")
os.chdir(workdir)

import csv
wordlist = []
epenthetic_stems = []
mismatch = []
wordlength = 0
with open('hun_wordlist.csv', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter="\t")
    for row in reader:
        word = row[0]
        wordlist.append(word.strip())

with open('hun_epenthetics_manual.csv', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter="\t")
    for row in reader:
        word = row[0]
        epenthetic_stems.append(word.strip())


for word in epenthetic_stems:
    if word not in wordlist:
       mismatch.append(word)

print(mismatch)
