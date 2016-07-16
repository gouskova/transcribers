#!usr/bin/env python3
# -*- coding: utf-8 -*-

#this module supplies functions and options for converting Russian Cyrillic into IPA, with or without voicing rules and unstressed vowel reduction as in the standard (Moscow) dialect. It will also convert the orthography to a pseudotranscription compatible with the Minimal Generalization Learner as well as the UCLA Phonotactic Learner.

#the module is compatible with morpheme boundary marking as in Tikhonov's dictionary (corrections by Maria Gouskova and Alex Torchio), which we distribute as russian_morphology_dictionary.txt. Morpheme boundaries "/" are replaced with pipes "|" after transcription; this happens in the spacify function and the rest of the module just assumes pipes as boundaries.

#note: several other modules rely on this one. You can copy it to the directory where the dependency is going to look for it, or else copy it to the appropriate sys.path(). On my system, the following steps located the relevant place:

#>>> import sys
#>>> print(sys.path())
#/Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5

# $ cp transcriber_russ.py /Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/


#=======================================================================
# basic housekeeping for the input. add spaces, define some stress digraphs
#=======================================================================

def spacify(word):
	chars = list(word)
	for char in chars:
		char=char.replace(char, char+' ')	
	word =" ".join(chars)
	word = word.replace(" '", "'")
	word = word.replace(" `", "`")
	word = word.replace(" /", " |")
	return word


#=======================================================================
#defining the conversion rules: consonants
#=======================================================================

cyr_ipa_cons = {
	 "б" : "b",
	 "в" : "v",
	 "г" : "ɡ",
	 "д" : "d",
	 "ж" : "ʐ",
	 "з" : "z",
	 "к" : "k",
	 "л" : "l",
	 "м" : "m",
	 "н" : "n",
	 "п" : "p",
	 "р" : "r",
	 "с" : "s",
	 "т" : "t",
	 "ф" : "f",
	 "х" : "x",
	 "ц" : "ʦ",
	 "ч" : "ʧ",
	 "ш" : "ʂ",
	 "щ" : "ʃʃ"}

#=======================================================================
# consonant transcription function
#=======================================================================

def do_consonants(word):
	for char in cyr_ipa_cons.keys():
		word = word.replace(char, cyr_ipa_cons[char])
	return word


#=======================================================================
#defining the conversion rules: vowels, basic cyrillic-to-IPA conversion
#=======================================================================

cyr_ipa_vowels_nostr = {	
	"а" : "a",
	"э" : "e",
	"ы" : "i",
	"о" : "o",
	"у" : "u", 
	"я" : "j a",
	"е" : "j e",
	"ю" : "j u",
	"ё" : "j o'",
	}

#=======================================================================
#defining the conversion rules: primary stress: ' is acute accent, ` is grave
#=======================================================================


ipa_vowels_str = {
	"a'" : "á",
	"e'" : "é",
	"i'" : "í",
	"o'" : "ó",
	"u'" : "ú"}
	
ipa_vowels_secstr = {
	"а`" : "à",
	"e`" : "è",
	"i`" : "ì",
	"o`" : "ò",
	"u`" : "ù"
	}

all_vowels=list(cyr_ipa_vowels_nostr.values())+list(ipa_vowels_str.values())
all_vowels_sec=all_vowels+list(ipa_vowels_secstr.values())

#=======================================================================
#some natural classes for palatalization transcription. some of these classes also used in the vowel reduction rules below, and in the MGL and UCLAPL transcriptions
#=======================================================================

always_velarized=["ʦ","ʐ", "ʂ"]
always_palatalized=["ʃʃ", "ʧ"]
contrastive = ["p", "t", "k", "b", "d", "ɡ", "f", "s", "x", "v", "z", "m", "n", "r", "l"]
float_pal = always_palatalized+contrastive
velarized = contrastive+always_velarized

#=======================================================================
#three separate functions for different desired levels of stress in the output.
#=======================================================================


def nostress_vowels(word):
	"""Removes stress from the transcription, returns orthographic vowel values in IPA"""
	word = word+" "
	word = word.replace("'","").replace("`","")
	word = word.replace("ь и", "ʲ j i")
	word = word.replace("и", "ʲ i")
	word = word.replace("ь | и", "ʲ | j i")
	word = word.replace("| и", "ʲ | i")
	for vowel in cyr_ipa_vowels_nostr.keys():
		word = word.replace(vowel+" ʲ | i", cyr_ipa_vowels_nostr[vowel]+ " | i") 
		word = word.replace(vowel, cyr_ipa_vowels_nostr[vowel])
		word = word.replace(vowel+" ʲ | i", cyr_ipa_vowels_nostr[vowel]+ " | i") 
		word = word.replace(vowel, cyr_ipa_vowels_nostr[vowel])
	word=word.replace("j o'", "j o")
	word=word.lstrip("ʲ ")
	return word.strip()


