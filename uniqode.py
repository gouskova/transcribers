#!/usr/bin/env python3
# coding: utf-8

'''
a python3 utility to create a copy of a file that eliminates duplicate lines. similar to the bash 'uniq' command except that it works on UTF-8 encoded files.

usage: 

$ pyuniq infile.txt

this will create a copy of infile.txt called infile_uniq.txt, in the same directory as infile.txt
'''

def unique(infile):
    wordset = set()
    if infile.endswith('.txt') and len(infile.split('.txt'))==2:
        outpath = infile.split('.txt')[0]+'_uniq.txt'
    else:
        outpath = input('Please enter the name of the file to write the output to (e.g., "LearningData_uniq.txt". Warning: if this file exists and is in the same directory as the input file, it will be overwritten without a prompt.')
    with open(infile, 'r', encoding='utf-8') as f:
       with open(outpath, 'w', encoding='utf-8') as out:
            for line in f:
                if line in wordset:
                    pass
                else:
                    out.write(line)
                    wordset.add(line)
    print('wrote a uniq version of '+ infile + " to " + outpath)


if __name__=='__main__':
    import sys
    try:
        unique(sys.argv[1])
    except FileNotFoundError:
        print("file " + sys.argv[1] + " does not exist.")

