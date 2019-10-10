import sys, os, re

sys.path.append(os.path.dirname(os.getcwd()))

import generic_transcriber as gt

tkey = gt.ordered_transkey(transkey='transcription_key.txt')

voiced = ['b', 'd', 'g', 'v', 'z', 'ʐ', 'ʑ']
voiceless = ['p', 't', 'k', 'f', 's', 'ʂ', 'ɕ']
vfmap = dict(zip(voiced, voiceless))
fvmap = dict(zip(voiceless, voiced))

voiceless.extend('x')
fvmap['x']='x'

def transcribe_wd(tkey=tkey, **kwargs):
    '''
    things to do:
    progressive voicing assimilation in onset clusters like prz, sw
    figure out what to do with palatalization
    '''
    word = kwargs['word']
    voice = kwargs['voice']
    vless_obs = ''.join(voiceless)
    voiced_obs = ''.join(voiced)
    for k in tkey:
        word = word.replace(tkey[k][0], tkey[k][1])
    word = word.replace('-', '')
    if voice:
        #progressive assimilation of former sonorants:
        word = re.sub('(['+vless_obs+'])ʐ', '\\1ʂ', word)
        word = re.sub('(['+vless_obs+'])v', '\\1f', word)
        #final devoicing:
        if word[-1] in voiced_obs:
            c = word[-1]
            word = re.sub(c+'$', vfmap[c], word)
        #regressive assimilation of everything else:
        for c in voiced:
            word = re.sub(c+'(['+vless_obs+'])', vfmap[c]+'\\1', word)
        for c in voiceless:
            word = re.sub(c+'(['+voiced_obs+'])', fvmap[c]+'\\1', word)
    word = ' '.join(list(word))
    return word

def transcribe_wds(tkey=tkey, **kwargs):
    infile = kwargs.get('infile')
    outfile = kwargs.get('outfile')
    print(kwargs.get('voice'))
    with open(infile, 'r', encoding='utf-8') as f:
        with open(outfile, 'w', encoding='utf-8') as out:
            for line in f:
                kwargs['word']=line.rstrip('\n')
                word = transcribe_wd(**kwargs)
                out.write(word+'\n')
    print('done')


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description='Polish transcriber with voicing assimilation')
    parser.add_argument('--word', help='transcribes a single-word passed after this argument. as in, "$ python3 polish_transcriber.py --word sweter"')
    parser.add_argument('--infile', help='input file in POLEX orthography', default='ortho_polex.txt')
    parser.add_argument('--outfile', help='output file', default='LearningData.txt')
    parser.add_argument('--voice', help='Transcribes voicing assimilation and devoicing.', dest='voice', action='store_true')
    parser.add_argument('--novoice', help="Voicing is left at orthographic values", dest='voice', action="store_false")
    args = parser.parse_args()
    kwargs = vars(args)
    print(kwargs)
    if args.word:
        transcribe_wd(**kwargs)
    else:
        transcribe_wds(**kwargs)

