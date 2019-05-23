#!/usr/bin/env python3
# coding: utf-8

'''
for converting paradigm list into token word list, transcribed
'''

def transkey(path):
    tk = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip().split('\t')
            tk[line[0]] = line[1]
    return tk


def transcribe(word, tk):
    for k in tk:
        if k in word:
            word = word.replace(k, tk[k])
    word = ' '.join(list(word))
    word = word.replace(" :", ":")
    word = word.replace("k h", 'k')
    word = word.replace("k k", "K")
    return word


def read_and_transcribe(tk, inpath, outpath):
    with open(inpath, 'r', encoding='utf-8') as f:
        with open(outpath, 'w', encoding='utf-8') as out:
            if 'latin-dictionary.txt' in inpath:
                for line in f:
                    word = line.strip().lower()
                    if 'ph' in word or 'y' in word or 'z' in word:
                           pass
                    else:
                        out.write(transcribe(word, tk)+'\n')
            else:
                for line in f:
                    words = [x for x in line.strip().split('\t')[3:] if not x=='']
                    for word in words:
                        if '/' in word:
                            for w in word.split('/'):
                                out.write(transcribe(w, tk) + '\n')
                        else:
                            out.write(transcribe(word, tk)+'\n')


if __name__ == '__main__':
    import sys
    tk = transkey('latin_transcription_key.txt')
    read_and_transcribe(tk, sys.argv[1], sys.argv[2])
    print("donesies")
                        
