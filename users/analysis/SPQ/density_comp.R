rm(list=ls(all=TRUE))
.rs.restartR()

library(dplyr)
ks_func <- function(dats) {
  df = data.frame(ks=seq(1:27),t=seq(1:27))#,seq(1:28))
  #names(df) = c('s','t')#,'s')
  counts = 1
  ref = diff(na.omit(dats$m))
  dats = select(dats,-m)
  for(i in names(dats)){
    dat = diff(unlist(na.omit(dats[i])))
    #print(dat)
    #print(k_s)
    #if (length(dat)<3){
    #  df[counts,]$ks = 0
    #  df[counts,]$t = 0
    #} else{
      #k_s = ks.test(dat,ref)
      #t_s = t.test(dat, ref, var.equal = FALSE)
      t_s = wilcox.test(dat, ref, var.equal = FALSE)
      df[counts,]$ks = sd(dat)
      df[counts,]$t = t_s$p.value
      hist(dat, main=c(i,sd(dat)))
      plot(ccf(dat,ref),main=c(i,t_s$p.value))
    #}
    #df[counts,]$m = mean(unlist(na.omit(dats[i])),na.rm=TRUE)
    #df[counts,]$s = sd(unlist(na.omit(dats[i])),na.rm=TRUE)
    counts = counts + 1
  }
  return(df)
}

get_cors <- function(dats){
  df = seq(1:27)
  counts = 1
  ref = diff(na.omit(dats$m))
  dats = select(dats,-m)
  for(i in names(dats)){
    dat = diff(unlist(na.omit(dats[i])))
    d = ccf(dat, ref, lag = 0, plot = FALSE)
    df[counts]=d$acf
    counts = counts + 1
  }
  return(df)
}

grid_arrange_shared_legend <- function(...) {
  plots <- list(...)
  g <- ggplotGrob(plots[[1]] + theme(legend.position="bottom"))$grobs
  legend <- g[[which(sapply(g, function(x) x$name) == "guide-box")]]
  lheight <- sum(legend$height)
  grid.arrange(
    do.call(arrangeGrob, lapply(plots, function(x)
      x + theme(legend.position="none"))),
    legend,
    ncol = 1,
    heights = unit.c(unit(1, "npc") - lheight, lheight))
}

Find_Max_CCF<- function(a,b)
{
  d <- ccf(a, b, plot = FALSE)
  if (length(d) > 3){
    cor = d$acf[,,1]
    lag = d$lag[,,1]
    d$res = data.frame(cor,lag)
    d$res_max = d$res[which.max(d$res$cor),]
  }
  return(d)
} 

cross_c = function(dats1,dats2){
  df = data.frame(c=seq(1:27),
                  l=seq(1:27))#,seq(1:28))
  #names(df) = c('s','t')#,'s')
  counts = 1
  #ref = diff(na.omit(dats$m))
  dats1 = select(dats1,-m)
  dats2 = select(dats2,-m)
  for(i in names(dats1)){
    ref = diff(unlist(na.omit(dats2[i])))
    dat = diff(unlist(na.omit(dats1[i])))
    #dat.ccf = ccf(dat,ref,plot=FALSE)
    #print(length(ref))
    if (length(dat) < 4){
      d = NA
      res_max = NA
      res_max$cor = NA
      res_max$lag = NA
      d$res_max = res_max
    }
    else{
      d = Find_Max_CCF(dat,ref)
    }
    df[counts,]$c = d$res_max$cor
    df[counts,]$l = d$res_max$lag
    counts = counts + 1
  }
  return(df)
}

e1_m1_h = read.csv("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/SPQ/e1_m1_h.csv", header = TRUE)
e1_m2_h = read.csv("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/SPQ/e1_m2_h.csv", header = TRUE)
e1_m3_h = read.csv("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/SPQ/e1_m3_h.csv", header = TRUE)

e1_m1_m = read.csv("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/SPQ/e1_m1_m.csv", header = TRUE)
e1_m2_m = read.csv("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/SPQ/e1_m2_m.csv", header = TRUE)
e1_m3_m = read.csv("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/SPQ/e1_m3_m.csv", header = TRUE)

e1_m1_l = cross_c(e1_m1_h,e1_m1_m)
e1_m2_l = cross_c(e1_m2_h,e1_m2_m)
e1_m3_l = cross_c(e1_m3_h,e1_m3_m)

