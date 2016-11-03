shona = read.csv("shona_verbs.txt", header=F)
colnames(shona)=c("word")

shona$Cvowel = gsub("[^aeiou] ", "C ", shona$word)
head(shona)


shona$vowels = gsub("[^ ]C", "C", shona$Cvowel)

shona$maxCVsep = ifelse(grepl("[aeiou] C C [aeiou]", shona$vowels), 2, 1)
shona$maxCVsep = ifelse(grepl("[aeiou] C C C [aeiou]", shona$vowels), 3, shona$maxCVsep)

length(shona[shona$maxCVsep==3,]$word)
length(shona[shona$maxCVsep==2,]$word)
length(shona[shona$maxCVsep==1,]$word)

prop.table(xtabs(~shona$maxCVsep))

shona[shona$maxCVsep==1 & grepl('u', shona$vowels) & grepl('i', shona$vowels),]$word
shona[shona$maxCVsep==3 & grepl('u', shona$vowels) & grepl('i', shona$vowels),]$word


shona$hiatus = grepl("[aeiou] [aeiou]", shona$vowels)

shona[shona$hiatus,]$word

summary(shona)

