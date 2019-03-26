.rs.restartR()

library(ggplot2)
library(likert)
library(ggthemes)
library(psych)
library(reshape2)
library(lattice)
# library("viridisLite")
# rm(list = ls())
# 
# cols <- viridis(3)
# cols <- substr(cols, 0, 7)
# 
# #### ex 0 ####
# 
# library("magrittr")
# 
# hc <- highchart() %>%
#   hc_title(text = "Frequency of Likert Scales") %>% 
#   hc_subtitle(text = "Blah blah blah") %>% 
#   hc_chart(type = "column") %>% 
#   hc_xAxis(categories = c("Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree")) %>% 
#   hc_add_series(name = "Naive", data = c(6, 23, 37, 66, 38)) %>%
#   hc_add_series(name = "Compensation", data = c(17, 31, 36, 50, 36)) %>% 
#   hc_add_series(name = "Phase Estimaton", data = c(5, 27, 35, 27, 76)) 
#   #hc_add_theme(hc_theme_tufte2())%>%
#   #hc_colors(cols)
# 
# hc

######## PERFORMING A TEST FOR DIFFERENCES BETWEEN THE SYSTEMS

# library("psych")
# library("FSA")
# library("lattice")
# library("ggplot2")
# library("plyr")
# library("boot")
# library("rcompanion")



dat = read.csv("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/SUS/kruskal.csv", header = TRUE)
dat$system[dat$system == 0] = 'Naive'
dat$system[dat$system == 1] = 'Comp'
dat$system[dat$system == 2] = 'Phase'
dat$system = factor(dat$system,
                    levels=c('Naive','Comp','Phase'))
dat$question = factor(dat$question,levels=unique(dat$question))
dat$rater = factor(dat$rater,levels=unique(dat$rater))
dat$likert.f = factor(dat$likert, ordered = TRUE,levels = c('1','2','3','4','5'))

XT = xtabs(~ system + likert.f,data=dat)
# barplot(XT,
#         beside=TRUE,
#         legend=TRUE,
#         xaxt="n",
#         yaxt="n",
#         border=F,
#         width=c(.35),
#         #space=1.8,
#         xlab="Likert score",
#         ylab="Frequency",
#         family="serif")
# 
# axis(1, at=(c(1,2.5,4,5.5,7))-.3, col=c('#242ca2','#25a224','#252ca2','#25a224','#252ca2'), labels=c("Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"), tick=F, family="serif")
# #axis(1, at=(1:length(d))-.26, labels=c("Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"), tick=F, family="serif")
# axis(2, las=2, tick=F, family="serif")
# abline(col="white", lwd=3)
# abline(h=0, col="gray", lwd=2)
# #text(min(XT)/2, max(XT)/1.2, pos = 4, family="serif",
# #     "Average scores\non negative emotion traits\nfrom 3896 participants\n(Watson et al., 1988)")

# library(ggplot2)
# library(ggthemes)
# library(psych)
# library(reshape2)

# d <- melt(colMeans(msq[,c(2,7,34,36,42,43,46,55,68)],na.rm = T)*10)
# d$trait <- rownames(d)
# ggplot(XT, aes(x=c("Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"), y=value)) + theme_tufte(base_size=14, ticks=F) +
#   geom_bar(width=0.25, fill="gray", stat = "identity") +  theme(axis.title=element_blank()) +
#   scale_y_continuous(breaks=seq(1, 5, 1)) + 
#   geom_hline(yintercept=seq(1, 5, 1), col="white", lwd=1) +
#   annotate("text", x = 3.5, y = 5, adj=1,  family="serif",
#            label = c("Average scores\non negative emotion traits
#                      from 3896 participants\n(Watson et al., 1988)"))

# dats <- data.frame(system=c('Phase','Comp','Naive'),
#                    "Strongly Disagree"=c(6,17,5),
#                    "Disagree"=c(20,25,21),
#                    "Neutral"=c(3,10,7),
#                    "Agree"=c(3,10,7),
#                    "Strongly Agree"=c(15,10,9))
# dats.m <- melt(dats, id.vars='system')
# ggplot(dats.m, aes(variable, value)) + geom_bar(aes(fill = system), stat = "identity", position = "dodge") + theme_minimal()

