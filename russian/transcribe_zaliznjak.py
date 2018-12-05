#!usr/bin/env python3
# -*- coding: utf-8 -*-

from transcriber_russ import *
import os


#workdir = os.path.expanduser('~/Documents/Dropbox/work/dictionaries/russian_dictionaries/morphology/')
#os.chdir(workdir)


infile= open("/home/maria/git/morphology/russian/input/zaliznjak_paradigms.txt", 'r', encoding='utf-8')
outfile=open("/home/maria/Desktop/transcribed_paradigms.txt", 'w', encoding='utf-8')


#outfile.write("cyrillic\t cyr_w_stress\t IPA\n")

for line in infile:
    line=line.strip('/n').split(",")
    if len(line)==1:
        outfile.write("%s \t %s \t %s\n" % (line[0], "", transcribe(line[0],  stress="threeway", spaces = "no", voice="yes", reduction="no")))

    else:
        trans = '\t'.join([transcribe(x, stress='threeway', spaces='no', voice='yes', reduction='no') for x in line])
        #outfile.write("%s \t %s \t %s\n" % (line[0], line[1], transcribe(line[1],  stress="threeway", spaces = "no", voice="yes", reduction="no")))
        outfile.write("%s \t %s\t %s\n" % (line[0], line[1], trans))
infile.close()
outfile.close()
