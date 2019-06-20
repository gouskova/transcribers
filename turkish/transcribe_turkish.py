#!/usr/bin/env python3
# coding: utf-8

pairs = {"g @":	'ɟ',
        "i @": 'ɯ',
        "k @": 'c',
        "l @": 'ʎ',
        "o @": 'ø',
        "u @": 'y',
        "a @": 'aː',
        "c @": 't ʃ',
        "s @": "ʃ",
        "y @": "yː", 
        "ɯ @": "ɯː"}


with open('tell.txt', 'r') as f:
    with open('LearningData.txt', 'w', encoding='utf-8') as out:
        for line in f:
            line = line.strip().split('\t')
            for word in line[5:]:
                if word in ['0', '1', 'y', 'n', '?', '', 'l', 'u'] or '-' in word:
                    continue
                else:
                        word = ' '.join(list(word.lower())).lstrip("?").strip()
                        word = word.replace('j', 'ʒ') #abajur
                        word = word.replace('y', 'j')
                        for dig in pairs:
                            word = word.replace(dig, pairs[dig])
                        word = word.replace('c', 'd ʒ')
                        word = word.replace(' :', 'ː').replace("' ", "")
                        word = word.replace('g', 'ɡ')
                if "~" in word: #only the first of the two variants preserved
                    word = word.split("~")
                    out.write(word[0].strip()+'\n')
                elif "*" in word:
                    word = word.split("*")
                    out.write(word[0].strip()+'\n')
                else:
                    out.write(word+'\n')

