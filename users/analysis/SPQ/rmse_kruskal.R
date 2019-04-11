rm(list=ls(all=TRUE))
.rs.restartR()

library(ggplot2)

#LOAD DATA
dats = read.csv("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/SPQ/intention_rmse.csv", header = TRUE)
excerpt = c(rep('e1',81),rep('e2',81),rep('e3',81))
rmse = c(dats$e1_n,dats$e1_c,dats$e1_p,dats$e2_n,dats$e2_c,dats$e2_p,dats$e3_n,dats$e3_c,dats$e3_p)
systems = c(c(rep('Naive',27),rep('Each Beat',27),rep('Beat Bopper',27)),c(rep('Naive',27),rep('Each Beat',27),rep('Beat Bopper',27)),c(rep('Naive',27),rep('Each Beat',27),rep('Beat Bopper',27)))
my_data = data.frame(excerpt,rmse,systems)
my_data$systems = ordered(my_data$systems,
                          levels = c('Naive','Each Beat','Beat Bopper'))


#PLOT DATA
myColor = c('#c2185b',
            '#eb9366',
            '#fff3bc')
library(ggplot2)
#my_data$t = dat_r - min(dat_r)
# Change  automatically color by groups
bp <- ggplot(my_data, aes(x=systems, y=rmse, fill=systems)) + 
  geom_boxplot(fill='#FFFFFF',color=c("#003f5c", "#7a5195", "#ef5675")) +
  labs(x="System", y = "Normalised RMSE")
bp  +   theme_classic()+
  theme(legend.position = "none")

#PLOT INTERACTION GAPHS
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

df = data.frame(
  excerpt = factor(c(1,2,3,1,2,3,1,2,3)),
  mean = Sum$mean,
  system = c(rep('Naive',3),rep('Each Beat',3),rep('Beat Bopper',3)),
  upper = Sum$max,
  lower = Sum$min
)

df$system = ordered(df$system,
                    levels = c('Naive','Each Beat','Beat Bopper'))

ggplot(df, aes(x=excerpt, y=mean,group = system))+
  geom_line(aes(linetype = system,color=system)) +
  scale_linetype_manual(values=c("dashed", "dotted","twodash"))+
  geom_point(data=df, mapping=aes(x=excerpt,y=mean,color=system),
             shape = c(15,15,15,17,17,17,16,16,16),
             size  = 4)+
  labs(x="Excerpt", y = "Estimated Marginal RMSE Means",fill='')+
  scale_colour_manual(values= c("#003f5c", "#7a5195", "#ef5675"))+
  theme_classic()

###T TEST on excerpts
rmse_e1 = c(dats$e1_n,dats$e1_c,dats$e1_p)
rmse_e2 = c(dats$e2_n,dats$e2_c,dats$e2_p)
rmse_e3 = c(dats$e3_n,dats$e3_c,dats$e3_p)
t.test(rmse_e1,rmse_e2)
t.test(rmse_e1,rmse_e3)
t.test(rmse_e2,rmse_e3)

#ANOVA TESTING FOR NORMALITY
res.aov <- aov(rmse ~ systems, data = my_data)
summary(res.aov)
TukeyHSD(res.aov)

library(multcomp)
summary(glht(res.aov, linfct = mcp(systems = "Tukey")))

# 1. Homogeneity of variances
plot(res.aov, 1)
plot(res.aov, 2)

library(car)
leveneTest(rmse ~ systems, data = my_data)

# Extract the residuals
aov_residuals <- residuals(object = res.aov )
# Run Shapiro-Wilk test
shapiro.test(x = aov_residuals )

###KRUSKAL WALLIST TEST for e1
e1 = my_data[my_data$excerpt=='e1',]
e1$systems = ordered(e1$systems,
                    levels = c('Naive','Each Beat','Beat Bopper'))

bp <- ggplot(e1, aes(x=systems, y=rmse, fill=systems)) + 
  geom_boxplot(fill='#FFFFFF',color=c("#003f5c", "#7a5195", "#ef5675")) +
  labs(x="System", y = "RMSE")

bp  +   theme_classic()+
  theme(legend.position = "none")

kruskal.test(rmse ~ systems, data = e1)
pairwise.wilcox.test(e1$rmse, e1$systems,
                     p.adjust.method = "BH")


