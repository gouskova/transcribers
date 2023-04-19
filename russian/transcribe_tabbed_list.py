#!usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
from transcriber_russ import *

basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
morphpath = os.path.join(basedir, 'transcribers')


#infile = open("/home/maria/Desktop/adjs_cyr.txt", "r", encoding='utf-8')
infile = open("/home/maria/Desktop/atyj_cyr.csv", "r", encoding='utf-8')
outfile =open('/home/maria/Desktop/atyj_ipa.txt', 'w', encoding='utf-8')


for line in infile:
    outline=[]
    try:
        line = line.strip('/n').split('\t')
        for word in line:
            outline.append(transcribe(word, stress="off", spaces="yes", voice="no", reduction="no")) 
        outfile.write("%s\n" % "\t".join(outline))
    except IndexError:
        print(line)
        break
infile.close()
outfile.close()