# 
# histogram(~ likert.f | system,
#           data=dat,
#           layout=c(1,3)      #  columns and rows of individual plots
# )
# 
# histogram(~ likert.f | question,
#           data=dat,
#           layout=c(1,10)      #  columns and rows of individual plots
# )
# 
# 
# histogram(~ likert.f | system + question,
#           data=dat,
#           layout=c(3,10)      #  columns and rows of individual plots
# )
# 
# boxplot(likert ~ system + question,
#         data=dat,
#         #names=c("SB.Inf","P.Inf","SB.Pres", "P.Pres", "SB.Quest", "P.Quest"),
#         ylab="Value")
# 
# ### Produce interaction plot 
# 
# library(FSA)
# 
# Sum = Summarize(likert ~ system + question, 
#                 data=dat, 
#                 digits=3)
# library(ggplot2)
# 
# pd = position_dodge(.2)
# 
# ggplot(Sum, aes(x=system,
#                 y=median,
#                 color=question)) +
#   geom_errorbar(aes(ymin=Q1,
#                     ymax=Q3),
#                 width=.2, size=0.7, position=pd) +
#   geom_point(shape=15, size=4, position=pd) +
#   theme_bw() +
#   theme(axis.title = element_text(face = "bold")) +
#   
#   ylab("Median Likert score")
# 
Naive = dat$likert[dat$system=='Naive']
Comp = dat$likert[dat$system=='Comp']
Phase = dat$likert[dat$system=='Phase']
likert_data <- data.frame(Naive, Comp, Phase)

likert_data$Naive = factor(likert_data$Naive, levels = c('1','2','3','4','5'))
likert_data$Comp = factor(likert_data$Comp, levels = c('1','2','3','4','5'))
likert_data$Phase = factor(likert_data$Phase, levels = c('1','2','3','4','5'))

Result = likert(likert_data)

plot(Result,
     type="density",
     facet = TRUE, 
     bw = 0.5)

#p = ggplot(dat, aes(factor(system),likert))
#p + geom_violin(scale = "width") + geom_jitter(height = 0, width = 0.1)


summary(Result)
#myColor <- c("#242CA2","#B1CEE8","#E6E6E6","#ADEDCD","#25A224")
myColor <- c('#B22222', '#F08080', '#DCDCDC', '#6495ED','#00008B')

#both_likert_2 = likert(dat[, c(2,5), drop = FALSE], grouping = dat$question)

plot(Result,type='bar',col=myColor)+theme_minimal()+ggtitle()
# THE PIXEL RESOLUTION IS 696 x 272
# 




#                    "Strongly Disagree"=c(6,17,5),
#                    "Disagree"=c(20,25,21),
#                    "Neutral"=c(3,10,7),
#                    "Agree"=c(3,10,7),
#                    "Strongly Agree"=c(15,10,9))

# create a dataset
System = c(rep('Naive',5), rep('Comp',5), rep('Phase',5))
System = factor(System, levels = c('Naive','Comp','Phase'))

Scale = c(rep(c("Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"),3))
Scale = factor(Scale, levels = c("Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"))
Value = c()
for (i in c('Naive','Comp','Phase')){
  for (j in c(1,2,3,4,5)){
    Count = length(dat$question[dat$system==i & dat$likert.f==j])
    Value = c(Value,Count)
  }
}

Perc_Values = (Value/180)*100
data=data.frame(System,Scale,Perc_Values)

Colors = c(rep(myColor,3))

ggplot(data, aes(fill=System, x=Scale, y=Perc_Values)) + 
  geom_bar(position="dodge", stat="identity") + 
  theme_minimal() + 
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) + 
  scale_fill_manual(values=c('#DCDCDC','#B22222','#00008B')) +
  ggtitle('')
# THE PIXEL RESOLUTION IS 696 x 272

# for (q in c(1,2,3,4,5,6,7,8,9,10)){
#   q = 10
#   Naive = dat$likert[dat$question==q & dat$system=='Naive']
#   Comp = dat$likert[dat$question==q & dat$system=='Comp']
#   Phase = dat$likert[dat$question==q & dat$system=='Phase']
#   likert_data <- data.frame(Naive, Comp, Phase)
#   likert_data$Naive = factor(likert_data$Naive, levels = c('1','2','3','4','5'))
#   likert_data$Comp = factor(likert_data$Comp, levels = c('1','2','3','4','5'))
#   likert_data$Phase = factor(likert_data$Phase, levels = c('1','2','3','4','5'))
#   
#   Result = likert(likert_data)
#   
#   plot(Result,type='bar',col=myColor)+theme_minimal()+ggtitle(q)
# }

# plot(Result,
#      type="heat",
#      low.color = "white",
#      high.color = "green",
#      text.color = "black",
#      text.size = 4,
#      wrap = 50)
# 
# plot(Result,
#      type="density",
#      facet = TRUE,
#      bw = 0.5)
# 
# kruskal.test(likert.f~system,data=dat)
