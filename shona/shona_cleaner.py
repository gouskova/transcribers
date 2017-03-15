#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
this doesn't really do anything useful at the moment'
'''

shonafile = open("Shona.Hannan1959_utf8.txt", 'r', encoding='utf-8')

shonaraw = shonafile.readlines()
print(len(shonaraw))

shona = {}
for line in shonaraw[100:2000]:
	entry = line.strip('\n').strip()
	if entry == "":
		continue
	else:
		entry = entry.split(' ')
		word = entry[0].lower()
		if len(entry)>1:
			tones = entry[1]
			cat = entry[2]
			print(word + " " + tones + " " + cat)
			if word.endswith('-'):
				shona[word]={'mcat':'prefix','syncat':cat, 'tones':tones.strip('[]')}
			elif word.startswith('-'):
				shona[word]={'mcat':'suffix','syncat':cat, 'tones':tones.strip('[]')}
			else:
				shona[word]={'mcat':'root','syncat':cat, 'tones':tones.strip('[]')}

print(len(shona))
		
shonafile.close()		
	
shonalex = [wd for wd in shona if shona[wd]['mcat']=='root' and "H" in shona[wd]['tones'] or "L" in shona[wd]['tones']]
shonaverbs = [wd for wd in shona if shona[wd]['syncat']=='v' and shona[wd]['mcat']=='root']
shonanouns = [wd for wd in shona if shona[wd]['syncat']=='n'and shona[wd]['mcat']=='root']

print('shona lex cats')
print(len(shonalex))

print('shona verbs')
print(len(shonaverbs))
for x in shonaverbs:
	print(x)

print('shona nouns ')
print(len(shonanouns))

illicitchars=['~','-',"�-", ">"]

