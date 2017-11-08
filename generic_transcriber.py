#!/usr/bin/env python3

def transc_table(ipatable):
    transkey = {}
    with open(ipatable, 'r', encoding='utf-8') as f:
        for line in f:
            ortho = line.strip().split('\t')[0]
            ipa = line.strip().split('\t')[1]
            transkey[ortho]=ipa
    return transkey


def transcribe_wds(ipatable, infile, outfile):
    transkey = transc_table(ipatable)
    with open(infile, 'r', encoding='utf-8') as f:
        with open(outfile, 'w', encoding='utf-8') as out:
            for line in f:
                word = line.strip().split('\t')[0].split(' ')
                out.write(' '.join([transkey[ortho] if ortho in transkey else ortho for ortho in word])+ '\n')
    print('done')



if __name__=='__main__':
    import sys
    try:    
        ipatable = sys.argv[1]
        infile = sys.argv[2]
        outfile = sys.argv[3]
        transcribe_wds(ipatable, infile, outfile)
        print ('your transcribed file is in ' + outfile)
    except IndexError:
        print ('Usage: python3 generic_transcriber.py fullpathtoIPAtable fullpathtoInfile fullpathtoOutfile')

