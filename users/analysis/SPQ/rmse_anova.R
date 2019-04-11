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

#SUMMARY STATISTICS