This subdirectory contains an old digitized dictionary by Creissels, which was available for download on the CBOLD project:

https://web.archive.org/web/20080229220938/http://www.cbold.ddl.ish-lyon.cnrs.fr/ 

I used the version of the dictionary from the following repo:

https://github.com/tebello-thejane/creis/

There are three versions of the data:

tswana-french-dictionary.txt	
	attempts to preserve as much of the information from the original Creissels dictionary, only updating the IPA transcriptions to Unicode.

LearningData_tones.txt is the tokenized version with a three-way tone distinction on all sonorants that can bear tone, in IPA.

LearningData_notones.txt is the same with tones removed.

If you want to see how these were generated, tswana_transcriber.py has more details. To re-generate the files, you can run the script as follows:

this will re-create the tab-separated French dictionary:

$ python3 tswana_transcriber.py writefrench

and this will write the learning data, and starter Features.txt files that save each segment to its own line. No actual features in these.

$ python3 tswana_transcriber.py writeld

Questions, corrections--let me know. 

-- Maria