def twoway_vowels(word):
	"""	Keeps two levels of stress: primary and unstressed (collapsing secondary stress--if present-- with unstressed)."""
	word = word+" "
	word = word.replace("`", "") #just remove sec stress, don't treat it as primary
	word = word.replace("ь и", "ʲ j i")
	word = word.replace("и", "ʲ i")
	word = word.replace("ь | и", "ʲ | j i")
	word = word.replace("| и", "ʲ | i")
	for vowel in cyr_ipa_vowels_nostr.keys():
		word = word.replace(vowel, cyr_ipa_vowels_nostr[vowel])
	for vowel in ipa_vowels_str.keys():
		word=word.replace(vowel, ipa_vowels_str[vowel])
	for vowel in all_vowels:
		word = word.replace(vowel+" ʲ", vowel)
	word=word.lstrip("ʲ ")
	return word.strip()


def threeway_vowels(word):
	"""Keeps all three levels of stress: primary as acute, secondary as grave, and unstressed"""
	word = word+" "
	word = word.replace("ь и", "ʲ j i")
	word = word.replace("ь | и", "ʲ | j i")
	word = word.replace("и", "ʲ i")
	word = word.replace("| и", "ʲ | i")
	for vowel in cyr_ipa_vowels_nostr.keys():
		word = word.replace(vowel, cyr_ipa_vowels_nostr[vowel])
	for vowel in ipa_vowels_str.keys():
		word=word.replace(vowel, ipa_vowels_str[vowel])
	for vowel in ipa_vowels_secstr.keys():
		word=word.replace(vowel, ipa_vowels_secstr[vowel])
	for vowel in all_vowels_sec:
		word = word.replace(vowel+" ʲ", vowel)
	word=word.lstrip("ʲ ")
	return word.strip()

#=======================================================================
# palatalization. this function requires the output of one of the vowels functions above.
#=======================================================================
		
def palatalize(word):
	"""Fixes palatalization, which Cyrillic indicates inconsistently both on the vowel and on the consonant letters. Does not show velarization"""
	word=word.replace("ь", "ʲ")
	for cons in float_pal:
		word = word.replace(cons+" j", cons+"ʲ")
		word = word.replace(cons+"| j", cons+"ʲ |")
	for cons in always_velarized:
		word = word.replace(cons+" j", cons)
		word = word.replace(cons+"ʲ", cons)
	for cons in always_palatalized:
		word = word.replace(cons+" ", cons+"ʲ")
	word=word.replace("ʲ ʲ", "ʲ")
	word=word.replace("ʲʲ", "ʲ")
	word=word.replace("ʲ | ʲ", "ʲ |")
	word=word.replace("ʲ | j", " ʲ |")
	word=word.replace(" ʲ", "ʲ")
	word=word.replace("ъ ", "")
	word=word.replace("й", "j")
	word=word.replace("- ", "-")
	return word




#=======================================================================
#this one calls one of the vowel transcription functions, depending on 
#the user-specified option in the transcribe function.
#=======================================================================
	
def do_vowels(word, stress):
	if stress == "threeway":
		return threeway_vowels(word)
	elif stress == "twoway":
		return twoway_vowels(word)
	elif stress == "off":
		return nostress_vowels(word)


#=======================================================================
#vowel reduction. obviously, requires stress levels to be in the transcribed input in order to work properly. vowels in hiatus sequences are not reduced, because it's not clear that they do in the language
#=======================================================================
def make_reduce_pairs():
	reduce_pairs={}
	reducing_vowels=["e", "a", "o"]
	for vowel in reducing_vowels:
		for cons in velarized:
			reduce_pairs[cons+" " + vowel] = cons+" ə"
		for cons in float_pal:
			reduce_pairs[cons+"ʲ "+vowel] = cons+"ʲ i"
		reduce_pairs["j " + vowel]="j i"	
	return reduce_pairs

reduce_pairs=make_reduce_pairs()

def reduce_vowels(word):
	for CVseq in reduce_pairs.keys():
		word = word.replace(CVseq, reduce_pairs[CVseq])
	if word.startswith("e"):
		word="i" + word.lstrip("e")
	elif word.startswith("o"):
		word="ə" + word.lstrip("o")
	elif word.startswith("a"):
		word="ə" + word.lstrip("a")
	return word

#=======================================================================
#consonant voicing. optional, requires IPA-transcribed input. Russian [v] undergoes devoicing but does not trigger voicing agreement, so the dictionaries for defining agreement mapping are slightly different. Note also that some consonants do not really apear

#=======================================================================

always_voiceless=["x", "ʦ", "ʃʃ", "ʧ"]


devoiced_pair = {
	"b": "p",
	"d": "t",
	"ɡ": "k",
	"v": "f",
	"z": "s",
	"ʐ": "ʂ"
	}

voiced_pair=dict((key, value) for (value, key) in devoiced_pair.items())
voiceless=always_voiceless+list(devoiced_pair.values())
del voiced_pair['f']



