#!/usr/bin/env python3
# *-* coding:utf-8 *-*

'''
Mongolian transcription notes:

Source: 
Svantesson, Jan-Olof and Tsendina, Anna and Mukhanova Karlsson, Anastasia and Franzén, Vivian. "The Phonology of Mongolian. 2005, Oxford University Press.

This book describes the Khalkha (Halh) dialect, spoken in Ulan Baatar.

Vowel length:

The language has a vowel length contrast, confined to the first syllable. Orthographic double vowels are pronounced as short in subsequent syllables.

Vowel quality: ATR contrast between [e,u,o] and [a, ʊ, ɔ]; narrow transcriptions depict [i] and [ɪ] as distinct.


There is a palatalization contrast, which appears to be related to the pharyntalization distinction in vowels such that "plain" consonants occur with pharyngealized vowels and palatalized consonants occur with non-pharyngealized vowels.

Palatalization is predictably present after i-diphthongs, thus aiC is aiCj

there's some sort of apocope going on between the orthography and the pronunciation, such that final э is not pronounced but is instead interpreted as lack of palatalization on the preceding consonant

final н means velar; final нэ means alveolar

velars [ŋ, x] occur in the vicinity of [i, e, u, o]; the uvulars [ɴ, χ] in the vicinity of [a, ʊ, ɔ]

there is a morpheme boundary blocking effect: [χ] fails to raise to [x] when followed by a suffix [i]; this is reflected in the orthography (сүх-ийг] is velar and [ах-ыг] is uvular

I'm making the executive decision to transcribe "г" as [k], not [g], because it's a really suspicious gap in the inventory
'''

import re

#=======================================================================

cyr_vowels = {
    'а':'a',
    'о':'ɔ',
    'ө':'o',
    'у':'ʊ',
    'ү':'u',
    'ы':'i',
    'э':'e',
    'е':'j e',
    'ё':'j ɔ',
    'и':'j i',
    'ю':'j ʊ',
    'я':'j a'
    }
    


cyr_consonants={
        'б':'p',
        'в':'w',
        'г':'g',
        'д':'t',
        'ж':'ʧ',
        'з':'ʦ',
        'й':'j',
        'к':'g', #unclear if there is a contrast
        'л':'ɮ',
        'м':'m',
        'н':'n',
        'п':'pʰ',
        'р':'r',
        'с':'s',
        'т':'tʰ',
        'ф':'pʰ',
        'х':'x',
        'ц': 'ʦʰ',
        'ч':'ʧʰ',
        'ш':'ʃ',
        'ь':'ʲ'
    }

long_j_combos={
        'я а': 'j aa',
        'е э': 'j ee',
        'е ө': 'j oo',
        'ё о': 'j ɔɔ',
        'ю у': 'j ʊʊ',
        'ю ү': 'j uu'}

#these are the full vowels
vowels_phar = ['a', 'aa', 'ɔ', 'ɔɔ', 'ʊ', 'ʊʊ'] 
vowels_nophar = ['o', 'oo', 'i', 'ii', 'u', 'uu', 'e', 'ee']

vowels = vowels_phar+vowels_nophar
short_vowels = [x for x in vowels if len(x)==1]
long_vowels = [x for x in vowels if len(x)==2]

def spacify(word):
        word = word.lower()
        chars = list(word)
        word =" ".join(chars)
        return word



def transcribe_vowels(word):
    word = word.replace("и й", "j ii")
    word = word.replace("э й", "ee")
    for v in long_j_combos:
        word = word.replace(v, long_j_combos[v])
    for v in cyr_vowels:
        #long vowels:
        word = word.replace(v+ ' ' + v, cyr_vowels[v]*2)
        #short vowels:
        word = word.replace(v, cyr_vowels[v])
    for v in vowels:
        word=word.replace(' i ' + v, ' j ' + v*2) 
    return word


def transcribe_consonants(word):
    for c in cyr_consonants:
        word = word.replace(c, cyr_consonants[c])
    return word

def fix_palatalization(word):
    word = word.replace("ь", "j")
    for c in cyr_consonants.values():
        word = word.replace(c + ' j', c + 'ʲ')
    word = word.replace(' ʲ', 'ʲ')
    word = word.replace('ʲʲ', 'ʲ')
    word = word.replace('g i', 'ɢ i')
    #word = word.replace('gʲ', 'g')
    word = word.replace('j i', 'i')
    word = word.replace(' ъ', '')
    return word
    
