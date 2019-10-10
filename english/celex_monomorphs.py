#!/usr/bin/env python3
# coding: utf-8

'''
this is a dumb shortcut. taking celex "eml.cd", remove from the list any word that has a morpheme boundary in the line. the celex dataset indicates most of them with a + somewhere on the line so that's what we'll use
'''

def find_monomorphs():
    wds = set()
    with open('celex_segmentation.txt', 'r', encoding='utf-8') as segm:
        for line in segm:
            if '+' in line:
                continue
            else:
                wds.add(line.strip().split('\\')[1])
    return wds

def transcribe_monomorphs():
    wds = find_monomorphs()
    with open('LearningData_w_ortho.txt', 'r', encoding='utf-8') as trans:
        with open('LearningData_monomorphs.txt', 'w', encoding='utf-8') as out:    
            for line in trans:
                if line.rstrip('\n').split('\t')[1] in wds:
                    out.write(line.split('\t')[0]+'\n')
    print('done')

if __name__=='__main__':
    transcribe_monomorphs()