u1 = get_cors(e1_m1_m)
u2 = get_cors(e1_m2_m)
u3 = get_cors(e1_m3_m)

cors_e1 = data.frame(u1,u2,u3)
cors_e1 = data.frame(e1_m1_l$c,e1_m2_l$c,e1_m3_l$c)

e1_obj_best = apply(cors_e1, 1, FUN=which.max)-1
e1_obj_wors = apply(cors_e1, 1, FUN=which.min)-1

###CONFUSION MATRIX RUN pros_cons.R to get hem
library(caret)
#ting[ting$sub_best==3,]$sub_best=NA
#ting[ting$sub_wors==3,]$sub_wors=NA
e1_pos = confusionMatrix(e1_obj_best,factor(pros$e1)) 
e1_neg = confusionMatrix(e1_obj_wors,factor(cons$e1))
# library(xtable)
# xtable(t(pos$byClass))
# xtable(t(neg$byClass))

#cors_e1.melt = melt(cors_e1)

ggplot(cors_e1.melt, aes(x=variable, y=value)) + 
  geom_boxplot()

library(reshape2)
lags = data.frame(n=e1_m1_l$l,c=e1_m2_l$l,p=e1_m3_l$l)
lags.melt = melt(lags)
cors = data.frame(n=e1_m1_l$c,c=e1_m2_l$c,p=e1_m3_l$c)
cors.melt = melt(cors)

library(ggplot2)
ggplot(lags.melt, aes(x=variable, y=value)) + 
   geom_boxplot()
 
ggplot(cors.melt, aes(x=variable, y=value)) + 
   geom_boxplot()

e2_m1_h = read.csv("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/SPQ/e2_m1_h.csv", header = TRUE)
e2_m2_h = read.csv("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/SPQ/e2_m2_h.csv", header = TRUE)
e2_m3_h = read.csv("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/SPQ/e2_m3_h.csv", header = TRUE)

e2_m1_m = read.csv("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/SPQ/e2_m1_m.csv", header = TRUE)
e2_m2_m = read.csv("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/SPQ/e2_m2_m.csv", header = TRUE)
e2_m3_m = read.csv("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/SPQ/e2_m3_m.csv", header = TRUE)

e2_m1_l = cross_c(e2_m1_h,e2_m1_m)
e2_m2_l = cross_c(e2_m2_h,e2_m2_m)
e2_m3_l = cross_c(e2_m3_h,e2_m3_m)

u1 = get_cors(e2_m1_m)
u2 = get_cors(e2_m2_m)
u3 = get_cors(e2_m3_m)

e2_m1_l = cross_c(e2_m1_h,e2_m1_m)
e2_m2_l = cross_c(e2_m2_h,e2_m2_m)
e2_m3_l = cross_c(e2_m3_h,e2_m3_m)

u1 = get_cors(e2_m1_m)
u2 = get_cors(e2_m2_m)
u3 = get_cors(e2_m3_m)

cors_e2 = data.frame(u1,u2,u3)

e2_obj_best = apply(cors_e2, 1, FUN=which.max)-1
e2_obj_wors = apply(cors_e2, 1, FUN=which.min)-1

###CONFUSION MATRIX RUN pros_cons.R to get hem
#library(caret)
#ting[ting$sub_best==3,]$sub_best=NA
#ting[ting$sub_wors==3,]$sub_wors=NA
e2_pos = confusionMatrix(factor(pros$e2),e2_obj_best) 
e2_neg = confusionMatrix(factor(cons$e2),e2_obj_wors)

e3_m1_h = read.csv("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/SPQ/e3_m1_h.csv", header = TRUE)
e3_m2_h = read.csv("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/SPQ/e3_m2_h.csv", header = TRUE)
e3_m3_h = read.csv("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/SPQ/e3_m3_h.csv", header = TRUE)

e3_m1_m = read.csv("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/SPQ/e3_m1_m.csv", header = TRUE)
e3_m2_m = read.csv("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/SPQ/e3_m2_m.csv", header = TRUE)
e3_m3_m = read.csv("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/SPQ/e3_m3_m.csv", header = TRUE)

e3_m1_l = cross_c(e3_m1_h,e3_m1_m)
e3_m2_l = cross_c(e3_m2_h,e3_m2_m)
e3_m3_l = cross_c(e3_m3_h,e3_m3_m)