#=======================================================================
#a little utility function that creates a dictionary of UR/SR correspondences for voicing agreement
#=======================================================================
def make_agree():
	make_clusters = {}
	for voiced in devoiced_pair.keys(): #leftward spread of voicelessness--all dp it
		for vless in voiceless:
			make_clusters[voiced+" "+vless]=devoiced_pair[voiced]+" " + vless
		if voiced not in always_velarized:
			make_clusters[voiced+"ʲ "+vless]=devoiced_pair[voiced]+"ʲ " + vless
	for vless in voiced_pair.keys(): #leftward spread of voicing: [v] doesn't trigger
		for voiced in voiced_pair.values():
			make_clusters[vless+" " +voiced]=voiced_pair[vless]+ " " + voiced
		if vless not in always_velarized:
			make_clusters[vless+"ʲ " +voiced]=voiced_pair[vless]+ "ʲ " + voiced
	return make_clusters

agree_clusters=make_agree()

#=======================================================================
#devoicing and voicing agreement function
#=======================================================================

def voicing(word):
	"""Applies word-final devoicing rule to obstruents, and regressive voicing agreement to obstruent clusters"""
	for cons in devoiced_pair.keys():
		if word.endswith(cons):
			word = word[:-1]+ word[-1].replace(cons, devoiced_pair[cons])
		if word.endswith(cons+"ʲ"):
			word = word[:-2]+word[-2].replace(cons, devoiced_pair[cons])+"ʲ"
	for cluster in agree_clusters.keys():
		word = word.replace(cluster, agree_clusters[cluster])
	return word


#=======================================================================
#the one function that does everything. note that it requires a list of words as input
#=======================================================================	

def transcribe(word, stress, spaces, voice, reduction):
	"""Transcribes Cyrillic to IPA. Options include stress ("off"=default, "twoway" and "threeway"), adding spaces between sounds ("yes"=default, "no), transcribing devoicing and voicing agreement ("no"=default, "yes"), vowel reduction ("no"=default, "yes")."""
	word = spacify(word)
	word = do_consonants(word)
	word = do_vowels(word, stress)
	word = palatalize(word)
	if voice == "yes":
		word=voicing(word)
	if reduction=="yes":
		word = reduce_vowels(word)
	if spaces == "no":
		word = word.replace(" ", "")
	return word

def transcription_wrapper(input_list, MGL="no", UCLAPL="no", stress="off", spaces = "yes", voice="no", reduction="no"):
	out=[]
	for word in input_list:
		word=transcribe(word, stress, spaces, voice, reduction)
		if MGL=="yes":
			word = MGL_transcribe(word)
		if UCLAPL!="no":
			word = UCLAPL_transcribe(word, UCLAPL)
		out.append(word)
	return out

#================================================================
#substitions for IPA characters, compatible with the Minimal Generalization Learner 
#================================================================
MGL = {
	 "ʦ" : "c",
	 "ʐ" : "Q", 
	 "ʃʃʲ" : "H", 
	 "ʂ" : "h", 
	 "ʧʲ" : "C", 
	 "ɡ" : "g",
	 "á" : "A", 
	 "é" : "E", 
	 "í" : "I", 
	 "ó" : "O", 
	 "ú" : "U", 
	 "à" : "A", 
	 "è" : "E", 
	 "ì" : "I", 
	 "ò" : "O", 
	 "ù" : "U",
	 "ə" : "§"}


def MGL_transcribe(word):
	""" converts IPA transcriptions into Minimal Generalization Learner ascii-only format. See documentation for conversion details"""
	for cons in contrastive:
		word = word.replace(cons+"ʲ", cons.upper())
	for sound in MGL.keys():
		word = word.replace(sound, MGL[sound])
	return word

#================================================================
#substitions for IPA characters, compatible with the UCLA Phonotactic Learner 
#================================================================

	
HWcons = {
	 "ʦ" : "ts",
	 "ʐ" : "zh",
	 "ʃʃʲ" : "shshj", 
	 "ʂ" : "sh", 
	 "ʧ" : "ch", 
	 "ɡ" : "g",
	 "ʲ" : "j",
	 "ə" : "@"}

HWvowelsnostress ={
	 "á" : "a", 
	 "é" : "e", 
	 "í" : "i", 
	 "ó" : "o", 
	 "ú" : "u", 
	 "à" : "a", 
	 "è" : "e", 
	 "ì" : "i", 
	 "ò" : "o", 
	 "ù" : "u"} 

HWvowelstress = {
	 "á" : "A1" , 
	 "é" : "E1" ,
	 "í" : "I1" ,
	 "ó" : "O1" ,
	 "ú" : "U1" ,
	 "à" : "A2" ,
	 "è" : "E2" ,
	 "ì" : "I2" ,
	 "ò" : "O2" ,
	 "ù" : "U2"} 
	 

def UCLAPL_transcribe(word, UCLAPL):
	"""converts IPA to UCLAPL ascii format, with stress (default) or without stress, as defined by the user-supplied UCLAPL parameter. the value is passed from the wrap function
	"""
	for sound in HWcons.keys():
		for cons in contrastive:
			word = word.replace(cons+ "ʲ", cons.upper())
		word = word.replace(sound, HWcons[sound])
	if UCLAPL=="nostress":
		for vowel in HWvowelsnostress.keys():
			word = word.replace(vowel, HWvowelsnostress[vowel])
	elif UCLAPL=="stress":
		for vowel in HWvowelstress.keys():
			word = word.replace(vowel, HWvowelstress[vowel])
	return word