#!/usr/bin/env python3
# coding: utf-8

'''
slight modifications to the file from Schott's wordlist for greek (Ralf's dictionaries) to make it usable in UCLAPL research
'''

def writefeats(inset, outpath):
    outlist = []
    for wd in inset:
        segs = wd.split(' ')
        for seg in segs:
            if not seg in outlist:
                outlist.append(seg)
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sorted(outlist)))


def spacify(inpath):
    out = set() 
    with open(inpath, 'r', encoding='utf-8') as f:
        for line in f:
            wd = ' '.join(list(line.rstrip('\n')))
            wd = wd.replace('ɪ', 'i')
            out.add(wd)
    return out


def writeld(inset, outpath):
    with open(outpath, 'w', encoding='utf-8') as f:
        for wd in sorted(inset):
            f.write(wd+'\n')


if __name__=='__main__':
    inpath = 'greek-dictionary.txt'
    x = spacify(inpath)
    writeld(x, 'LearningData.txt')
    writefeats(x, 'Features.txt')
