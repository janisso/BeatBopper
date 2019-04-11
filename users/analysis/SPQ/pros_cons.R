###HERE WILL CHECK OUT THEEASON WHY PEOPLE CHOSE THE SYSTEMS THEY CHOSE
#####FOR SYSTEM
dats = read.csv("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/SPQ/chisq_system.csv", header = TRUE)
dats$pref.f[dats$pref == 0] = 'Naive'
dats$pref.f[dats$pref == 1] = 'Each Beat'
dats$pref.f[dats$pref == 2] = 'Beat Bopper'
dats$pref.f[dats$pref == 3] = 'Not Sure'

dats$question = factor(dats$question,
                       levels=c('q1','q2','q3','q4','q5','q6'))
dats$excerpt = factor(dats$excerpt,
                      levels=c('0','1','2'))
dats$pref.f = factor(dats$pref.f,
                     levels=c('Naive','Each Beat','Beat Bopper','Not Sure'))

q1 = dats[dats$question=='q1',]
q6 = dats[dats$question=='q6',]

e1 = q1[q1$excerpt==0,]$pref
e2 = q1[q1$excerpt==1,]$pref
e3 = q1[q1$excerpt==2,]$pref

pros = data.frame(e1,e2,e3)

e1 = q6[q6$excerpt==0,]$pref
e2 = q6[q6$excerpt==1,]$pref
e3 = q6[q6$excerpt==2,]$pref

cons = data.frame(e1,e2,e3)

pros[pros==3]=NA
cons[cons==3]=NA

