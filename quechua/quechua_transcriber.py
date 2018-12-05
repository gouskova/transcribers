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
    '''
    this only transcribes the first word on each line! assumes file to be tab-separated. comments, glosses, etc. will be left alone
    '''
    transkey = transc_table(ipatable)
    with open(infile, 'r', encoding='utf-8') as f:
        with open(outfile, 'w', encoding='utf-8') as out:
            for line in f:
                word = line.strip().split('\t')[0].split(' ')
                rest = '\t'.join(line.strip().split('\t')[1:])
                out.write('\t'.join([' '.join([transkey[ortho] if ortho in transkey else ortho for ortho in word]), rest])+'\n')
    print('done')


quech_ipa_table = '/home/maria/git/transcribers/quechua/quechua_transcription_key.txt'

#newspaper words file, segmented:

#quechortho = '/home/maria/git/morphology/quechua/words/NC_type_seg.txt'
#quechipa = '/home/maria/git/morphology/quechua/words/words_ipa.txt'

#roots file:
#quechortho = '/home/maria/git/morphology/quechua/roots/LearningData.txt'
#quechipa = '/home/maria/git/morphology/quechua/roots/roots_ipa.txt'

#unsegmented novela:
#quechortho = '/home/maria/git/morphology/quechua/words/PYW_novela.txt'
#quechipa = '/home/maria/git/morphology/quechua/words/novela_ipa.txt'

#quechortho = '/home/maria/git/phonotactics/data/quechua/wds/LearningData.txt'

quechortho = '/home/maria/git/phonotactics/data/quechua/wds/TestingData_pseudoorth.txt'
quechipa = '/home/maria/Desktop/TestingData.txt'


transcribe_wds(quech_ipa_table, quechortho, quechipa)

