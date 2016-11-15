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
		if word not in shonadic:
			shonadic.append(word.lower())
	wlist.close()

print('done reading shona files')


shonatrigraphs = ['tsv','dzv']
shonadigraphs=['mh','pf','bh','bv','vh','ng','ch','sh','sv','zh','zv','ny', 'nh','dh','dz','dy','ty', 'ts']
shonaV=['i','e','a','o','u']
shonasingC = ['y','m','v','p','b','f','k','g','h','j','n','r','s','t','d','z','w']


outfile = open("LearningData.txt", 'w', encoding='utf-8')
orthofile = open("shona_all_maxentified.txt", 'w', encoding='utf-8')

def spacify(wordlist, outfile, orthofile):
	for word in sorted(wordlist):
		orthoword = word
		word = word.replace("'","")
		word = word.replace("-", "")
		word = word.replace("ng", "Ng")
		word = word.replace(" ", "")
		for seg in word:
			word = word.replace(seg, seg+" ")
		word = word.replace("  ", " ").strip()
		for digraph in shonadigraphs:
			spaced = list(digraph)[0]+ ' ' + list(digraph)[1]
			word=word.replace(spaced, digraph)
		word = word.replace("ts v", 'tsv')
		word = word.replace("dz v", 'dzv')		
		word = word.replace("  ", " ").strip()
		orthofile.write(orthoword + '\t' + word + '\n')
		outfile.write(word+'\n')
				
spacify(shonadic, outfile, orthofile)	

outfile.close()
orthofile.close()



#		if len(word)==1:
#			outfile.write(word+'\n')
#			orthofile.write(word + '\t' + word + '\n')
#		else:
#			newword=[]
#			for segindex in range(len(word)-1):
#				seg = word[segindex]
#				if segindex<len(word)-1: 
#					ondigraph = False
#					ontrigraph = False
#					if not ondigraph and not ontrigraph:
#						follseg=word[segindex+1]
#						digraph = seg+follseg
#					if segindex < len(word)-2:
#						thirdseg = word[segindex+2]
#						trigraph = digraph+thirdseg
#						if trigraph in shonacombos:
#							ontrigraph = True
#							newword.append(trigraph + " ")
#						elif digraph in shonacombos:
#							ondigraph = True
#							newword.append(digraph+" ")
#						else:
#							newword.append(seg+' ')				
#					elif ontrigraph == True:
#						seg = word[segindex+2]
#						newword.append(seg + " ")
#				else:
#					newword.append(seg)							
#			newword = ''.join(newword).strip()