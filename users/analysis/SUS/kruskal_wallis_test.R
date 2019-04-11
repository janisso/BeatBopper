rm(list=ls(all=TRUE)) 
.rs.restartR()

get_stats <- function(dat,title) {

  #yo = xtabs( ~ system + likert.f,
  #              data = dat)
  #print(yo)
  XT = xtabs( ~ system + likert.f,
              data = dat)
  
  yo = chisq.test(XT)
  print(yo)
  
  PP = prop.table(XT,
                  margin = 1) * 100
  print(round(PP))
  
  print(kruskal.test(likert ~ system, data = dat))
  Hadj = unname(kruskal.test(likert ~ system, data = dat)$statistic)
  print(paste0("Statistic ", Hadj))
  
  n = sum(table(dat$likert,dat$system))
  print(paste0("N ",n))
  e2 = Hadj*(n+1)/(n^2-1)
  print(paste0("Epsilon^2 ",e2))
  
  # epsilonSquared(x = dat$likert, 
  #                g = dat$system)
  
  DT = dunnTest(dat$likert,dat$system,method="bonferroni")
  DT
  PT = DT$res
  print(PT)
  
  # print(cldList(P.adj ~ Comparison,
  #         data = PT,
  #         threshold = 0.05))
  
  Naive = dat$likert[dats$system=='Naive']
  EachBeat = dat$likert[dat$system=='Each Beat']
  BeatBopper = dat$likert[dat$system=='Beat Bopper']
  likert_data <- data.frame(Naive, EachBeat, BeatBopper)
  
  likert_data$Naive = factor(likert_data$Naive, levels = c('1','2','3','4','5'))
  likert_data$EachBeat = factor(likert_data$EachBeat, levels = c('1','2','3','4','5'))
  likert_data$BeatBopper = factor(likert_data$BeatBopper, levels = c('1','2','3','4','5'))
  
  Result = likert(likert_data)
  
  # plot(Result,
  #      type="density",
  #      facet = TRUE, 
  #      bw = 0.5)
  
  #p = ggplot(dat, aes(factor(system),likert))
  #p + geom_violin(scale = "width") + geom_jitter(height = 0, width = 0.1)
  
  # summary(Result)
  #myColor <- c("#242CA2","#B1CEE8","#E6E6E6","#ADEDCD","#25A224")
  #myColor <- c('#B22222', '#F08080', '#DCDCDC', '#6495ED','#00008B')

  Sum = groupwiseMedian(likert ~ system,
                        data       = dat,
                        conf       = 0.95,
                        R          = 5000,
                        percentile = TRUE,
                        bca        = FALSE,
                        digits     = 3)
  print(Sum)
  X     = 1:3
  Y     = Sum$Percentile.upper + 0.2
  Label = c("ab", "a", "b")
  # 
  # 
  return(list('res'= Result, 'sum'=Sum, 'dun'=DT))
}

# library(psych)
# library(effsize)
# library(coin)
# library(dplyr)
# library(BSDA)
# library(ggplot2)
# library(likert)
# library(ggthemes)
# library(rcompanion)
# library(dunn.test)
# library(FSA)
# library(xtable)

options(scipen = 4)

dats = read.csv("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/SUS/kruskal.csv", header = TRUE)
dats$system[dats$system == 0] = 'Naive'
dats$system[dats$system == 1] = 'Each Beat'
dats$system[dats$system == 2] = 'Beat Bopper'
#dat$system = as.factor(dat$system)
dats$system = factor(dats$system,
                      levels=c('Naive','Each Beat','Beat Bopper'))
dats$question = factor(dats$question,levels=unique(dats$question))
dats$rater = factor(dats$rater,levels=unique(dats$rater))
dats$likert.f = factor(dats$likert, ordered = TRUE,levels = c('1','2','3','4','5'))
library(likert)
library(FSA)
library(multcompView)
library(ggplot2)
library("descr")
library('rcompanion')

########## KRUSKAL WALLIS TEST
###       OVERALL

quest=c("1. I found the system to be intuitive",
        "2. The system was easy to use",
        "3. How much did the used system reflect your desired tempo?",
        "4. It took me a long time to understand how the system works",
        "5. I was able to express my desired intentions",
        "6. I felt music was synchronised with my hand movements"	,
        "7. I found the system to be versatile",
        "8. I was satisfied with the overall sound output of the system",
        "9. I would use this system in a performance",
        "10. I would use this system to explore expressivity")

myColor = c('#ef5675',
            '#f7a8b1',
            '#f1f1f1',
            '#8093a3',
            '#003f5c')
#myColor <- c('#FF5352', '#E8A8D9', '#C5CAE9', '#BBA9E8','#303F9F')

Res = get_stats(dats,'Overall') #OVERALL
plot(Res$res,type='bar',col=myColor)+theme_classic()#+ggtitle('Overal Likert plot for SUS')

