#this takes as input the Latin dictionary file downloaded from Ralf's dictionary collection. it needs a bit of cleaning, and it provides no morphological segmentation so it really only represents orthographic words found in latin texts. not sure exactly what era is represented, but i am assuming classical latin pronuncations for "v", "c", and so on. The rest should be self-explanatory as long as you understand basic regex operations in R.

latin_dict<-read.csv("latin-dictionary.txt", sep="\t")
head(latin_dict)

colnames(latin_dict)=c("grapheme")

latin_dict$grapheme=tolower(latin_dict$grapheme)
latin_dict$grapheme<-gsub("c", "k", latin_dict$grapheme)
latin_dict$grapheme<-gsub("qu", "kw", latin_dict$grapheme)


latin_dict=unique(latin_dict)
latin_dict=subset(latin_dict, grepl('z', latin_dict$grapheme)==F) #there should not be zs in latin words. those are either greek or who knows what
latin_dict=subset(latin_dict, grepl('XX', latin_dict$grapheme)==F) #these are all numbers

length(latin_dict$grapheme)

geminates=c('v', "ll", "tt", "dd", "rr", "nn", "pp", "bb", "ff", "mm", "vv", "gg", "kk", "ph", "jj", "ss", 'x','y')
singletons=c('w', "L", "T", "D", "R", "N", "P", "B", "F", "M", "V", "G", "K", "f", "J", "S", 'ks', 'i')

latin_dict$transcr=latin_dict$grapheme
for (i in 1:length(geminates)){
	gem = as.character(geminates[i])
	j = as.character(singletons[i])
	latin_dict$transcr=gsub(gem, j, latin_dict$transcr)
}

#add spaces between sounds
latin_dict$transcr=gsub("(.)", "\\1 ", latin_dict$transcr)
latin_dict$transcr=gsub(" $", "", latin_dict$transcr)

latin_dict$alis=grepl("a l i s$", latin_dict$transcr)
latin_dict$aris=grepl("a r i s$", latin_dict$transcr)

latin_dict$transcr=gsub("([aeiou]) (i) ([aeiou])", "\\1 j \\2", latin_dict$transcr)
latin_dict$transcr=gsub("^(i) (aeiou)", "j \\2", latin_dict$transcr )

length(latin_dict$transcr)

latin_aris<-subset(latin_dict, aris==T)
latin_alis<-subset(latin_dict, alis==T)
latin_arlis<-rbind(latin_aris, latin_alis)

length(latin_aris$transcr)
length(latin_alis$transcr)

latin_alis1<-latin_alis
latin_aris1<-latin_aris

while(length(latin_alis$transcr)<3000){
	latin_alis=rbind(latin_alis, latin_alis1)
}

while(length(latin_aris$transcr)<3000){
	latin_aris=rbind(latin_aris, latin_aris1)
}


write.table(latin_arlis$transcr, file='latin_arlis.txt', row.names=F, quote=F, col.names=F)
write.table(latin_aris$transcr, file='latin_aris.txt', row.names=F, quote=F, col.names=F)
write.table(latin_alis$transcr, file='latin_alis.txt', row.names=F, quote=F, col.names=F)
write.table(latin_dict$transcr, file='latin_all_2.txt', row.names=F, quote=F, col.names=F)
