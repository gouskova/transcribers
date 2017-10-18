#!usr/bin/env python3

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


quechortho = '/home/maria/git/morphology/quechua/words/words_try3.txt'
quechipa = '/home/maria/git/morphology/quechua/words/words_try3_ipa.txt'
quech_ipa_table = '/home/maria/git/transcribers/quechua/quechua_transcription_key.txt'


transcribe_wds(quech_ipa_table, quechortho, quechipa)

