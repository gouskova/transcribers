#!usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
from transcriber_russ import *

basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
morphpath = os.path.join(basedir, 'transcribers')


#infile= open(os.path.join(morphpath, "russian/zaliznjak_db.txt"), 'r', encoding='utf-8')
#outfile=open(os.path.join(morphpath, "russian/transcribed_zalinjak_db.txt"), 'w', encoding='utf-8')

infile= open(os.path.join(morphpath, "russian/tikhonov.txt"), 'r', encoding='utf-8')
outfile=open(os.path.join(morphpath, "russian/LearningData_tikho.txt"), 'w', encoding='utf-8')



for line in infile:
    #line=line.strip('/n').split(",")
    try:
        line = line.strip('/n').split(' | ')
        word = line[1].split(' ')[0]
        outfile.write("%s\n" % (transcribe(word,  stress="off", spaces = "yes", voice="yes", reduction="no")))
    except IndexError:
        print(line)
        break
infile.close()
outfile.close()
