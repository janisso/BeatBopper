df = read.csv("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/P_INFO/p_info.csv", header = TRUE)
colnames(df) = c('ts','id','age','sex','hearing','instr','names','years','num_instr','practice','conductor','cond_exp','music','music_styles','classical','enjoy','comment')
drops = c('ts','hearing','names','cond_exp','music','music_styles','classical','enjoy','comment')
keeps = df[ , !(names(df) %in% drops)]

summary(keeps)
keeps[keeps$instr=='No',]$practice=NA
keeps$num_instr

