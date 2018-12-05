# transcribers
Some utilities for converting orthography into IPA or ASCII formats compatible with several phonological learner programs. 


##Russian
The Russian branch implements phonological rules such as voicing assimilation and vowel reduction in unstressed syllables, and can distinguish up to three degrees of stress marking. Also does UCLA Phonotactic Learner transcription and Minimal Generalization Learner transcription of Russian.

To do: make it work better with morpheme boundaries.

##Generic transcriber

Usage:

python3 generic_transcriber.py path_to_IPA_chart path_to_orig_file path_to_IPA_outfile

paths should be full. An example of an IPA chart:



jy	  ɟ

ny	  ɲ

ng	  ŋ

sy	  ç

ts	  ʦ

ch	  ʧ

sh	  ʃ

zh	  ʒ


An example of the original file to be converted to IPA:




a b a n a

a b a ny a r u k i k o

a b i r a

a f i t e

a g a ch u h o

a g a ch u r i

a g a h e r a

a g a h i n d a

a g a h u m b a g i z a

a g a h u m b i

a g a k a t o

a g a k i z a

a g a m i zh e

a g a sh i ny a g u r o

a g a s u s u r u k o

a g a t e g a ny o

a g a t i m b a

a g a ts i k o

a g a ts i ts i n o
=======

The script will take this and convert the digraphs to IPA counterparts, leaving the other characters alone. See Kinyarwanda folder for examples of IPA chart files, originals, and IPA transcribed files.
