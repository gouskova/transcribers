#!/usr/bin/env python3
# coding: utf-8

'''
fixes the deprecated Mac OS txt file of Creissels' 1996 French-Tswana dictionary.

has options to preserve or delete tones, and to save the txt file as a dictionary or as a single word list.

also makes a starter Features.txt file with one segment per row
'''

import re

def preprocess_dic():
    indic = 'Tswana.Creissels1996_orig.txt'
    outdic = 'Tswana.Creissels1996.txt'
    subtable = read_transkey('subtable.txt')
    with open(indic, 'r') as f:
        with open(outdic, 'w', encoding='utf-8') as out:
            for line in f:
                for sub in subtable:
                    line = line.replace(sub, subtable[sub])
                out.write(line)
    print('done fixing the original')


def read_transkey(path):
    transkey = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            transkey[line.strip().split('\t')[0]]=line.strip().split('\t')[1]
    return transkey

def tones(word, removetones = True):
    if not removetones:
        word = word.replace("%", "ˋ")
        word = word.replace("@", "ˊ")
    else:
        word = word.replace("@", "")
        word = word.replace("%", "")
    return word 

vowels = ['a', 'e', 'i', 'u', 'ɛ', 'ɪ', 'o','ɔ']

def transcribe(word, transkey, removetones):
    word = tones(word, removetones)
    for seg in transkey:
        word = word.replace(seg, transkey[seg])
    word = ' '.join(list(word))
    #aspiration and h
    vREr = '(['+''.join(vowels)+'])()'
    vREl = '(['+''.join(vowels)+'])([ˋˊ]*)'
    if not removetones:
        word = re.sub(" ([ˋˊ])", '\\1', word)
    else:
        vREl = vREr
    #remove space before h, then add it back in after vowels
    word = word.replace(" ˋ", "")
    word = word.replace(" h", "h")
    word = re.sub(vREl + 'h '+vREr, '\\1\\2 h \\3', word) 
    return word.strip()

def transcribe_wds(path, transkey, removetones):
    out = {}
    poslist = ['part', 'v', 'n', 'conj', 'ad', 'prep', 'd', 'int']
    with open(path, 'r', encoding='utf-8') as f:
        num = 0
        for line in f:
            num+=1
            words = line.strip().split('\t')
            out[num] = {}
            out[num]['french']=words[0].replace("@", "'")
            if words[1].endswith('-') or words[1].endswith('.'):
                out[num]['prefix']= words[1]
            else:
                out[num]['prefix']=''
            out[num]['POS']='NA'
            if words[-1] in poslist:
                out[num]['POS']=words[-1]
                out[num]['tswana_orig']=words[-2]
            else:
                out[num]['tswana_orig']=words[-1]
            transstem = transcribe(out[num]['tswana_orig'], transkey, removetones)
            out[num]['tswana_trans'] = transstem 
            spacepref = ' '.join(list(out[num]['prefix'].rstrip('-.')))
            out[num]['tswana_spaces'] = spacepref + ' ' + transstem
            out[num]['tswanawd'] = out[num]['prefix'].rstrip('-.') +' ' +out[num]['tswana_trans']
    return out


def writefeats(dic, outpath):
    outlist = []
    for wd in dic:
        segs = dic[wd]['tswana_spaces'].split(' ')
        for seg in segs:
            if not seg in outlist:
                outlist.append(seg)
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sorted(outlist)))


if __name__=='__main__':
    import sys
    preprocess_dic()
    tswanadic = 'Tswana.Creissels1996.txt'
    transkey = read_transkey('transcription_key.txt')
    if 'writefrench' in sys.argv:
        x = transcribe_wds(tswanadic, transkey, removetones=False)
        with open('tswana-french-dictionary.txt', 'w', encoding='utf-8') as f:
            f.write('\t'.join(['word', 'prefix', 'stem', 'notones', 'part of speech', 'french'])+'\n')
            for wd in sorted(x):
                f.write('%s\t%s\t%s\t%s\t%s\n' % (x[wd]['tswanawd'],x[wd]['prefix'], x[wd]['tswana_trans'], x[wd]['POS'], x[wd]['french']))
        print("finished writing Tswana dictionary")
    if 'writeld' in sys.argv:
        x = transcribe_wds(tswanadic, transkey, removetones=True)
        writefeats(x, 'Features_notones.txt')
        with open('LearningData_notones.txt', 'w', encoding='utf-8') as f:
            for wd in sorted(x):
                f.write("%s\n" % x[wd]['tswana_spaces'])
        print('finished writing Tswana Learing Data and Features without tones')
        x = transcribe_wds(tswanadic, transkey, removetones=False)
        writefeats(x, 'Features_tones.txt')
        with open('LearningData_tones.txt', 'w', encoding='utf-8') as f:
            for wd in sorted(x):
                f.write("%s\n" % x[wd]['tswana_spaces'])
        print('finished writing Tswana Learing Data and Features with tones')

