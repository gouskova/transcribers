#!/usr/bin/env python3
# encoding: utf-8


'''
given a text with paragraphs, capitalization, punctuation, this will transcribe it into connected speech in IPA, without stresses or punctuation or spaces between words.
Tricky bits: applying voicing assimilation to left- and right-leaning clitics
dealing with hyphenation
'''

import os, sys, re


import transcriber_russ as tr

# read in left clitics
def clist(path):
    with open(path, 'r', encoding='utf-8') as f:
        return([x.rstrip('\n') for x in f.readlines()])

def process_lines(inpath, outpath, wb=True):
    leftlist = clist('leftclitics.txt')
    rightlist = clist('rightclitics.txt')
    with open(inpath, 'r', encoding='utf-8') as f:
        with open(outpath, 'w', encoding='utf-8') as out:
            for line in f:
                line=line.lower().strip('\n').lstrip("- ")
                line = re.sub('\d+', '', line)
                if line == '':
                    continue
                else:
                    line = ' '.join(re.split('["\,\.\!\?:;]+', line))
                    line = line.replace('--', '')
                    line = re.sub('[()\*«»\|\[\]\{\}]', '', line)
                    for cl in leftlist:
                        line = re.sub(r'(^|\s)'+cl+' ', '\\1'+cl, line)
                    for cl in rightlist:
                        line = re.sub(' '+cl+r'($|\s)', cl+'\\1', line)
                    line = line.replace('-', '')
                    if not line=="":
                        words = [x for x in line.split(" ") if not x=='']
                        outline = []
                        for word in words:
                            if re.search('[a-z]', word):
                                pass
                            else:
                                outw = tr.transcribe(word, stress='off', spaces='yes', voice='yes', reduction='no').replace('ʨ', 't ɕ').replace('ʦ', 't s').replace('ʥ', 'd ʑ').replace('ʣ', 'd z')
                                if word.startswith('t ɕ t o'):
                                    word = word.replace('t ɕ t o', 'ʂ t o')
                                if not wb:
                                    outline.append(outw)
                                if wb:
                                    out.write(outw+'\n')
                        if not wb:
                            out.write(' '.join(outline)+ ' ')
    print("done")




if __name__=='__main__':
    #basepath = os.path.expanduser("~/Dropbox/work/dictionaries/russian_dictionaries/novel_corpus/")
    #for fi in os.listdir(basepath):
    #    fin = fi.split('.txt')[0]
    #    outfile = os.path.join("novel_corpus", fin+'_IPA.txt')
    #    if not os.path.isfile(outfile):
    #        try:
    #            process_lines(os.path.join(basepath, fi), outfile, wb=True)
    #        except UnicodeDecodeError:
    #            pass
    process_lines('russian_novels.txt', 'russian_novels_IPA.txt', wb=False)