u1 = get_cors(e3_m1_m)
u2 = get_cors(e3_m2_m)
u3 = get_cors(e3_m3_m)

#cors_e3 = data.frame(u1,u2,u3)
e3_m1_l = cross_c(e3_m1_h,e3_m1_m)
e3_m2_l = cross_c(e3_m2_h,e3_m2_m)
e3_m3_l = cross_c(e3_m3_h,e3_m3_m)

u1 = get_cors(e3_m1_m)
u2 = get_cors(e3_m2_m)
u3 = get_cors(e3_m3_m)

cors_e3 = data.frame(u1,u2,u3)

e3_obj_best = apply(cors_e3, 1, FUN=which.max)-1
e3_obj_wors = apply(cors_e3, 1, FUN=which.min)-1

###CONFUSION MATRIX RUN pros_cons.R to get hem
#library(caret)
#ting[ting$sub_best==3,]$sub_best=NA
#ting[ting$sub_wors==3,]$sub_wors=NA
e3_pos = confusionMatrix(factor(pros$e3),e1_obj_best) 
e3_neg = confusionMatrix(factor(cons$e3),e1_obj_wors)

####


####
e1_m1_l = rep('Naive',27)
e1_m1_c = colSums(!is.na(e1_m1_h[1:27]))
e1_m2_l = rep('Each Beat',27)
e1_m2_c = colSums(!is.na(e1_m2_h[1:27]))
e1_m3_l = rep('Beat Bopper',27)
e1_m3_c = colSums(!is.na(e1_m3_h[1:27]))
e1_df = data.frame(excerpt = rep('e1',81),
                   system=c(e1_m1_l,e1_m2_l,e1_m3_l),
                   count=c(e1_m1_c,e1_m2_c,e1_m3_c))

e1_df$system = ordered(e1_df$system,
                          levels = c('Naive','Each Beat','Beat Bopper'))

p1 = ggplot(data=e1_df, aes(count))+#, y=freq_var,fill=system_var)) +
  geom_bar(aes(fill=system), position=position_dodge())+
  scale_fill_manual(values=c("#003f5c", "#7a5195", "#ef5675",'#ffa600'))+
  labs(x="Beats", y = "Frequency")+
  labs(fill = "System")+
  xlim(12.5,18.5)+
  theme(plot.margin = unit(c(6,0,6,0), "pt"))+
  theme_classic()

  
###E2
e2_m1_l = rep('Naive',27)
e2_m1_c = colSums(!is.na(e2_m1_h[1:27]))
e2_m2_l = rep('Each Beat',27)
e2_m2_c = colSums(!is.na(e2_m2_h[1:27]))
e2_m3_l = rep('Beat Bopper',27)
e2_m3_c = colSums(!is.na(e2_m3_h[1:27]))
e2_df = data.frame(excerpt = rep('e2',81),
                   system=c(e2_m1_l,e2_m2_l,e2_m3_l),
                   count=c(e2_m1_c,e2_m2_c,e2_m3_c))

e2_df$system = ordered(e2_df$system,
                       levels = c('Naive','Each Beat','Beat Bopper'))

p2 = ggplot(data=e2_df, aes(count))+#, y=freq_var,fill=system_var)) +
  geom_bar(aes(fill=system), position=position_dodge())+
  scale_fill_manual(values=c("#003f5c", "#7a5195", "#ef5675",'#ffa600'))+
  labs(x="Beats")+
  labs(fill = "System")+
  theme(plot.margin = unit(c(6,0,6,0), "pt"))+ ylab("")+
  theme_classic(base_size = 11)

####e3
e3_m1_l = rep('Naive',27)
e3_m1_c = colSums(!is.na(e3_m1_h[1:27]))
e3_m2_l = rep('Each Beat',27)
e3_m2_c = colSums(!is.na(e3_m2_h[1:27]))
e3_m3_l = rep('Beat Bopper',27)
e3_m3_c = colSums(!is.na(e3_m3_h[1:27]))
e3_df = data.frame(excerpt = rep('e3',81),
                   system=c(e3_m1_l,e3_m2_l,e3_m3_l),
                   count=c(e3_m1_c,e3_m2_c,e3_m3_c))

