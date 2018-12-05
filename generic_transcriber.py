#!/usr/bin/env python3

def transc_table(ipatable):
    transkey = {}
    with open(ipatable, 'r', encoding='utf-8') as f:
        for line in f:
            if not line=='':
                ortho = line.strip().split('\t')[0]
                ipa = line.strip().split('\t')[1]
                transkey[ortho]=ipa
    return transkey


def transcribe_wds(ipatable, infile, outfile, takefirstcolumn=True):
    transkey = transc_table(ipatable)
    with open(infile, 'r', encoding='utf-8') as f:
        with open(outfile, 'w', encoding='utf-8') as out:
            for line in f:
                if takefirstcolumn:
                    word = line.strip().split('\t')[0].split(' ')
                    out.write(' '.join([transkey[ortho] if ortho in transkey else ortho for ortho in word])+ '\n')
                else:
                    if '\t' in line:
                        words = line.strip().split('\t')
                        newwords = []
                        for word in words:
                            newwords.append(' '.join([transkey[ortho] if ortho in transkey else ortho for ortho in word.split(' ')]))
                        out.write('\t'.join(newwords)+'\n')
                    else:
                        print("Sorry, files must have either one word per line or be in CSV tab-separated columnar format. If the latter, each word will be transcribed in the order it appears in the input file.")

    print('done')



if __name__=='__main__':
    import sys
    try:
        if 'help' in sys.argv:
            print("usage:\n\n$ python3 generic_transcriber.py fullpathtoIPAtable fullpathtoinputfile fullpathtooutputfile\n\n\n if your data file has multiple columns, add 'False' after the other arguments. The script otherwise assumes that you have one line per word.\n\n\n the IPA table file should have two columns; one for orthographic representations and one for IPA correspondents, in that order.")
        else:
            ipatable = sys.argv[1]
            infile = sys.argv[2]
            outfile = sys.argv[3]
            if 'False' in sys.argv:
                transcribe_wds(ipatable, infile, outfile, takefirstcolumn=False)
            else:
                transcribe_wds(ipatable, infile, outfile)
            print ('your transcribed file is in ' + outfile)
    except IndexError:
        print(sys.argv)
        print ('Usage: python3 generic_transcriber.py fullpathtoIPAtable fullpathtoInfile fullpathtoOutfile')

