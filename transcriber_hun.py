#!usr/bin/env python3
# -*- coding: utf-8 -*

# This is a script providing functions for transcribing a list of (lowercase) words written in Hungarian orthography into a UCLA Phonotactic Learner input, IPA and Minimal Generalization Learner input format. It incorporates phenomena like voicing assimilation, palatal assimilation and degemination.
# =======================================================================
# timing the script
# =======================================================================
#import time
#start_time = time.time()


# =======================================================================
# basic housekeeping for the input. add spaces
# =======================================================================
def spacify(word):
    word = word.replace(word, str(word))
    word = unicode(word, 'utf8')
    low_word = word.lower()
    chars = list(low_word)
    for char in chars:
        char = char.replace(char, char + ' ')
    word = " ".join(chars)
    return word


# ===================================================
# transcribing consonants -- step 1, digraphs into unigraphs and miscellaneous segments (x, q, qu, w)
# ===================================================
step1_digr_misc = {
    u"t y": u"T",
    u"g y": u"D",
    # "d z" : "q",
    u"c s": u"C",
    u"s z": u"RRR",  # interim solution, so that transcribing all "s"'es won't interfere
    u"z s": u"Z",
    u"c h": u"h",
    u"n y": u"N",
    u"l_y": u"j",
    # miscellaneous
    u"x": u"k sz",
    u"q u": u"k",
    u"w": u"v"}


def do_step1(word):
    for char in step1_digr_misc.keys():
        word = word.replace(char, step1_digr_misc[char])
    return word


# ===================================================
# transcribing consonants -- step 1b, corrections for s-sz and q-dz
# ===================================================
step1b_corr = {
    u"d z": u"q",  # we cannot convert things into q's before misc
    u"s": u"S"}


def do_step1b(word):
    for char in step1b_corr.keys():
        word = word.replace(char, step1b_corr[char])
    return word


# ===================================================
# transcribing consonants -- step 2, digraphs for long consonants
# ===================================================
step2_longdigraph = {
    u"t T": u"TT",
    u"t j": u"TT",
    u"T j": u"TT",
    u"g D": u"DD",
    u"d j": u"DD",
    u"D j": u"DD",
    u"d Z": u"QQ",
    u"c C": u"CC",
    u"t RRR": u"cc",
    u"t S": u"CC",
    u"d q": u"qq",
    u"S RRR": u"ss",
    u"z Z": u"ZZ",
    u"c h": u"hh",
    u"n N": u"NN",
    u"N j": u"NN",
    u"l j": u"jj",
    u"n j": u"NN",
    u"l j": u"jj"}


def do_step2(word):
    for char in step2_longdigraph.keys():
        word = word.replace(char, step2_longdigraph[char])
    return word


# ===================================================
# transcribing consonants -- step 1b, corrections for s-sz and q-dz
# ===================================================
step2b_corr = {
    u"RRR": u"s",  # to give 'sz' [s]'s their final form
    u"y": u"i"}  # whatever y is not part of a digraph (remained a y after step1), is an i


def do_step2b(word):
    for char in step2b_corr.keys():
        word = word.replace(char, step2b_corr[char])
    return word


# ===================================================
# transcribing consonants -- step 3, long unigraph consonants
# ===================================================
step3_longunigraph = {
    u"p p": u"pp",
    u"t t": u"tt",
    u"k k": u"kk",
    u"b b": u"bb",
    u"d d": u"dd",
    u"g g": u"gg",
    u"c c": u"cc",
    u"f f": u"ff",
    u"v v": u"vv",
    u"z z": u"zz",
    u"h h": u"hh",
    u"m m": u"mm",
    u"n n": u"nn",
    u"l l": u"ll",
    u"r r": u"rr",
    u"j j": u"jj"}


def do_step3(word):
    for char in step3_longunigraph.keys():
        word = word.replace(char, step3_longunigraph[char])
    return word


# ===================================================
# transcribing vowels
# ===================================================
vowels_shortlong = {
    u"á": u"aa",
    u"é": u"ee",
    u"í": u"ii",
    u"ó": u"oo",
    u"ö": u"2",
    u"ő": u"22",
    u"ú": u"uu",
    u"ü": u"y",
    u"ű": u"yy"}


def do_vowels(word):
    for char in vowels_shortlong.keys():
        word = word.replace(char, vowels_shortlong[char])
    return word


# ===================================================
# voicing assimilation:
# ===================================================
always_voiceless = [u"h", u"hh"]

