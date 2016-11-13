#!usr/bin/env python3
# -*- coding: utf-8 -*-

import os, shutil, sys

workdir = os.getcwd()

files = [x for x in os.listdir(workdir) if x.startswith('shona')]

print(files)

shonadic=[]

for file in files:
	list = open(file, 'r', encoding= 'utf-8')
	for line in list:
		line=line.strip('\n').split('\t')
		word = line[0].strip()
		if word not in shonadic:
			shonadic.append(word)
	list.close()

print('done reading shona files')


shonasingletons = ['i','o','a','u','e', "w", "y"]
shonapairs = {
	"nd" : "n d",
	"mb" : "m b",
	"ng" : "N g",
	"nh" : "n h",
	"mh" : "m h",
	"nz" : "n z",
	'nj': 'n j',
	"-" : ""	
}

outfile = open("LearningData.txt", 'w', encoding='utf-8')

for word in shonadic:
	for seg in shonasingletons:
		word = word.replace(seg, " " + seg +" ")
	for digraph in shonapairs:
		word = word.replace(digraph, shonapairs[digraph])
	word = word.replace("  ", " ")
	word = word.replace("'","")
	word = word.strip()
	outfile.write(word + '\n')
outfile.close()