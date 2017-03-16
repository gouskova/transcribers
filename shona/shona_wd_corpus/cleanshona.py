#!usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import itertools

workdir = os.getcwd()

files = [x for x in os.listdir(workdir) if x.startswith('shona')]

#collect all words into a list

shonadic=[]

for file in files:
    wlist = open(file, 'r', encoding= 'utf-8')
    for line in wlist:
        line=line.strip('\n').split(' ')
        for word in line:
            word = word.strip('^,".!?:;').strip("'").lower()
            if not word in shonadic:
                shonadic.append(word)
    wlist.close()

print('length of shonadic ')
print(len(shonadic))


#obtain a list of shona segments that can be defined using our features

shonasegs = []
feats = open('/home/maria/git/phonotactics/data/shona/verbs_chimhundu_ext_segs/Features.txt', 'r', encoding='utf-8')
shonafeats =feats.readlines()[1:]
for line in shonafeats:
    seg = line.split('\t')[0]
    shonasegs.append(seg)
feats.close()


vowels = ['i', 'e', 'a', 'o', 'u']

consonants = [x for x in shonasegs if not x in vowels]

shonadigraphs=['m h','n h','d h','b h','v h', 'c h','s h','p f','s v','z h','z v','b v','n y','d z','d y','t y', 't s']

clusters = [a+' '+ b for (a,b) in list(itertools.product(consonants, repeat=2))]
print('all 2-way combinations of consonants')
print(len(clusters))
#print(clusters)


#these were identified with the help of git/phonotactics/code/datachecker.py, using extended Features.txt on prelim output of this very script

garbagesegs = ['č','ɔ','è','ę','í','ɲ','ə','zvh','ɪ','ā','ː','ɛ','ĉ','β','ó','ŭ','é','ˌ','ō','ê','á','ī','ç','c','ɑ','ớ','ö','l','ú','ū','î','ḥ','â','ô','ŋ','ʊ','ì','à','å','ñ','ï','ë','ý','ă','ü','ã','tsh','ɾ','ž','ǔ','ʻ','ṅ','ð','ṃ','ł','ä','ɓ','š','ɡ']



#now break up every word into spaces according to the existing list of segs 

def spacify(wordlist):
    '''
    takes in a raw word list, one word per line
    outputs something close to UCLAPL LearningData.txt--a dictionary of word and transcription pairs, where transcriptions are files separated by spaces
    '''
    trandic = {}
    garbsegs = set(garbagesegs)
    for word in sorted(wordlist):
        orthoword=word
        trandic[orthoword]={'transcription':'', 'garbage':len(set(word)&garbsegs)>0}
        orthoword = word
        word = word.replace("-", "")
        word = word.replace("\s", "") #spaces left from removing hyphens
        word = word.replace("n'", "N")
        word = word.replace("ng", "Ng")
        word = word.replace(" ", "")
        for seg in word:
            word = word.replace(seg, seg+" ").strip()
            word = word.replace("  ", " ")
        for digraph in shonadigraphs:
            word = word.replace(digraph, digraph.replace(" ",""))
            word = word.replace("ts v", 'tsv')
            word = word.replace("dz v", 'dzv')
            word = word.replace("  ", " ")
        trandic[orthoword]['transcription']=word
    print('number of words with garbage segs: ')
    print(len([x for x in trandic if trandic[x]['garbage']==True]))
    return sorted([trandic[x]['transcription'] for x in trandic if not trandic[x]['garbage']==True]) 



def find_shona_clusters(wlist):
    '''
    assuming that any legal consonant sequences will also occur in nouns and verb stems listed in Chimhundu (that is, no local phonotactic exceptions in morphologically derived environments). none of the sources indicate that this assumption could be problematic

    '''
    clist = {}.fromkeys(clusters, False)
    for cl in clist:
        if clist[cl]==False:
            for wd in wlist:
                if cl in wd:
                    clist[cl]=True
    return sorted(list(set([x for x in clist if clist[x]==True])))


chimhundu = open('chimhundu.txt', 'r', encoding='utf-8')
cleanwds = [x.strip('\n') for x in chimhundu.readlines()]

attested = find_shona_clusters(cleanwds)
chimhundu.close()

print('attested clusters')
print(len(attested))

unattcl = [x for x in clusters if not x in attested]

print('length of unattcl')
print(len(unattcl))
#print(unattcl)

print('length before spacify: '+ str(len(shonadic)))
shonawds = spacify(shonadic)
print('length after spacify: ' + str(len(shonawds)))
#print(shonawds[0:200])

def rm_nonnat_clusters(wdic):
    nativelist = {}.fromkeys(wdic, True) #'keep' is True unless a cluster is found
    for wd in nativelist:
        if nativelist[wd]==True:
            for cl in unattcl:
                if cl in wd:
                    nativelist[wd]=False
    print('length of removed list')
    print(len([wd for wd in nativelist if nativelist[wd]==False]))
    return sorted([wd for wd in nativelist if nativelist[wd]==True])

#reusing the variable because long wordlist

shonadic = rm_nonnat_clusters(shonawds)
print('length of declustered shonadic ' + str(len(shonadic)))

outfile = open("LearningData.txt", 'w', encoding='utf-8')
for wd in shonadic:
    outfile.write(wd+'\n')

outfile.close()



#print(len(shonawds))

#print(spacify(shonadic)[1])


#for orthoword in sorted(shonawds.keys()):
#    orthofile.write(orthoword + '\t' + shonawds[orthoword]['transcription'] +'\t' + ','.join(shonawds[orthoword]['consclusters'])+'\n')
#    outfile.write(shonawds[orthoword]['transcription']+'\n')

#outfile.close()
#orthofile.close()
