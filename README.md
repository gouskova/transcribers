# transcribers
Some utilities for converting orthography into IPA or ASCII formats compatible with several phonological learner programs. 


##Russian
The Russian branch implements phonological rules such as voicing assimilation and vowel reduction in unstressed syllables, and can distinguish up to three degrees of stress marking. Also does UCLA Phonotactic Learner transcription and Minimal Generalization Learner transcription of Russian.

To do: make it work better with morpheme boundaries.

##Generic transcriber

Usage:

python3 generic_transcriber.py path_to_IPA_chart path_to_orig_file path_to_outfile

paths should be full. An example of an IPA chart:



jy     ɟ
ny     ɲ
ng     ŋ
sy     ç
ts     ʦ
ch     ʧ
sh     ʃ
zh     ʒ


An example of the original file to be converted to IPA:


a b a ny a r u k i k o
a b i r a
a g a ch u h o
a g a h u m b a g i z a
a g a k a t o
a g a m i zh e
a g a sh i ny a g u r o

The script will take this and convert the digraphs to IPA counterparts, leaving the other characters alone. See Kinyarwanda folder for examples.
