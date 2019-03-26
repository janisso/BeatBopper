rm(list=ls(all=TRUE)) 
.rs.restartR()

dats = read.csv("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/SPQ/intention_rmse.csv", header = TRUE)

excerpt = c(rep('e1',81),rep('e2',81),rep('e3',81))
rmse = c(dats$e1_n,dats$e1_c,dats$e1_p,dats$e2_n,dats$e2_c,dats$e2_p,dats$e3_n,dats$e3_c,dats$e3_p)
systems = c(c(rep('Borch',27),rep('Each Beat',27),rep('Phase',27)),c(rep('Borch',27),rep('Each Beat',27),rep('Phase',27)),c(rep('Borch',27),rep('Each Beat',27),rep('Phase',27)))
my_data = data.frame(excerpt,rmse,systems)
my_data$systems = ordered(my_data$systems,
                          levels = c('Each Beat','Borch','Phase'))

# Box plots
# ++++++++++++++++++++
# Plot weight by group and color by group
# library("ggpubr")
# ggboxplot(my_data, x = "systems", y = "rmse", 
#           color = "systems", palette = c("#00AFBB", "#E7B800", "#FC4E07"),
#           order = c("Naive", "Comp", "Phase"),
#           ylab = "Rmse", xlab = "Treatment")

myColor = c('#c2185b',
            '#eb9366',
            '#fff3bc')
library(ggplot2)
# Change  automatically color by groups
bp <- ggplot(my_data, aes(x=systems, y=rmse, fill=systems)) + 
  geom_boxplot() +
  labs(title="RMSE for for all 3 Excerpts",x="System", y = "RMSE")
bp + scale_fill_manual(values=c("#003f5c", "#7a5195", "#ef5675")) + theme_minimal()
res.aov <- aov(rmse ~ systems, data = my_data)
summary(res.aov)
TukeyHSD(res.aov)

library(multcomp)
summary(glht(res.aov, linfct = mcp(systems = "Tukey")))

# 1. Homogeneity of variances
plot(res.aov, 2)

leveneTest(rmse ~ systems, data = my_data)

# Extract the residuals
aov_residuals <- residuals(object = res.aov )
# Run Shapiro-Wilk test
shapiro.test(x = aov_residuals )

library(foreign)
write.csv(my_data, file = "data_for_spss.csv")
write.foreign(my_data, "data_for_spss.csv", "data_for_spss.sps",   package="SPSS")


#########TWO WAY ANOVA PLOT
my_data$se <- with(my_data , aggregate(rmse, list(systems=systems, excerpt=excerpt), 
                                      function(x) sd(x)/sqrt(10)))[,3]

mean(my_data[my_data$excerpt=='e1',]$rmse)

mean_data



#########TWO WAY ANOVA
interaction.plot(x.factor = my_data$excerpt,
                 trace.factor = my_data$systems,
                 response = my_data$rmse,
                 fun = mean,
                 type = "b",
                 col=c("black","red","green"),  ### Colors for levels of trace var.
                 pch=c(19, 17, 15),             ### Symbols for levels of trace var.
                 fixed=TRUE,                    ### Order by factor order in data
                 leg.bty = "o")

library(FSA)
Sum = Summarize(rmse ~ excerpt + systems, 
                data=my_data, 
                digits=3)
Sum$se = Sum$sd / sqrt(Sum$n)
Sum$se = signif(Sum$se, digits=3)
Sum$excerpt = factor(Sum$excerpt,
                     levels=unique(Sum$excerpt))
Sum$systems = factor(Sum$systems,
                     levels=unique(Sum$systems))


### Produce interaction plot 

pd = position_dodge(.3)

ggplot(Sum, aes(x = excerpt,
                y = mean,
                color = systems)) +
  geom_errorbar(aes(ymin = mean - se,
                    ymax = mean + se),
                width=.2, size=0.7, position=pd) +
  geom_point(shape=15, size=4, position=pd) +
  scale_colour_manual(values= c("#003f5c", "#7a5195", "#ef5675"))+ 
  ylab("RMSE") + xlab("excerpt")+
  theme_minimal()
#          scale_colour_manual(values= c("#003f5c", "#7a5195", "#ef5675")) +


ggplot(Sum, aes(x = excerpt,
                y = mean,
                color = systems)) +
  geom_errorbar(aes(ymin = mean - se,
                    ymax = mean + se),
                width=.2, size=0.7, position=pd) +
  geom_line(aes(geom='systems')) +
  geom_point(shape=15, size=4, position=pd) +
  scale_colour_manual(values= c("#003f5c", "#7a5195", "#ef5675"))+ 
  ylab("RMSE") + xlab("excerpt")+
  theme_minimal()

df = data.frame(
  excerpt = factor(c(1,2,3,1,2,3,1,2,3)),
  mean = c(0.411, 0.241, 0.484, 0.370, 0.164, 0.430, 0.314, 0.179, 0.344),
  system = c(rep('Each Beat',3),rep('Borch',3),rep('Phase',3)),
  upper = c(0.44200, 0.26520, 0.54420, 0.38670, 0.18190, 0.43674, 0.33230, 0.19500, 0.37080),
  lower = c(0.38000, 0.21680, 0.42380, 0.35330, 0.14610, 0.42326, 0.29570, 0.16300, 0.31720)
)

df$system = ordered(df$system,
        levels = c('Each Beat','Borch','Phase'))

p <- ggplot(df, aes(x=excerpt,
                    y=mean,
                    color = system))

p + geom_line(aes(group = system),position=pd) +
  geom_errorbar(aes(ymin = lower, ymax = upper), width = 0.2, position=pd)+
                  #geom_line(position=pd) +
                  geom_point(position=pd)+
  labs(title="Estimated Marginal Means of RMSE",x="Excerpt", y = "Estimated Marginal Means")+
  scale_colour_manual(values= c("#003f5c", "#7a5195", "#ef5675"))+ 
  theme_minimal()

#bc5090
  

# df <- data.frame(
#   trt = factor(c(1, 1, 2, 2)),
#   resp = c(1, 5, 3, 4),
#   group = factor(c(1, 2, 1, 2)),
#   upper = c(1.1, 5.3, 3.3, 4.2),
#   lower = c(0.8, 4.6, 2.4, 3.6)
# )
# 
# p <- ggplot(df, aes(trt, resp, colour = group))
# p + geom_linerange(aes(ymin = lower, ymax = upper),position=pd)
