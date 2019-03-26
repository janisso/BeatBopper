df = read.csv("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/SPQ/rmse_plot/ioi_sig.csv", header = TRUE)

beat = rep(df$beat,4)
Signal = c(rep('Template',16),rep('Each Beat',16),rep('Borch',16),rep('Phase',16))
ioi = c(df$m_ioi,df$e_ioi,df$b_ioi,df$p_ioi)

new_df = data.frame(beat,Signal,ioi)
new_df$Signal = factor(new_df$Signal,
                     levels=c('Template','Each Beat','Borch','Phase'))

# ggplot(df, aes(beat)) +
#   geom_line(aes(y=m_ioi))+
#   geom_line(aes(y=e_ioi),linetype = "dashed") +
#   geom_line(aes(y=b_ioi),linetype = "dotted") + 
#   geom_line(aes(y=p_ioi),linetype = "twodash") +
#   scale_color_manual(values=c("#003f5c","#003f5c", "#7a5195", "#ef5675")) +
#   theme_minimal()

ggplot(new_df, aes(x=beat, y=ioi, group=Signal)) +
  geom_line(aes(linetype=Signal, color=Signal))+
  scale_color_manual(values=c("black","#003f5c", "#7a5195", "#ef5675"))+
  scale_linetype_manual(values=c("solid","dashed", "dotted","twodash"))+
  labs(title="Comparison of participant IOIs to template", x="Score time (beats)", y = "IOI (s)")+
  xlim(0, 16)+
  geom_rect(aes(xmin = 7, xmax = 12, ymin = -Inf, ymax = Inf),fill="blue")+
  theme_minimal()
