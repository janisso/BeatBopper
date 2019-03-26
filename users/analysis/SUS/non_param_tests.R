#NON parametric tests
#taken from http://rcompanion.org/handbook/F_01.html
rm(list=ls(all=TRUE)) 
.rs.restartR()

library(psych)
library(effsize)
library(coin)
library(dplyr)
library(BSDA)

A = Naive#c(2,4,3,1,2,3,3,2,3,1)
B = Phase#c(3,5,4,2,4,3,5,5,3,2)

cliff.delta(A, B)

wilcox.test(A,B)

g = factor(c(rep("A", length(A)), rep("B", length(B))))
v = c(A, B)
#r = rank(v)
wilcox_test(v ~ g, distribution="exact")
r = rank(v)
dat = data.frame(g, r)
lapply((split(dat, dat$g)), mean)

rA = dat$r[dat$g=="A"]
rB = dat$r[dat$g=="B"]

mean(rA)
mean(rB)

2.3369/sqrt(20)

SIGN.test(Phase, 
          md = 3)