devoiced_pair = {
    u"b": u"p",
    u"d": u"t",
    u"D": u"T",
    u"ɡ": u"k",
    u"v": u"f",
    u"z": u"s",
    u"Z": u"S",
    u"q": u"c",
    u"Q": u"C"
}

voiced_pair = dict((key, value) for (value, key) in devoiced_pair.items())
voiceless = always_voiceless + list(devoiced_pair.values())
del voiced_pair[u"f"]


# =======================================================================
# a little utility function that creates a dictionary of UR/SR correspondences for voicing agreement
# =======================================================================
def make_agree():
    make_clusters = {}
    for voiced in devoiced_pair.keys():  # leftward spread of voicelessness--all dp it
        for vless in voiceless:
            if devoiced_pair[voiced] == vless:
                make_clusters[voiced + " " + vless] = vless + vless
            else:
                make_clusters[voiced + " " + vless] = devoiced_pair[voiced] + " " + vless
    for vless in voiced_pair.keys():  # leftward spread of voicing: [v] doesn't trigger
        for voiced in voiced_pair.values():
            if voiced_pair[vless] == voiced:
                make_clusters[vless + " " + voiced] = voiced + voiced
            else:
                make_clusters[vless + " " + voiced] = voiced_pair[vless] + " " + voiced
    return make_clusters


agree_clusters = make_agree()


def voicing(word):
    """Applies word-final devoicing rule to obstruents, and regressive voicing agreement to obstruent clusters"""
    for cluster in agree_clusters.keys():
        word = word.replace(cluster, agree_clusters[cluster])
    return word


# ===================================================
# the transcription function -- putting the pieces together. it has to be broken down into so many pieces because of the many digraphs and also because a unigraph (s) needs to be replaced too
# ===================================================
degem_pair = {
    u"pp": u"p",
    u"bb": u"b",
    u"tt": u"t",
    u"dd": u"d",
    u"TT": u"T",
    u"DD": u"D",
    u"kk": u"k",
    u"gg": u"g",
    u"cc": u"c",
    u"qq": u"q",
    u"CC": u"C",
    u"QQ": u"Q",
    u"ff": u"f",
    u"vv": u"v",
    u"ss": u"s",
    u"zz": u"z",
    u"SS": u"S",
    u"ZZ": u"Z",
    u"hh": u"h",
    u"mm": u"m",
    u"nn": u"n",
    u"NN": u"N",
    u"ll": u"l",
    u"rr": u"r",
    u"jj": u"j"}

consonants = [u"p", u"b", u"t", u"d", u"T", u"D", u"k", u"g", u"c", u"q", u"C", u"Q", u"f", u"v", u"s", u"z", u"S",
              u"Z", u"h", u"m", u"n", u"N", u"l", u"r", u"j"]


def elim_geminates():
    gem_clusters = {}
    for gem in degem_pair.keys():  # leftward spread of voicelessness--all dp it
        for cons in consonants:
            gem_clusters[gem + " " + cons] = degem_pair[gem] + " " + cons
            gem_clusters[cons + " " + gem] = cons + " " + degem_pair[gem]
    return gem_clusters


degem = elim_geminates()


def degeminate(word):
    for cluster in degem.keys():
        word = word.replace(cluster, degem[cluster])
    return word


# ===================================================
# function transcribing UCLAPL input into IPA
# ===================================================
IPA_precleaning = {
    u"c": u"WW",
    u"cc": u"WWWW",
    u"a": u"XX"}

def do_ipa_preclean(word):
    for char in IPA_precleaning.keys():
        word = word.replace(char, IPA_precleaning[char])
    return word

IPA_corresp_long = {
    u"XXXX": u"aː",
    u"ee": u"eː",
    u"ii": u"iː",
    u"oo": u"oː",
    u"22": u"øː",
    u"uu": u"uː",
    u"yy": u"yː",
    u"pp": u"pː",
    u"bb": u"bː",
    u"tt": u"tː",
    u"dd": u"dː",
    u"TT": u"cː",
    u"DD": u"ɟː",
    u"kk": u"kː",
    u"gg": u"gː",
    u"ff": u"fː",
    u"vv": u"vː",
    u"ss": u"sː",
    u"zz": u"zː",
    u"SS": u"ʃː",
    u"ZZ": u"ʒː",
    u"hh": u"hː",
    u"WWWW": u"ʦː",
    u"qq": u"dzː",
    u"CC": u"ʧː",
    u"QQ": u"dʒː",
    u"mm": u"mː",
    u"nn": u"nː",
    u"NN": u"ɲː",
    u"ll": u"lː",
    u"rr": u"rː",
    u"jj": u"jː"}

