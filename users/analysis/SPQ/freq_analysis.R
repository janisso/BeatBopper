rm(list=ls(all=TRUE)) 
.rs.restartR()
library(ggplot2)
library(likert)



#####FOR SYSTEM
dats = read.csv("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/SPQ/chisq_system.csv", header = TRUE)
dats$pref.f[dats$pref == 0] = 'Borch'
dats$pref.f[dats$pref == 1] = 'Each Beat'
dats$pref.f[dats$pref == 2] = 'Phase'
dats$pref.f[dats$pref == 3] = 'Not Sure'

#dats = dats[dats$question!='q6',]

dats$question = factor(dats$question,
                       levels=c('q1','q2','q3','q4','q5','q6'))
dats$excerpt = factor(dats$excerpt,
                       levels=c('0','1','2'))
dats$pref.f = factor(dats$pref.f,
                     levels=c('Each Beat','Borch','Phase','Not Sure'))

XT_pref_all = xtabs( ~ pref.f + question, data = dats)
XT_pref_00 = xtabs( ~ pref.f + question, data = dats[dats$excerpt==0,])
XT_pref_01 = xtabs( ~ pref.f + question, data = dats[dats$excerpt==1,])
XT_pref_02 = xtabs( ~ pref.f + question, data = dats[dats$excerpt==2,])
XT_pref_00
XT_pref_01
XT_pref_02
XT_pref_all

chisq.test(XT_pref_all)
chisq.test(XT_pref_01)
chisq.test(XT_pref_01)
chisq.test(XT_pref_all)

chi_sq = chisq.test(XT_pref_all)

contrib = 100*chi_sq$residuals^2/chi_sq$statistic
crit = 0.05
critAdj = crit/(nrow(XT_pref_all)*ncol(XT_pref_all))
pnorm(-abs(chi_sq$stdres))<=critAdj

bim = XT_pref_all
N = sum(XT_pref_all)
for (i in 1:ncol(XT_pref_all)){
  for (j in 1:nrow(XT_pref_all)){
    colsum = sum(XT_pref_all[i])
    rowsum = sum(XT_pref_all[j,])
    adj_res = (XT_pref_all[j,i]-chi_sq$expected[j,i])/sqrt(rowsum * colsum * (1/N) * (1-rowsum * (1/N)) * (1 - colsum*(1/N)))
    bim[j,i] = adj_res
    #print(themes[j,i]) 
  }
}
p_values = pchisq(chi_sq$stdres^2,df=1,  lower.tail = FALSE)
p_values <= critAdj
library(corrplot)
#corrplot(chisq.test(XT_pref_all)$residuals, method = "circle")

corrplot(chi_sq$stdres, is.cor = FALSE,
         #addCoef.col = "black", # Add coefficient of correlation,
         #method = "color",
         p.mat = p_values, sig.level = critAdj,
         pch.col = "white",
         tl.col="black")#,
#insig= "n")
theme_set(theme_bw())

#####BARPLOT FOR FREQS
system_var = c(rep('Borch',6),rep('Each Beat',6),rep('Phase',6),rep('Not Sure',6))
question_var = rep(c('q1','q2','q3','q4','q5','q6'),4)
freq_var = c(24,25,23,22,23,26,12,15,14,18,13,31,38,33,36,31,37,18,7,8,8,10,8,6)
#dadata = matrix(c(24,12,38,7,25,15,33,8,23,14,36,8,22,18,31,10,23,13,37,8,26,31,18,6),nrow=4)
dats_freq = data.frame(system_var,question_var,freq_var)
dats_freq$system_var = factor(dats_freq$system,
                              levels=c('Each Beat','Borch','Phase','Not Sure'))

myColor = c('#c2185b',
            '#eb9366',
            '#fff3bc',
            '#97c694',
            '#009688')


ggplot(data=dats_freq, aes(x=question_var, y=freq_var,fill=system_var)) +
  geom_bar(stat="identity", position=position_dodge())+
  scale_fill_manual(values=c("#003f5c", "#7a5195", "#ef5675",'#ffa600'))+
  theme_minimal()

table <- matrix(c(24,12,38,7,25,15,33,8,23,14,36,8,22,18,31,10,23,13,37,8,26,31,18,6),nrow=4)#matrix(c(1,21,34,35,26,17), nrow = 2, byrow = T)
dimnames(table) = list(System=c('Borch','Each Beat','Phase','Not Sure'), Variable=c('q1','q2','q3','q4','q5','q6'))
table; addmargins(table)
expect <- round(chisq.test(table)$expected)
addmargins(expect)
round(chisq.test(table)$residuals, 1)
library(vcd)
mosaic(table, shade=T, gp = shading_max)

########

fisher.test(data,workspace=1e+10)
chisq.test(data)

library(fifer)
chisq.post.hoc(data)
assocplot(XT_pref_all)

#barplot(XT_pref_all)



#plot(XT_pref_all,type='bar',col=myColor)+theme_minimal()+ggtitle(q)




#####FOR ORDER
dats = read.csv("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/SPQ/chisq_order.csv", header = TRUE)
dats$order.f[dats$order == 0] = 'First'
dats$order.f[dats$order == 1] = 'Second'
dats$order.f[dats$order == 2] = 'Third'
dats$order.f[dats$order == 3] = 'Not Sure'
dats$question = factor(dats$question,
                       levels=c('q1','q2','q3','q4','q5','q6'))
#dats$order = factor(dats$order,
#                    levels=c('0','1','2'))
dats$order.f = factor(dats$order.f,
                     levels=c('First','Second','Third','Not Sure'))
XT_order_all = xtabs( ~ order.f + question, data = dats)
XT_order_00 = xtabs( ~ order.f + question, data = dats[dats$excerpt==0,])
XT_order_01 = xtabs( ~ order.f + question, data = dats[dats$excerpt==1,])
XT_order_02 = xtabs( ~ order.f + question, data = dats[dats$excerpt==2,])
XT_order_00
XT_order_01
XT_order_02

chisq.test(XT_order_all)$residuals
chisq.test(XT_order_00)
chisq.test(XT_order_01)
chisq.test(XT_order_02)




