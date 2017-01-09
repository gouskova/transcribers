#!usr/bin/env python3
# -*- coding: utf-8 -*-

import os, shutil, sys

workdir = os.getcwd()

files = [x for x in os.listdir(workdir) if x.startswith('shona')]

shonadic=[]

for file in files:
	wlist = open(file, 'r', encoding= 'utf-8')
	for line in wlist:
		line=line.strip('\n').split('\t')
		word = line[0].strip()
		if not word in shonadic:
			shonadic.append(word.lower())
	wlist.close()

print('done reading shona files')


#shonatrigraphs = ['tsv','dzv']
#shonadigraphs=['mh','nh','dh','bh','vh', 'ch','sh','pf','sv','zh','zv','bv','ny','dz','dy','ty', 'ts']
#shonaV=['i','e','a','o','u']
#shonasingC = ['y','m','v','p','b','f','k','g','h','j','n','r','s','t','d','z','w']


shonadigraphs=['m h','n h','d h','b h','v h', 'c h','s h','p f','s v','z h','z v','b v','n y','d z','d y','t y', 't s']


outfile = open("LearningData.txt", 'w', encoding='utf-8')
orthofile = open("shona_all_ortho_key.txt", 'w', encoding='utf-8')

def spacify(wordlist, outfile, orthofile):
	for word in sorted(wordlist):
		orthoword = word
		word = word.replace("-", "")
		word = word.replace("\s", "") #spaces left from removing hyphens
		word = word.replace("n'", "N")
		word = word.replace("ng", "Ng")
		word = word.replace(" ", "")
		for seg in word:
			word = word.replace(seg, seg+" ").strip()
		word = word.replace("  ", " ")
		for digraph in shonadigraphs:
			word = word.replace(digraph, digraph.replace(" ",""))
		word = word.replace("ts v", 'tsv')
		word = word.replace("dz v", 'dzv')		
		word = word.replace("  ", " ")
		orthofile.write(orthoword + '\t' + word + '\n')
		outfile.write(word+'\n')
				
spacify(shonadic, outfile, orthofile)	

outfile.close()
orthofile.close()
