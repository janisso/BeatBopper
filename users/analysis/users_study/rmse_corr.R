rm(list=ls(all=TRUE)) 
.rs.restartR()

library(ggplot2)
library(reshape2)


# R function
f = function(x, output) {
  # x is the row of type Character
  cat(which.min(x),which.max(x),"\n")
}


#####FOR SYSTEM
dats = read.csv("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/SPQ/chisq_system.csv", header = TRUE)
dats$pref.f[dats$pref == 0] = 'Naive'
dats$pref.f[dats$pref == 1] = 'Each Beat'
dats$pref.f[dats$pref == 2] = 'BB'
dats$pref.f[dats$pref == 3] = 'Not Sure'

#dats = dats[dats$question!='q6',]

dats$question = factor(dats$question,
                       levels=c('q1','q2','q3','q4','q5','q6'))
dats$excerpt = factor(dats$excerpt,
                      levels=c('0','1','2'))
dats$pref.f = factor(dats$pref.f,
                     levels=c('Naive','Each Beat','BB','Not Sure'))



u_pos = dats[dats$question=="q1",]
u_neg = dats[dats$question=="q6",]



######RMSE VALUES
datss = read.csv("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/SPQ/intention_rmse.csv", header = TRUE)

my_data <- melt(datss, id="id")

#rmse = c(dats$e3_n,dats$e3_c,dats$e3_p)
my_data$variable = rep(c(rep('Naive',27),rep('Each Beat',27),rep('BB',27)),3)
names(my_data)[2] <- "systems"
names(my_data)[3] <- "rmse"
#my_data = data.frame(rmse,systems)
my_data$systems = ordered(my_data$systems,
                          levels = c('Naive','Each Beat','BB'))


e1_rmse = data.frame(naive=datss$e1_n,each_beat=datss$e1_c,bb=datss$e1_p)
e1_obj_best = apply(e1_rmse, 1, FUN=which.min)-1
e1_obj_wors = apply(e1_rmse, 1, FUN=which.max)-1

e2_rmse = data.frame(naive=datss$e2_n,each_beat=datss$e2_c,bb=datss$e2_p)
e2_obj_best = apply(e2_rmse, 1, FUN=which.min)-1
e2_obj_wors = apply(e2_rmse, 1, FUN=which.max)-1

e3_rmse = data.frame(naive=datss$e3_n,each_beat=datss$e3_c,bb=datss$e3_p)
e3_obj_best = apply(e3_rmse, 1, FUN=which.min)-1
e3_obj_wors = apply(e3_rmse, 1, FUN=which.max)-1
#obj = apply(e1_rmse,1,f)


ting = data.frame(id=u_pos$rater,
                  e = u_pos$excerpt,
                  obj_best=c(e1_obj_best,e2_obj_best,e3_obj_best),
                  sub_best=u_pos$pref,
                  obj_wors=c(e1_obj_wors,e2_obj_wors,e3_obj_wors),
                  sub_wors=u_neg$pref)

###CONFUSION MATRIX
library(caret)
numLlvs <- 3
ting[ting$sub_best==3,]$sub_best=NA
ting[ting$sub_wors==3,]$sub_wors=NA
pos = confusionMatrix(factor(ting$sub_best),factor(ting$obj_best)) 
neg = confusionMatrix(factor(ting$sub_wors),factor(ting$obj_wors)) 
library(xtable)
xtable(t(pos$byClass))
xtable(t(neg$byClass))
