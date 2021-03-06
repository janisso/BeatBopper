rm(list=ls(all=TRUE)) 
.rs.restartR()

dats = read.csv("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/SPQ/intention_rmse.csv", header = TRUE)

my_data <- melt(dats, id="id")

#rmse = c(dats$e3_n,dats$e3_c,dats$e3_p)
my_data$variable = rep(c(rep('Naive',27),rep('Each Beat',27),rep('BB',27)),3)
names(my_data)[2] <- "systems"
names(my_data)[3] <- "rmse"
#my_data = data.frame(rmse,systems)
my_data$systems = ordered(my_data$systems,
                          levels = c('Naive','Each Beat','BB'))


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
# Change  automatically color by groups
bp <- ggplot(my_data, aes(x=systems, y=rmse, fill=systems)) + 
  geom_boxplot() +
  labs(x="System", y = "RMSE")

bp + scale_fill_manual(values=c("#003f5c", "#7a5195", "#ef5675")) + theme_classic()

library("ggpubr")
ggline(my_data, x = "systems", y = "rmse", 
       add = c("mean_se", "jitter"), 
       order = c("Borch", "Each Beat", "Phase"),
       ylab = "Rmse", xlab = "Treatment")


res.aov <- aov(rmse ~ systems, data = my_data)
summary(res.aov)
TukeyHSD(res.aov)

library(multcomp) 
summary(glht(res.aov, linfct = mcp(systems = "Tukey")))
plot(res.aov, 1)

library(car)
leveneTest(rmse ~ systems, data = my_data)

oneway.test(rmse ~ systems, data = my_data)
pairwise.t.test(my_data$rmse, my_data$systems,
                p.adjust.method = "BH", pool.sd = FALSE)

# 2. Normality
plot(res.aov, 2)


# Extract the residuals
aov_residuals <- residuals(object = res.aov )
# Run Shapiro-Wilk test
shapiro.test(x = aov_residuals )

kruskal.test(rmse ~ systems, data = my_data)