dat_e1 = data.frame(dens = c(dats$e1_n,dats$e1_c,dats$e1_p),
                    lines = rep(c('Naive','Each Beat','Beat Bopper'),each=27))
dat_e1$lines = ordered(dat_e1$lines,
                       levels = c('Naive','Each Beat','Beat Bopper'))
p1 = ggplot(dat_e1,aes(x=dens, color=lines))+
  geom_density(alpha=0.2)+
  scale_color_manual(values=c("#003f5c", "#7a5195", "#ef5675")) +
  scale_fill_manual(values=c("#999999", "#E69F00", "#56B4E9"))+
  labs(x='E1 RMSE',y='Density')+
  theme_classic()

###plotting residuals
e1.ols = lm(rmse~systems, data=e1)
e1$resi = e1.ols$residual
ggplot(data = e1, aes(y = resi, x = systems)) + geom_point(col = 'blue') + geom_abline(slope = 0)
var.func <- lm(resi^2 ~ systems, data = e1)
summary(var.func)
qchisq(.95, df = 1)

###KRUSKAL WALLIST TEST for e2
e2 = my_data[my_data$excerpt=='e2',]
e2$systems = ordered(e2$systems,
                     levels = c('Naive','Each Beat','Beat Bopper'))

bp <- ggplot(e2, aes(x=systems, y=rmse, fill=systems)) + 
  geom_boxplot(fill='#FFFFFF',color=c("#003f5c", "#7a5195", "#ef5675")) +
  labs(x="System", y = "RMSE")

bp  +   theme_classic()+
  theme(legend.position = "none")

kruskal.test(rmse ~ systems, data = e2)
pairwise.wilcox.test(e2$rmse, e2$systems,
                     p.adjust.method = "BH")

dat_e2 = data.frame(dens = c(dats$e2_n,dats$e2_c,dats$e2_p),
                    lines = rep(c('Naive','Each Beat','Beat Bopper'),each=27))
dat_e2$lines = ordered(dat_e2$lines,
                       levels = c('Naive','Each Beat','Beat Bopper'))
p2 = ggplot(dat_e2,aes(x=dens, color=lines))+
  geom_density(alpha=0.2)+
  scale_color_manual(values=c("#003f5c", "#7a5195", "#ef5675")) +
  scale_fill_manual(values=c("#999999", "#E69F00", "#56B4E9"))+
  labs(x='E2 RMSE')+ ylab("")+
  theme(legend.position = "none")+
  theme_classic()

###KRUSKAL WALLIST TEST for e3
e3 = my_data[my_data$excerpt=='e3',]
e3$systems = ordered(e3$systems,
                     levels = c('Naive','Each Beat','Beat Bopper'))

bp <- ggplot(e3, aes(x=systems, y=rmse, fill=systems)) + 
  geom_boxplot(fill='#FFFFFF',color=c("#003f5c", "#7a5195", "#ef5675")) +
  labs(x="System", y = "RMSE")

bp  +   theme_classic()+
  theme(legend.position = "none")

kruskal.test(rmse ~ systems, data = e3)
pairwise.wilcox.test(e3$rmse, e3$systems,
                     p.adjust.method = "BH")

dat_e3 = data.frame(dens = c(dats$e3_n,dats$e3_c,dats$e3_p),
                    lines = rep(c('Naive','Each Beat','Beat Bopper'),each=27))
dat_e3$lines = ordered(dat_e3$lines,
                       levels = c('Naive','Each Beat','Beat Bopper'))
p3 = ggplot(dat_e3,aes(x=dens, color=lines))+
  geom_density(alpha=0.2)+
  scale_color_manual(values=c("#003f5c", "#7a5195", "#ef5675")) +
  scale_fill_manual(values=c("#999999", "#E69F00", "#56B4E9"))+
  labs(x='E3 RMSE')+ ylab("")+
  scale_fill_discrete(name = "System", labels = c("Naive", "Each Beat", "Beat Bopper"))+
  theme_classic()

#Plotting all three densities
# library(ggpubr)
# ggarrange(p1+theme(legend.position = "none"), p2+theme(legend.position = "none"), p3+theme(legend.position = c(0.7,0.9))+labs(fill = "Dose (mg)"), 
#           labels = c("a", "b", "c"),
#           ncol = 3, nrow = 1)

