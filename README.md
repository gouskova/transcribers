# transcribers

Some utilities for converting orthography into IPA, for work with phonological computational models. 

The generic transcriber script is designed to work with relatively simple, good orthographies. If an orthography can be converted into IPA using a simple unordered lookup table (as in Quechua) or by applying ordering logic (as in Russian), the generic transcriber should get you most of the way towards a usable transcription. Many languages require additional processing to implement more complex phonological rules not reflected in the orthography.

To use the generic transcriber:

$ python3 generic_transcriber.py --help

This will print all the available options.

A simple use case:

$ python3 generic_transcriber.py --infile my_orthography.txt --outfile LearningData.txt --transkey transcription_key.txt

This will take any sequences in the first column of the transcription key file, and replace them with corresponding sequences from the second column of the transcription file, unordered.

An example of an IPA chart ("--transkey"):

#transcription_key.txt
jy	  ɟ
ny	  ɲ
ng	  ŋ
sy	  ç
ts	  ʦ
ch	  ʧ
sh	  ʃ
zh	  ʒ

Other options you can control include whether to insert spaces between characters, whether to transcribe only the first column of a file, and whether to save the original orthographic forms alongside the transcriptions in the output. You can also apply the transcriber to just one word, to test it. See help for details.
