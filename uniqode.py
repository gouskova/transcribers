#!/usr/bin/env python3
# coding: utf-8

'''
a python3 utility to create a copy of a file that eliminates duplicate lines. similar to the bash 'uniq' command except that it works on UTF-8 encoded files.

copy it to your bin directory as uniqode, and then do:

$ uniqode infile.txt

by default this will create a copy of infile.txt called infile_uniq.txt, in the same directory as infile.txt

if you want to name the file something else, give the util second argument:

$ uniqode infile.whatevs outfile.somestuff

'''

def unique(infile, outfile):
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
    if len(sys.argv)==2:
        try:
            unique(sys.argv[1])
        except FileNotFoundError:
            print("file " + sys.argv[1] + " does not exist.")
    elif len(sys.argv)==3:
            print("file " + sys.argv[2] + ' will be overwritten if it exists.')  
            try:
                unique(sys.argv[1], sys.argv[2])
            except FileNotFoundError:
                print("file " + sys.argv[1] + " does not exist.")

