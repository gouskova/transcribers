shonafull<-read.csv("~/git/phonotactics/test_runs/shona/user_input_files_full/LearningData.txt", header=F)

shonaverbs<-read.csv("~/git/phonotactics/test_runs/shona/user_input_files_verbs_extended_segs/LearningData.txt", header=F)

colnames(shonafull)=c("word")
colnames(shonaverbs)=c("word")

length(unique(shonafull$word))
length(unique(shonaverbs$word))
length(shonaverbs$word)

inboth = intersect(shonafull$word, shonaverbs$word)

shonaverbs$inbigdict = shonaverbs$word %in% inboth
summary(shonaverbs)

shonaverbs[shonaverbs$inbigdict==F,]$word

length(unique(shona$word))

shonaverbs[shonaverbs=='bh u r e k a',]$word
shonafull[shonafull=='bh u r e k a',]$word


write.table(sort(shona$word), "~/Desktop/LearningData.txt",  quote=F, row.names=F)