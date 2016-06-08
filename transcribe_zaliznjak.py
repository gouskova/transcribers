#!usr/bin/env python3
# -*- coding: utf-8 -*-

from transcriber import *
import os


workdir = os.path.expanduser('~/Documents/Dropbox/work/dictionaries/russian_dictionaries/morphology/')
os.chdir(workdir)


infile= open("zaliznjak_paradigms.txt", 'r', encoding='utf-8')
outfile=open("transcribed_citation.txt", 'w', encoding='utf-8')


outfile.write("cyrillic\t cyr_w_stress\t IPA\n")

for line in infile:
    line=line.strip('/n').split(",")
    if len(line)==1:
        outfile.write("%s \t %s \t %s\n" % (line[0], "", transcribe(line[0],  stress="threeway", spaces = "no", voice="yes", reduction="no")))

    else:
        outfile.write("%s \t %s \t %s\n" % (line[0], line[1], transcribe(line[1],  stress="threeway", spaces = "no", voice="yes", reduction="no")))

infile.close()
outfile.close()
