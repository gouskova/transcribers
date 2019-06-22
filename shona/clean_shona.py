#!/usr/bin/env python3
# coding: utf-8

'''
designed to make duramazwi recishona usable for phonological purposes
http://www.edd.uio.no/perl/search/search.cgi?appid=215;tabid=2391&lang=ENG
(the source list was obtained by sending an empty query to the database)
'''

def transkey():
    with open('transcription_key.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        transkey = {}.fromkeys(range(1,len(lines)+1))
        for key in transkey:
            line = lines[key-1].strip('\n').split('\t')
            transkey[key] = [line[0], line[1]]
    return transkey

def transcribe_wd(word, tkey):
    for key in sorted(tkey):
        word = word.replace(tkey[key][0], tkey[key][1])
    word = word.replace(" -", "")
    return word


def transcribe_words():
    tkey = transkey()
    segs = []
    with open('duramazwi_rechishona.txt', 'r', encoding='utf-8') as f:
        with open('LearningData.txt', 'w', encoding='utf-8') as out:
            for line in f:
                word = ' '.join(list(line.strip('\n').split('\t')[0].lower().strip('-')))
                word = transcribe_wd(word, tkey)
                for seg in word.split(' '):
                    if not seg in segs:
                        segs.append(seg)
                out.write(word+'\n')
    with open('Features.txt', 'w', encoding='utf-8') as f:
        for seg in sorted(segs):
            f.write(seg+'\n')
    print('done')




if __name__=='__main__':
    transcribe_words()