def apocopate(word):
    if word.endswith('n'):
        word = word[:-1]+'ŋ'
    for v in short_vowels:
        if word.endswith('j ' +v):
            word = word[:-2]
        elif word.endswith('n ' + v):
            word = word[:-2]       
        elif word.endswith('g ' +v):
            word = word[:-3]+ 'ɢ'
        elif word.endswith('x ' + v):
            word = word[:-3]+ 'χ'

    return word

def enforce_velar_agr(word):
    segs = word.split(' ')
    if 'g' in word or 'x' in word: 
        if len(set(segs)&set(vowels_nophar))>0:
            pass
        elif not word.endswith('g') and len(set(segs)&set(vowels_phar))>0:
            word = word.replace('g', 'ɢ')
            word = word.replace('x', 'χ')
        elif len(set(segs)&set(vowels_phar))>0:
            word = word.replace('x', 'χ')
            head = word[:-2]
            head = head.replace('g', 'ɢ')
            word = head+word[-2:]
    word = re.sub('n ([kgx])', 'ŋ \\1', word)
    word = re.sub('n ([χɢ])', 'ɴ \\1', word)
    return word

def vowel_length(word):
    '''
    vowel length contrasts phonologically in the first syllable only
    in subsequent syllables, double orthog vowels are short, and single orthog vowels are reduced
    '''
    word = word.replace('aaa', 'aa a')
    v_tier = [x for x in word.split(' ') if x in vowels]
    if len(v_tier) in [0,1]:
        return word
    else:
        v1 = v_tier[0]
        if word.startswith(v1):
            ons = ''
            tail = re.search("^("+v1+" )(.*)",word).group(2)
        else:
            ons = word.split(v1)[0]
            tail = re.search("("+v1+" )(.*)",word).group(2) 
        for v in list(set(v_tier[1:])):
            short = v[0]
            if len(v)==2:
                tail = tail.replace(v, short)
            else:
                tail = re.sub(' '+v+' ', ' ə ', tail)
        if v1 == 'e': #orthographic short э in first syllable stands for i
            v1='i'
        word = ''.join([ons, v1, ' ', tail])
        return word

#a final sonorant must be preceded by a vowel:

vowels.append('ə')

always_epenth = ['j','w','wʲ','r','rʲ','n','nʲ','m','mʲ', 'ɮ','ɮʲ', 'ŋ']
fin_obs = ['tʰ', 'ʃ' ,'s','t','ʧʰ', 'ʧ','ʦ', 'ʦʰ', 'x', 'xʲ']


good_obs_clusters = ['ʃ tʰ', 's tʰ', 's ʧʰ', 'x ʧʰ', 'x tʰ', 'xʲ tʰ', 'ɢ tʰ', 'g tʰ', 'g ʧʰ', 'g ʦʰ', 'g t', 'g ʧ', 'g ʦ', 'g s', 'g ʃ']
 

def epenthesis(word):
    segs = word.split(' ')
    final_seq = ' '.join(segs[-2:])
    if final_seq in good_obs_clusters:
        pass
    elif len(segs)>3 and not segs[-2] in vowels:
        if segs[-1] in always_epenth:
            word = ' '.join(segs[:-1]) + ' ə '+ segs[-1]
        elif segs[-1] in fin_obs and segs[-2] in fin_obs:
            word = ' '.join(segs[:-1]) + ' ə ' + segs[-1]
        elif segs[-2]=='ŋ' and not segs[-1] in ['ʃ', 'x', 'g', 'gʲ', 'ɢ']:
            word = ' '.join(segs[:-1]) + ' ə ' + segs[-1]
    return word

def pal_cleanup(word):
    word = re.sub('([χʧjʦɢʃs]ʰ*)ʲ', '\\1', word)
    return word

def transcribe_word(word):
    word = spacify(word)
    word = transcribe_vowels(word)
    word = transcribe_consonants(word)
    word = fix_palatalization(word)
    word = apocopate(word)
    word = vowel_length(word)
    word = enforce_velar_agr(word)
    word = epenthesis(word)
    word = pal_cleanup(word)
    return word



def transcribe_wlist(infile, outfile):
	with open(infile, 'r', encoding='utf-8') as f:
		with open(outfile, 'w', encoding='utf-8') as out:
			for word in f:
				#out.write(transcribe_word(word.strip())+'\t' + word)
                                out.write(transcribe_word(word.strip())+'\n')
	print('done') 


if __name__ == '__main__':
	import sys
	transcribe_wlist(sys.argv[1], sys.argv[2])


