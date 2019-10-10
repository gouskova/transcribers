import os

workdir = os.environ['POLEX'] 

rawfiles = [x for x in os.listdir(workdir) if x.endswith('.PLX')]


words = set()
for fi in rawfiles:
    with open(os.path.join(workdir, fi), 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            words.add(line.split(';')[0])

words = {x for x in words if not x.startswith('%') and not x==''}


with open('ortho_polex.txt', 'w', encoding='utf-8') as f:
    for word in sorted(words):
        f.write(word+'\n')


