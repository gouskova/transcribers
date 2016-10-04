#!usr/bin/env python3
# -*- coding: utf-8 -*-

from transcriber_russ import *


infile= open("zaliznjak_paradigms.txt", 'r', encoding='utf-8')
outfile=open("/Users/maria/git/phonotactics/test_runs/russian/user_input_files/LearningData.txt", 'w', encoding='utf-8')


for line in infile:
	line=line.strip('\n').split(",")
	if len(line)==1:
		withstress = line[0]
	else:
		cyrword = line[0]
		withstress = line[1]
		ipa = transcribe(withstress, stress = "threeway", spaces="yes", voice='yes', reduction='yes')
		transcription = UCLAPL_transcribe(ipa, 'stress')
	#	transcription=ipa
	outfile.write(transcription+'\n')

infile.close()
outfile.close()
