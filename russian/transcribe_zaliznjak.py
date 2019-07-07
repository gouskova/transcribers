#!usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
from transcriber_russ import *

basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
morphpath = os.path.join(basedir, 'morphology')


infile= open(os.path.join(morphpath, "russian/input/zaliznjak_paradigms.txt", 'r', encoding='utf-8')
outfile=open(os.path.join(morphpath, "transcribed_paradigms.txt", 'w', encoding='utf-8')



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
