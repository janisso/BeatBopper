rm(list=ls(all=TRUE)) 
.rs.restartR()

options(scipen = 4)

######SUS
get_sus <- function(sus) {
  x = vector(mode="numeric", length=27)
  for (user in 1:27){
    user_score = sus[sus$rater==user,]$likert
    sus_score = sum(user_score-1)*2.5
    x[user] = sus_score
  }
  return(x)
}


dats = read.csv("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/SUS/kruskal.csv", header = TRUE)
dats$system[dats$system == 0] = 'Borch'
dats$system[dats$system == 1] = 'Each Beat'
dats$system[dats$system == 2] = 'Phase'
#dat$system = as.factor(dat$system)
dats$system = factor(dats$system,
                     levels=c('Each Beat','Borch','Phase'))
dats$question = factor(dats$question,levels=unique(dats$question))
dats$rater = factor(dats$rater,levels=unique(dats$rater))

rater = c(seq(1, 27))
each_beat = get_sus(dats[dats$system=='Each Beat',])
borch = get_sus(dats[dats$system=='Borch',])
phase = get_sus(dats[dats$system=='Phase',])
sus_scores = data.frame(rater,each_beat,borch,phase)

rater = rep(rater,3)
system = c(rep('Each Beat',27),rep('Borch',27),rep('Phase',27))
score = c(each_beat,borch,phase)
sus_df = data.frame(rater,system,score)
sus_df$system <- ordered(sus_df$system,
                         levels=c('Each Beat','Borch','Phase'))

sus_scores$years[is.na(sus_scores$years)] <- 0

library(dplyr)

#ANOVA
group_by(sus_df, system) %>%
  summarise(
    count = n(),
    mean = mean(score, na.rm = TRUE),
    sd = sd(score, na.rm = TRUE)
  )

# Change box plot line colors by groups
p<-ggplot(sus_df, aes(x=system, y=score, color=system)) +
  geom_boxplot()+
  labs(title="System Usability Scale Comparison", x="System", y = "SUS Score")+
  theme_classic()+
  theme(legend.position = "none")+
  scale_colour_manual(values= c("#003f5c", "#7a5195", "#ef5675"))
p


#CHECK ANOVA ASSUMPTIONS

# 1. Homogeneity of variances
plot(res.aov, 1)
library(car)
leveneTest(score ~ system, data = sus_df)

# 2. Normality
plot(res.aov, 2)
# Extract the residuals
aov_residuals <- residuals(object = res.aov )
# Run Shapiro-Wilk test
shapiro.test(x = aov_residuals )

sus_df$system.n = as.numeric(sus_df$system)
sus_df$system.n = factor(sus_df$system.n,
                         labels = c('Each Beat','Borch','Phase'))

mdl = lm(formula=score ~ system.n, data = sus_df)
summary(mdl)

#ONE WAY ANOVA

anova(mdl)
9506/(9506+32956)

confint(mdl)
rSquared(mdl)


res.aov <- aov(score ~ system, data = sus_df)
summary(res.aov)

#library(foreign)
#write.foreign(sus_df, "/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/SUS/sus_anova/sus_anova.csv", "/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/SUS/sus_anova/sus_anova.sps",   package="SPSS")
#library(ez)
#ezANOVA(sus_df,
#        dv = score,
#        wid = system,
#        within = .(1))

tapply(sus_df$score, as.numeric(sus_df$system), mean, na.rm=T) 

fm1 = aov(score ~ system, data = sus_df)
xtable(fm1)
# 
lm(score ~ system, data = sus_df)



#####BARPLOT FOR FREQS
system_var = c(rep('Each Beat',10),rep('Borch',10),rep('Phase',10))
question_var = rep(c('q1','q2','q3','q4','q5','q6','q7','q8','q9','q10'),3)
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

library(ggplot2)
ggplot(data=dats_freq, aes(x=question_var, y=freq_var,fill=system_var)) +
  geom_bar(stat="identity", position=position_dodge())+
  scale_fill_manual(values=c("#003f5c", "#7a5195", "#ef5675",'#ffa600'))+
  theme_minimal()

# ggplot(sus_scores) + 
#   geom_point(aes(x=years, y=each_beat),shape=15,color="#003f5c") +
#   geom_point(aes(x=years, y=borch),shape=6,color="#7a5195")+
#   geom_point(aes(x=years, y=phase),shape=16,color="#ef5675")+
#   labs(title = "SUS Score\n", x = "Experience (years)", y = "SUS Score", color = "Legend Title\n")+
#   theme_minimal()
  
df = read.csv("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/P_INFO/p_info.csv", header = TRUE)
colnames(df) = c('ts','id','age','sex','hearing','instr','names','years','num_instr','practice','conductor','cond_exp','music','music_styles','classical','enjoy','comment')
drops = c('ts','hearing','names','cond_exp','music','music_styles','classical','enjoy','comment')
keeps = df[ , !(names(df) %in% drops)]

summary(keeps)
keeps[keeps$instr=='No',]$practice=NA
keeps$num_instr

sus_scores$years = keeps$years
sus_scores$years[is.na(sus_scores$years)] = 0


names(arbuthnot) <- c("years", "Men", "Women")

arbuthnot.melt <- melt(arbuthnot, id.vars = 'Year', variable.name = 'Sex', 
                       value.name = 'Rate')

ggplot(arbuthnot.melt, aes(x = Year, y = Rate, shape = Sex, color = Sex))+
  geom_point() + scale_color_manual(values = c("Women" = '#ff00ff','Men' = '#3399ff')) + 
  scale_shape_manual(values = c('Women' = 17, 'Men' = 16))