e3_df$system = ordered(e3_df$system,
                       levels = c('Naive','Each Beat','Beat Bopper'))

p3 = ggplot(data=e3_df, aes(count))+#, y=freq_var,fill=system_var)) +
  geom_bar(aes(fill=system), position=position_dodge())+
  scale_fill_manual(values=c("#003f5c", "#7a5195", "#ef5675",'#ffa600'))+
  labs(x="Beats", y = "Frequency")+
  labs(fill = "System")+
  theme(plot.margin = unit(c(6,0,6,0), "pt"))+ ylab("")+
  theme_classic(base_size = 11)


####PLOTTING FREQS
#library(ggpubr)
#ggarrange(p1+theme(legend.position = "none"), p2+theme(legend.position = "bottom"), p3+theme(legend.position = 'none')+labs(fill = "Dose (mg)"), 
#          labels = c("a", "b", "c"),
#          ncol = 3, nrow = 1)

#df = rbind(e1_df,e2_df,e3_df)

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
####PLOTTING MEDIANS
library(rcompanion)
Sum = groupwiseMedian(data = df,
                      group = c("excerpt","system"),
                      var = "count",
                      R=5000)

pd = position_dodge(.2)
ggplot(df, aes(x=excerpt,
                y=count,
                color=system)) +
  geom_point(shape=15, size=4, position=pd) +
  theme_bw() +
  theme(axis.title = element_text(face = "bold")) +
  
  ylab("Median Likert score")



#E1
e1_d1 = ks_func(e1_m1_h)
e1_d2 = ks_func(e1_m2_h)
e1_d3 = ks_func(e1_m3_h)


na.omit(dats$m)
library(ggplot2)
hist(diff(unlist(na.omit(e1_m1_h$X7))))
hist(diff(unlist(na.omit(e1_m1_h$m))))


dens1 = data.frame(e1_d1$t,e1_d2$t,e1_d3$t)
names(dens1) = c('n','c','p')#,'p2','m2','s2','p3','m3','s3')
# m_dens1 = melt(dens1)
# #m_dens1$value = log10(m_dens1$value)
# m_dens1$r = rep(c(seq(1,28)))
# ggplot(data = m_dens1, aes(x = variable, y = r)) +
#   geom_tile(aes(fill = value))
dens1<0.05

#E2
e2_d1 = ks_func(e2_m1_h)
e2_d2 = ks_func(e2_m2_h)
e2_d3 = ks_func(e2_m3_h)

dens2 = data.frame(e2_d1$t,e2_d2$t,e2_d3$t)
names(dens2) = c('n','c','p')
# m_dens2 = melt(dens2)
# m_dens2$value = log10(m_dens2$value)
# m_dens2$r = rep(c(seq(1,28)))
# ggplot(data = m_dens2, aes(x = variable, y = r)) +
#   geom_tile(aes(fill = value))

dens2<0.05

#E3
e3_d1 = ks_func(e3_m1_h)
e3_d2 = ks_func(e3_m2_h)
e3_d3 = ks_func(e3_m3_h)

dens3 = data.frame(e3_d1$t,e3_d2$t,e3_d3$t)
names(dens3) = c('n','c','p')
# m_dens3 = melt(dens3)
# m_dens3$value = log10(m_dens3$value)
# m_dens3$r = rep(c(seq(1,28)))
# ggplot(data = m_dens3, aes(x = variable, y = r)) +
#   geom_tile(aes(fill = value))

dens3<0.1

library(ggplot2)
ggplot(dens, aes(r)) + 
  geom_line(aes(y = d1, colour = "d1")) + 
  geom_line(aes(y = d2, colour = "d2")) +
  geom_line(aes(y = d3, colour = "d3"))
# ggplot(data=dens,
#        aes(x=variable,y=value,colour=variable))+
#   geom_line()


library(changepoint)
dat = diff(unlist(na.omit(e1_m1_h$X5)))*100
dat.amoc = cpt.mean(dat)
cpts(dat.amoc)
plot(dat.amoc)
#m1.cumsum = cpt.mean(dat,pen.value=1,penalty='Manual',test.stat='CUSUM')
#cpt.mean(dat, penalty="MBIC", pen.value=0, method="AMOC", Q=5, test.stat="Normal", class=TRUE, param.estimates=TRUE,minseglen=1)