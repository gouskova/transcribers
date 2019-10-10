#!/usr/bin/env python3
# coding: utf-8

import xml.etree.ElementTree as ET

wds = ET.parse('german-dictionary.xml')
root = wds.getroot()

ipa = set()

for child in root.findall('lexeme'):
    ipa.add(child.find('phoneme').text)
    

with open('LearningData.txt', 'w', encoding='utf-8') as f:
    for word in sorted(ipa):
        word = word.replace("V", 'u:')
        word = word.replace('t͡s', 'ts')
        word = ' '.join(list(word))
        word = word.replace(" ː", ":")
        word = word.replace(" ̯", "")
        if not 'θ' in word and not 'w' in word:
            f.write(f'{word}\n')
print('done')


