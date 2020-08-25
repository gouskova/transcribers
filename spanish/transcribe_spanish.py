#!/usr/bin/env python3

import re

def unordered_transkey(**kwargs):
    '''
    this assumes no ordering logic. for an ordered transcriber, see 'ordered_transcribe'
    it takes in a tab-separated file with 
    ortho \tab ipa
    and returns a dictionary that has orthog symbols as keys and ipa correspondences as values
    '''
    ipatable=kwargs['transkey']
    transkey = {}
    with open(ipatable, 'r', encoding='utf-8') as f:
        for line in f:
            if not line=='':
                ortho = line.strip('\n').split('\t')[0]
                ipa = line.strip('\n').split('\t')[1]
                transkey[ortho]=ipa
    return transkey


def ordered_transkey(**kwargs):
    '''
    for sucky orthographies like russian where the same symbols stand for different sounds depending on context.
    this is like unordered_transkey except the output is 
    {1: [a, b], 2: [x, y} etc.
    '''
    ipatable=kwargs['transkey']
    transkey = {}
    c = 1
    with open(ipatable, 'r', encoding='utf-8') as f:
        for line in f:
            if not line=='':
                transkey[c]=[line.strip('\n').split('\t')[0], line.strip('\n').split('\t')[1]]
            c+=1
    return transkey

def transcribe_wd(**kwargs):
    '''
    replaces orthographic symbols with their IPA values, given an IPA table of them
    '''
    transkey = kwargs['transkey'] # a dictionary of ortho and ipa values
    word = kwargs['word']
    ordered = kwargs['ordered']
    spaces = kwargs['spaces']
    if not type(transkey)==dict: #if function called from command line on a single word
        if ordered:
            transkey = ordered_transkey(**kwargs)
        else:
            transkey = unordered_transkey(**kwargs)
    if ordered:
        for k in sorted(transkey):
            word = word.replace(transkey[k][0], transkey[k][1])
        word = re.sub('(c) ([ieíé])', 's \\2', word)
        word = word.replace('c', 'k') #should be just k a, k u, k o, k l, etc. left
        word = word.replace('z', 's') #assuming mexican not peninsular
        word = re.sub('^β', 'b', word)
        word = re.sub('^ð', 'd', word)
        word = re.sub('^ɣ', 'ɡ', word)
        word = word.replace('m β', 'm b')
        word = word.replace('n ð', 'n d')
        word = word.replace('h', '')
        return word 
    else:
        for k, v in transkey.items():
            word = word.replace(k, v)
        if spaces:
            return ' '.join(list(word))
        else:
            return word


def transcribe_wds(**kwargs):
    '''
    takes in an orthography file and writes an IPA transcription file
    '''
    ordered = kwargs['ordered']
    takefirstcolumn = kwargs['takefirstcolumn']
    ipatable = kwargs['transkey']
    infile = kwargs['infile']
    outfile = kwargs['outfile']
    spaces = kwargs['spaces']
    side = kwargs['sidebyside']
    if ordered:
        transkey = ordered_transkey(**kwargs)
    else:
        transkey = unordered_transkey(**kwargs)
    kwargs['transkey']=transkey
    with open(infile, 'r', encoding='utf-8') as f:
        with open(outfile, 'w', encoding='utf-8') as out:
            for line in f:
                if takefirstcolumn or side:
                    kwargs['word']=line.strip('\n').split('\t')[0]
                    if takefirstcolumn:
                        rest = line.strip('\n').split('\t')[1:]
                    elif side:
                        rest = kwargs['word']
                    out.write('\t'.join([transcribe_wd(**kwargs), rest])+'\n')
                else:
                    kwargs['word']=line.strip('\n')
                    out.write(transcribe_wd(**kwargs)+'\n')



if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser(description="A command-line utility for transcribing orthography into IPA.")
    parser.add_argument('--ordered', help="If set, the learner will apply substitutions from the transcription key in the given order. Otherwise the substitutions are unordered.", dest='ordered', action='store_true')
    parser.add_argument('--infile', help='the .txt file to be transcribed.')
    parser.add_argument('--outfile', help='the file where output is going to be written. Existing file with that name will be overwritten without a prompt.')
    parser.add_argument('--transkey', help='the location of a tab-separated transcription key, with orthographic value in first column and ipa correspondence in 2nd. rest of file gets ignored.', default='transcription_key.txt')
    parser.add_argument('--spaces', help='True or False; if true, spaces are inserted between characters.', default=False, type=bool)
    parser.add_argument('--sidebyside', help='True or False; if true, writes IPA-column \tab ortho-column in ouput', default=False, type=bool)
    parser.add_argument('--takefirstcolumn', help="True or False; if True, transcribes the first column of the input file and writes the remainder to the outfile in the original form", default=False, type=bool)
    parser.add_argument('--word', help='provide a word along with a transkey file to see its transcription: $ python3 generic_transcriber.py --word szykaj --transkey /home/Desktop/polish/transcription_key.txt')
    args = parser.parse_args()
    kwargs = vars(args)
    if not args.ordered:
        kwargs['ordered']=False
    if args.word:
        print(transcribe_wd(**kwargs))
    else:
        transcribe_wds(**kwargs)

