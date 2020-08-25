with open('headwords.txt', 'r', encoding='utf-8') as f:
    with open('headwords_cleaned.txt', 'w', encoding='utf-8') as out:
        for line in f:
            word = ' '.join(list(line.split(',')[0]))
            out.write(word+'\n')

