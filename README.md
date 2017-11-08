# transcribers
Some utilities for converting orthography into IPA or ASCII formats compatible with several phonological learner programs. 


##Russian
The Russian branch implements phonological rules such as voicing assimilation and vowel reduction in unstressed syllables, and can distinguish up to three degrees of stress marking. Also does UCLA Phonotactic Learner transcription and Minimal Generalization Learner transcription of Russian.

To do: make it work better with morpheme boundaries.

##Generic transcriber

Usage:

python3 generic_transcriber.py path_to_IPA_chart path_to_orig_file path_to_IPA_outfile

paths should be full. 

The script will take this and convert the digraphs to IPA counterparts, leaving the other characters alone. See Kinyarwanda folder for examples of IPA chart files, originals, and IPA transcribed files.
