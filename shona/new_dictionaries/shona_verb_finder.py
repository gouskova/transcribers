#usr/bin/env python3
#-*- coding: utf-8 -*-

import os, cleanshona



def findHyph(infile, outfile):
	'''
	this goes through the Chimhundu dictionary .txt file, shona_all_ortho_key.txt
	finds verbs, which are hyphen-initial
	returns them
	checks if they all end in 'a'
	'''
	words = open(infile, 'r', encoding='utf-8')
	vdic={}
	for line in words:
		if line.startswith('-'):
			orthword=line.strip('\n').split('\t')[0]
			transcr = line.strip('\n').split('\t')[1]
			if orthword.endswith('a'): #all verbs appear in citation forms, which end in -a. the non-a-final ones are function words of some sort. unclear
				vdic[orthword]=transcr
				#print('the word ' + orthword + ' does not end in a')
	print('the number of hyphen-initial stems is ' + str(len(vdic)))
	f=open(outfile, 'w', encoding='utf-8')
	for thing in sorted(vdic, key= vdic.get):
		f.write(vdic[thing]+ '\n')
	return (vdic)

findHyph(infile='shona_all_ortho_key.txt', outfile='/Users/maria/Desktop/shonaverbs_chimhundu.txt')

