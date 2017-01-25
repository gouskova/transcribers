#!usr/bin/env python3 
# -*- coding: utf-8 -*-
import itertools

def pairOEcalc(filepath, segs, rounded=2):
	'''
	segs is the list of segbols you want to evaluate for Observed/Expected
        the input should look like this: "a e i o u". Quotes and all.
	filepath is a path to a file that has one word per line, with spaces between segbols. 
	for example, 
	p a t a 
	p i k u b e
	s a mb u k i
	
	O/E is calculated as follows:
	Expected: N(S1) * N(S2)/ N of all pairs
	Observed: N(S1S2)
        the function will return unrounded OE, as well as a value rounded to the parameter given by the "rounded" argument. Defaults to 2, so an O/E value of 1.3432 will be printed as 1.34.
	
	'''
	words = open(filepath, 'r', encoding='utf-8').readlines()
	seglist = segs.strip().split(' ')
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
		pairs[pair]['OErnd']=round(pairs[pair]['OE'],rounded)
	return(pairs)
	
def makeOETable(pairsdic, segs, prnt=True, rawcounts=False, rounded=2):
    '''
    this function is a utility function, called by another one, and is meant to work in tandem with pairOECalc. the "segs" input is given to the upper level function.
    arranges the O/E values and sorts them into a table for display.
    "prnt" defaults to "True"; the function will print the results to screen.
    the default rounding paramter is 2. If you want to see raw unrounded values, pass "False" to 'rounded'
    if you want to see the raw counts for how often each seg is observed, set rawcounts to "True".
    '''
    seglist = segs.strip().split(' ')
    header = '\t'+'\t'.join(seglist)
    print(header)
    for seg in seglist:
        row = [seg]
        rndrow = [seg]
        for otherseg in seglist:
            pair = seg+otherseg
            row.append(str(pairsdic[pair]['OE']))
            rndrow.append(str(pairsdic[pair]['OErnd']))
            if rawcounts:
                observed = str(pairsdic[pair]['observed'])
        if rounded=="False":
            print('\t'.join(row))     
        else:
            print('\t'.join(rndrow))
        


#x = pairOEcalc('/home/maria/Desktop/LearningData.txt', "a e i o u")

#makeOETable(x, "a e i o u")

def OE(filepath, segs, prnt = True, rawcounts = False, rounded = 2):
    pairsdic = pairOEcalc(filepath, segs, rounded)
    makeOETable(pairsdic, segs, prnt, rawcounts, rounded)


#pathtofile = '/home/maria/Desktop/LearningData.txt'
#segs = "a e i o u"

#OE(pathtofile, segs)


if __name__ == "__main__":
    import sys
    OE(sys.argv[0], sys.argv[1])