PT = Res$dun$res
cldList(P.adj ~ Comparison,
        data = PT,
        threshold = 0.05)

X = 1:3
Y = Res$sum$Percentile.upper + 0.4
Label = c("a","a","b")

#MEDIAN PLOTS
p <- ggplot(Res$sum,
            aes(x=system,
                y=Median,
                color = system))

p + geom_errorbar(aes(ymin = Percentile.lower, ymax = Percentile.upper), width = 0.2) +
  geom_point(shape = c(15,17,16),
             size  = 4)+
  labs(x="System", y = "Median Likert Scores")+
  theme_classic()+
  theme(legend.position = "none")+
  scale_colour_manual(values= c("#003f5c", "#7a5195", "#ef5675"))+
  ylim(1,5.5)+
  annotate("text", 
           x = X, 
           y = Y, 
           label = Label)
  #ylab("Median Likert score")+

# Res = get_stats(dats[dats$question==1,],quest[1])
# plot(Res,type='bar',col=myColor)+theme_minimal()+ggtitle(quest[1])
# 
# Res = get_stats(dats[dats$question==2,],quest[2])
# plot(Res,type='bar',col=myColor)+theme_minimal()+ggtitle(quest[2])
# 
# Res = get_stats(dats[dats$question==3,],quest[3])
# plot(Res,type='bar',col=myColor)+theme_minimal()+ggtitle(quest[3])
# 
# Res = get_stats(dats[dats$question==4,],quest[4])
# plot(Res,type='bar',col=myColor)+theme_minimal()+ggtitle(quest[4])
# 
# Res = get_stats(dats[dats$question==5,],quest[5])
# plot(Res,type='bar',col=myColor)+theme_minimal()+ggtitle(quest[5])
# 
# Res = get_stats(dats[dats$question==6,],quest[6])
# plot(Res,type='bar',col=myColor)+theme_minimal()+ggtitle(quest[6])
# 
# Res = get_stats(dats[dats$question==7,],quest[7])
# plot(Res,type='bar',col=myColor)+theme_minimal()+ggtitle(quest[7])
# 
# Res = get_stats(dats[dats$question==8,],quest[8])
# plot(Res,type='bar',col=myColor)+theme_minimal()+ggtitle(quest[8])
# 
# Res = get_stats(dats[dats$question==9,],quest[9])
# plot(Res,type='bar',col=myColor)+theme_minimal()+ggtitle(quest[9])
# 
# Res = get_stats(dats[dats$question==10,],quest[10])
# plot(Res,type='bar',col=myColor)+theme_minimal()+ggtitle(quest[10])
# 
# source("http://pcwww.liv.ac.uk/~william/R/crosstab.r")
# 
# crosstab(dats, row.vars = "Age", col.vars = "Sex", type = "f")
# yo = crosstab(dats, row.vars = c("question","system"), col.vars = "likert", type = "r")
# write.csv(yo$table, "crosstab.csv")
# xtabs( ~ system + likert.f,
#        data = dat)
# 
# XT = xtabs( ~ system + likert.f,
#             data = dat)
# 
# PP = prop.table(XT,
#                 margin = 1) * 100
# 
# kruskal.test(likert ~ system, data = dat)
# Hadj = unname(kruskal.test(likert ~ system, data = dat)$statistic)
# Hadj
# 
# n = sum(table(dat$likert,dat$system))
# n
# e2 = Hadj*(n+1)/(n^2-1)
# e2
# 
# # epsilonSquared(x = dat$likert, 
# #                g = dat$system)
# 
# DT = dunnTest(dat$likert,dat$system,method="bonferroni")
# DT
# PT = DT$res
# PT
# 
# cldList(P.adj ~ Comparison,
#         data = PT,
#         threshold = 0.05)

# multcompLetters(PT,
#                 compare="<",
#                 threshold=0.05,  # p-value to use as significance threshold
#                 Letters=letters,
#                 reversed = FALSE)

#library(rcompanion)

# ######MOOD MEDIAN TEST
# library(RVAideMemoire)
# mood.medtest(likert ~ system,
#              data  = dat,
#              exact = FALSE)
# 
# dat$likert.inv = 6 - dat$likert
# 
# mood.medtest(likert.inv ~ system,
#              data = dat,
#              exact = FALSE)
# 
# 
# median_test(likert ~ system,
#             data = dat,
#             distribution = approximate(B = 10000))
# 
# 
# PT = pairwiseMedianTest(likert ~ system,
#                         data   = dat,
#                         exact  = NULL,
#                         method = "fdr")
# 
# cldList(p.adjust ~ Comparison,
#         data = PT,
#         threshold = 0.05)
# 
# PT = pairwiseMedianMatrix(likert ~ system,
#                           data   = dat,
#                           exact  = NULL,
#                           method = "fdr") 
# 
# multcompLetters(PT$Adjusted,
#                 compare="<",
#                 threshold=0.05,
#                 Letters=letters)