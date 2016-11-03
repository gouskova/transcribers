#!usr/bin/env python3
# -*- coding: utf-8 -*-

# This is a script prepping a newline-eliminated .csv file of a fictionary into a list that doesn't contain illicit characters or

#====================================================
# Basic housekeeping: the original file I had is a dictionary, so quite a lot of words had superscript numbers to indicate different meanings; hyphenated compounds were also ruled out
#====================================================
import csv
wordlist = []
wordlength = 0
bound_stems = []

digraphs = ["cs", "dz", "dzs", "gy", "ly", "ny", "sz", "ty", "zs", "á", "é", "í", "ó", "ö", "ő", "ú", "ü", "ű"]
digits = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
#banned_segments = [" ", ",", "-", "à", "ä"]

with open('C:/Users/ildi/Dropbox/NYELVESZET/GitHub/transcribers/hungarian/preparation/hun_dict_SzAB.csv', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter="\t")
    for row in reader:
        word = row[0]
        for digit in digits:
            word = word.replace(digit,"")
        #word = word.replace('1', '')
        #word = word.replace('2', '')
        #word = word.replace('3', '')
        #word = word.replace('4', '')
        #word = word.replace('5', '')
        if word not in wordlist and not (word.startswith("leg") and word.endswith("bb")) and len(word) > 1 and word not in digraphs and " " not in word and "," not in word and "-" not in word and "à" not in word and "ä" not in word and "’" not in word and "." not in word and "(" not in word and ")" not in word:
            if word.endswith("a"):
                alternant = word[0:len(word)-1]+"á"
                bound_stems.append(alternant)
            if word.endswith("e"):
                alternant = word[0:len(word)-1]+"é"
                bound_stems.append(alternant)
            if word.endswith("alom"):
                alternant = word[0:len(word)-4]+"alm"
                bound_stems.append(alternant)
            if word.endswith("elem"):
                alternant = word[0:len(word)-4]+"elm"
            wordlength += len(word)
            wordlist.append(word.strip())

print(str(len(wordlist)) + " words remaining")
#print wordlist[:100]
print(float(wordlength)/len(wordlist))

#====================================================
#Writing out the output file into a .csv file
#====================================================

with open('hun_wordlist.csv', 'w', encoding='utf-8', newline='') as wordlist_csv:
    writer = csv.writer(wordlist_csv)
    writer.writerows(zip(wordlist))

with open('hun_bound_stems_automatic.csv', 'w', encoding='utf-8', newline='') as bound_stems_csv:
    writer = csv.writer(bound_stems_csv)
    writer.writerows(zip(bound_stems))
