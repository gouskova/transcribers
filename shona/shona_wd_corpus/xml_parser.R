
library(XML)

setwd('/home/maria/git/transcribers/shona/shona_wikipedia_corpus')

shona<-xmlParse('snwiki-20170301-pages-articles-multistream.xml')

mode(xmlChildren(shona))
length(xmlChildren(shona))

#shonadic<-xmlToDataFrame(getNodeSet(shona, "//text"))

head(shona) 
colnames(shona)


write.table(german, 'german-dictionary.txt', quote=F, row.names=F, sep="\t") #quotes otherwise are inserted around each word. row.names removes numbers at the beginning of each line. the "sep" argument specifies whether to put a tab (chosen), comma, or space (default) between columns

#if everything worked, there should now be a new file in the same directory as the original xml file.


#this whole procedure can be automated: 

files=list.files(workdir)

for (file in files){
	path=paste(workdir, file, sep="/")
	print(path)
	x=xmlToDataFrame(path)
	filename=gsub('xml', 'txt', basename(path))
	write.table(x, filename, quote=F, row.names=F, sep="\t")
	}
