bad_chars = set("' + . 2 q ß à á â ä å æ ç è é ê ë í î ð ñ ô ö ø ú ü þ ā č ē ě ī ı ō ŏ ő ř ş š ū ’".split(" "))

with open('polimorf.txt', 'r', encoding='utf-8') as f:
    with open('polimorf_clean.txt', 'w', encoding='utf-8') as out:
        for word in f:
            if set(word) & bad_chars:
                continue
            else:
                out.write(word)