library(cowplot)
# arrange the three plots in a single row
prow <- plot_grid( p1 + theme(legend.position="none"),
                   p2 + theme(legend.position="none"),
                   p3 + theme(legend.position="none"),
                   align = 'vh',
                   labels = c("a", "b", "c"),
                   hjust = -1,
                   nrow = 1
)
legend_b <- get_legend(p1 + theme(legend.position="bottom"))
p <- plot_grid( prow, legend_b, ncol = 1, rel_heights = c(1, .2))
p

library(BSDA)
##SIGN TEST
#e1
SIGN.test(x = e3[e3$systems=='Each Beat',]$rmse,
          y = e3[e3$systems=='Beat Bopper',]$rmse,
          alternative = "two.sided",
          conf.level = 0.95)

# ####DATA TRANSFORMATION DID NOT WORK
# library(rcompanion)
# dat = my_data$rmse
# x = 1:length(dat)
# plotNormalHistogram(dat)
# qqnorm(dat,
#        ylab="Sample Quantiles for RMSE")
# qqline(dat, 
#        col="red")
# library(fifer)
# dat_r = boxcoxR(dat)
# plotNormalHistogram(dat_r)
# qqnorm(dat_r,
#        ylab="Sample Quantiles for RMSE")
# qqline(dat_r, 
#        col="red")
# 
# 
# library(fitdistrplus)
# library(logspline)
# ####TESTING FOR DISTRIBUTIONS
# dat = dat_r
# descdist(dat, discrete = FALSE)#, boot=500)
# fg <- fitdist(dat, "beta")
# fln <- fitdist(dat, "lnorm")
# fl <- fitdist(dat, "logis")
# 
# #e1
# ks.test(dats$e2_p,fl)
# 
# f_list <- list(fg, fln, fl)
# # par(mfrow = c(2, 2))
# # plot.legend <- sapply(c(1:length(f_list)), function(x) f_list[[x]]$distname)
# # denscomp(f_list, legendtext = plot.legend)
# # qqcomp(f_list, legendtext = plot.legend)
# # cdfcomp(f_list, legendtext = plot.legend)
# # ppcomp(f_list, legendtext = plot.legend)
# #
# #
# # denscomp(list(fln,fl), legendtext = c("lnorm", "logis"))
# #
# gofstat(list(fg,fln,fl))
# #
# #
# #
# # plot(fit.norm)
# # plot(fit.weibull)
# # plot(fit.gamma)
# # # 
# # # 
# # # 
# # # 
# # dat_e1 = data.frame(dens = c(dats$e1_n,dats$e1_c,dats$e1_p),
# #                     lines = rep(c('Naive','Each Beat','Beat Bopper'),each=27))
# # dat_e1$lines = ordered(dat_e1$lines,
# #                        levels = c('Naive','Each Beat','Beat Bopper'))
# # #dat = rmse
# # #plot(density(dat),main='Density estimate of e1_n')
# # #plot(ecdf(dat),main='Empirial cumulative distribution function for e1_n')
# # #znorm = (dat-mean(dat))/sd(dat)
# # #qqnorm(znorm)
# # #abline(0,1)
# # ggplot(dat_e1,aes(x=dens, color=lines))+
# #   geom_density(alpha=0.2)+
# #   scale_color_manual(values=c("#003f5c", "#7a5195", "#ef5675")) +
# #   scale_fill_manual(values=c("#999999", "#E69F00", "#56B4E9"))+
# #   labs(x='RMSE',y='Density')+
# #   labs(fill="System")+
# #   theme_classic()
# # #   
# # # #qqnorm(my_data[my_data$systems=="Each Beat",]$rmse,
# # # #       main = "Each Beat Q-Q Plot of RMSE Data")
# # # #qqline(my_data[my_data$systems=="Each Beat",]$rmse, col = "red")
# # # 
# # # ####BOX PLOT
# # # boxplot(my_data$rmse ~ my_data$excerpt,
# # #         main = "RMSE by Excerpt",
# # #         xlab = "Excerpt",
# # #         ylab = "RMSE",
# # #         col = rgb(0.0, 0.0, 0.9, 0.3))
# # # 
# # # #SUMMARY STATISTICS
# # # library(stats)
# # # kw.test = kruskal.test(my_data$rmse ~ my_data$excerpt)
# # # kw.test