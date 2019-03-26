options(scipen = 4)

dat = read.csv("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/eaq_df.csv", header = TRUE)

dat$question = factor(dat$question,levels=unique(dat$question))
dat$rater = factor(dat$rater,levels=unique(dat$rater))
dat$likert.f = factor(dat$likert, ordered = TRUE,levels = c('1','2','3','4','5'))

library(likert)
#likert_data = data.frame()
#likert_data = 
#items=dat[,3, drop=FALSE]
#Result = likert(items)

#plot(Result,type='bar',col=myColor)+theme_minimal()+ggtitle()
hist(dat$likert)
ggplot(dat, aes(x=likert), bins=5) + geom_histogram()

str = "q8"

myColor = c('#c2185b',
            '#eb9366',
            '#fff3bc',
            '#97c694',
            '#009688')

ggplot(dat, aes(likert)) + geom_bar(fill=myColor)+theme_minimal()+ggtitle("Overall Attitudes...")
