library("reshape2")
library('ggplot2')
library(ggthemes)
dats = read.csv('/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/DRIFT/drift_t.csv')
dats_long <- melt(dats, id="beat")  # convert to long format

p1 = ggplot(data=tail(idx,-1),
                aes(x=range, y = ioi))+
  geom_line(size=0.5)+
  theme_classic()+
  theme(axis.title.y = element_text(margin = margin(t = 0, r = 10, b = 0, l = 0)))+
  labs(y = "IOI (s)")+theme(axis.title.x=element_blank(),
                            axis.text.x=element_blank(),
                            axis.ticks.x=element_blank())
 
dats_long[dats_long$variable=='borch',]$variable = "Naive"

p2 = ggplot(data=dats_long,
       aes(x=beat, y = value, colour=variable))+
  geom_line(aes(linetype=variable, color=variable))+
  scale_color_manual(values=c("#003f5c", "#7a5195", "#ef5675"))+
  scale_linetype_manual(values=c("dashed", "dotted","twodash"))+
  scale_fill_discrete(name = "System", labels = c("Each Beat", "Borch", "Phase"))+
  theme_classic()+
  theme(axis.title.y = element_text(margin = margin(t = 0, r = 10, b = 0, l = 0)))+
  #theme(text=element_text(family="Helvetica", size=10))+
  theme(legend.title=element_blank())+
  theme(legend.position = c(0.9,0.8))+
  labs(x="Score time (beats)", y = "Drift (s)")

grid.newpage()
#grid.draw(rbind(ggplotGrob(p1),ggplotGrob(p2),size="last"))
pushViewport(viewport(layout = grid.layout(2, 1)))
print(p2, vp = viewport(layout.pos.row = 2, layout.pos.col=1))
print(p1, vp = viewport(layout.pos.row = 1, layout.pos.col=1))

vel_data = read.csv('/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/DRIFT/hand_vel.csv')
idx = read.csv('/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/DRIFT/idx.csv')
idx$time = vel_data[idx$idx,]$time
idx$ioi = c(0,diff(idx$time))
idx$tempo = 60/idx$ioi

p1 = ggplot(data=vel_data,
       aes(x=time, y = vel))+
  geom_line(size=0.5)+
  geom_vline(data = idx, aes(xintercept = as.numeric(time)),color="gray",size=0.5)+
  theme_classic()+
  theme(axis.ticks.length=unit(0.5,"cm"))+
  theme(axis.title.y = element_text(margin = margin(t = 0, r = 10, b = 0, l = 0)))+
  labs(y = "Velocity (mm/s)")+theme(axis.title.x=element_blank(),
                                    axis.text.x=element_blank(),
                                    axis.ticks.x=element_blank())

p2 = ggplot(data=tail(idx,-1),
       aes(x=time, y = ioi))+
  geom_line(size=0.5)+
  theme_classic()+
  theme(axis.title.y = element_text(margin = margin(t = 0, r = 10, b = 0, l = 0)))+
  labs(y = "IOI (s)")+theme(axis.title.x=element_blank(),
                            axis.text.x=element_blank(),
                            axis.ticks.x=element_blank())

p3 = ggplot(data=tail(idx,-1),
       aes(x=time, y = tempo))+
  geom_line(size=0.5)+
  theme_classic()+
  theme(axis.title.y = element_text(margin = margin(t = 0, r = 10, b = 0, l = 0)))+
  labs(x="Time (s)", y = "Tempo (BPM)")
library(grid)
grid.newpage()
grid.draw(rbind(ggplotGrob(p1),ggplotGrob(p2),ggplotGrob(p3),size="last"))