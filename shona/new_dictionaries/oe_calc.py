#!usr/bin/env python3 
# -*- coding: utf-8 -*-
import itertools

def pairOEcalc(filepath, seglist):
	'''
	seglist is the list of segbols you want to evaluate for Observed/Expected
	for example, ['a', 'e', 'i', 'o', 'u']
	filepath is a path to a file that has one word per line, with spaces between segbols. 
	for example, 
	p a t a 
	p i k u b e
	s a mb u k i
	
	O/E is calculated as follows:
	Expected: N(S1) * N(S2)/ N of all pairs
	Observed: N(S1S2)
	
	'''
	words = open(filepath, 'r', encoding='utf-8').readlines()
	wordlist = [x.strip().split() for x in words]
	pairs = {}.fromkeys(''.join(list(x)) for x in itertools.product(seglist, repeat=2)) #creates a dictionary with S1,S2 pairs from seglist, every possible combination
	segs = {}.fromkeys(seglist, 0)
	for x in pairs:
		pairs[x] = {'observed':0, 'expected':0}
	paircount = 0
	for word in wordlist:
		word = [x for x in word if x in seglist]
		if len(word)<2:
			continue
		else:
			segpairsinword = [word[x]+word[x+1] for x in range(0, len(word)-1)] #a list of 2-seg pairs in the word
			paircount += len(segpairsinword)
			for pair in segpairsinword:
				joined = ''.join(pair)
				pairs[joined]['observed']+=1
			for seg in word:
				segs[seg] += 1
	for pair in pairs:
		seg1 = pair[0]
		seg2 = pair[1]
		pairs[pair]['expected'] = segs[seg1]*segs[seg2]/paircount
		pairs[pair]['OE'] = pairs[pair]['observed']/pairs[pair]['expected']
	return(pairs)
				
x = pairOEcalc('/Users/maria/Desktop/LearningData.txt', ['a','e','i','o','u'])


for pair in sorted(x):
	print(pair)
	print(round(x[pair]['OE'], 2))	
