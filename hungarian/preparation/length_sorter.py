#!usr/bin/env python3
# -*- coding: utf-8 -*-

#This is a script writing two output files based on one input file. One contains words that are at most 7 characters long, the other writes 8-character-long words into a separate file

#====================================================
#Dividing the input file into 3 subsets: up to 7, exactly 8 and 9-and-up character long words
#====================================================
import csv

rootlist = []
#nine_long = 0
#nine_long_list = []
remaining_list = []
eight_long = 0
eight_long_list = []

with open('C:/Users/ildi/Dropbox/NYELVESZET/GitHub/transcribers/hungarian/preparation/hun_roots.csv', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter="\t")
    for row in reader:
        word = row[0]
        rootlist.append(word.strip())

for word in rootlist:
    if len(word) < 8:
        #print(word)
        remaining_list.append(word)
    if len(word) == 8:
        eight_long += 1
        eight_long_list.append(word)


#print(str(nine_long) + "nine-character-long words")
print(str(eight_long) + "eight-character-long words")

#====================================================
#Writing the 0-to-7-character-long words and 8-character-long words into separate files.
#====================================================
with open('hun_root_list.csv', 'w', newline='', encoding='utf-8') as short_ones:
    writer = csv.writer(short_ones)
    writer.writerows(zip(remaining_list))

#with open('hun_ninelong.csv', 'w', newline='', encoding='utf-8') as ninelong_csv:
#    writer = csv.writer(ninelong_csv)
#    writer.writerows(zip(nine_long_list))

with open('hun_eightlong.csv', 'w', newline='', encoding='utf-8') as eightlong_csv:
    writer = csv.writer(eightlong_csv)
    writer.writerows(zip(eight_long_list))