IPA_corresp_short = {
    u"XX": u"ɒ",
    u"e": u"ɛ",
    u"2": u"ø",
    u"T": u"c",
    u"D": u"ɟ",
    u"S": u"ʃ",
    u"Z": u"ʒ",
    u"WW": u"ʦ",
    u"q": u"dz",
    u"C": u"ʧ",
    u"Q": u"dʒ",
    u"N": u"ɲ"}


def ipafy(word):
    for char in IPA_corresp_long.keys():
        word = word.replace(char, IPA_corresp_long[char])
    for char in IPA_corresp_short.keys():
        word = word.replace(char, IPA_corresp_short[char])
    word = u"ˈ" + word.replace(" ", "")
    return word


# ===================================================
# function transcribing UCLAPL input into IPA
# ===================================================
mgl_corresp_vowel_palat_long = {
    u"aa": u"A",
    u"ee": u"E",
    u"ii": u"I",
    u"oo": u"O",
    u"22": u"3",
    u"uu": u"U",
    u"yy": u"Y",
    u"CC": u"X",
    u"QQ": u"W",
    u"TT": u")",
    u"DD": u"]",
    u"SS": u">",
    u"ZZ": u"}",
    u"NN": u"_"}

mgl_corresp_vowel_palat_short = {
    u"C": u"x",
    u"Q": u"w",
    u"T": u"(",
    u"D": u"[",
    u"S": u"<",
    u"Z": u"{",
    u"N": u"-"}

mgl_corresp_reg_cons = {
    u"pp": u"P",
    u"bb": u"B",
    u"tt": u"T",
    u"dd": u"D",
    u"kk": u"K",
    u"gg": u"G",
    u"qq": u"Q",
    u"cc": u"C",
    u"ff": u"F",
    u"vv": u"V",
    u"ss": u"S",
    u"zz": u"Z",
    u"hh": u"H",
    u"mm": u"M",
    u"nn": u"N",
    u"rr": u"R",
    u"ll": u"L",
    u"jj": u"J"}


def mglify(word):
    for char in mgl_corresp_vowel_palat_long.keys():
        word = word.replace(char, mgl_corresp_vowel_palat_long[char])
    for char in mgl_corresp_vowel_palat_short.keys():
        word = word.replace(char, mgl_corresp_vowel_palat_short[char])
    for char in mgl_corresp_reg_cons.keys():
        word = word.replace(char, mgl_corresp_reg_cons[char])
    word = word.replace(" ", "")
    return word

# ===================================================
# the transcription function -- putting the pieces together. it has to be broken down into so many pieces because of the many digraphs and also because a unigraph (s) needs to be replaced too
# ===================================================
def transcribe(word, IPA, MGL):
    word = spacify(word)
    word = do_step1(word)
    word = do_step1b(word)
    word = do_step2(word)
    word = do_step2b(word)
    word = do_step3(word)
    word = do_vowels(word)
    word = voicing(word)
    word = degeminate(word)
    if IPA == "yes":
        word = do_ipa_preclean(word)
        word = ipafy(word)
    if MGL == "yes":
        word = mglify(word)
    return word


# ===================================================
# providing the list to be transcribed -- it needs a list of words as input, named wordlist
# ===================================================
import csv

wordlist = []
with open('C:\Users\ildi\Dropbox\NYELVESZET\PROJECTS\Tiers\Transcriber_hun\hun_roots.csv') as f:
    reader = csv.reader(f, delimiter="\t")
    for row in reader:
        wordlist.append(row[0])

# ===================================================
# the transcription itself with saving
# ===================================================
wordlist_trans = []
for word in wordlist:
    trans_word = transcribe(word, "no", "no")
    wordlist_trans.append(trans_word)

import codecs

text_file = codecs.open("hun_UCLAPL_roots.txt", "w", "utf-8")
#text_file = codecs.open("hun_IPA_roots.txt", "w", "utf-8")
#text_file = codecs.open("hun_MGL_roots.txt", "w", "utf-8")
for item in wordlist_trans:
    text_file.write(item)
    text_file.write("\n")
text_file.close()

#print wordlist_trans[0:100]
#print("--- %s seconds ---" % (time.time() - start_time))
