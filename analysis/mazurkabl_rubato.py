#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 12:28:30 2019

@author: mb
"""
import numpy as np
import os
from scipy import signal
import matplotlib.pyplot as plt
import scipy
from scipy.stats import skewnorm
import glob

path = "/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper_study/MazurkaBL/"
j = 0
#things = np.zeros((46,3)).dtype([('i',int),('name','|S5'),('skew',float)])

names = []
skewness = []
for file in glob.glob(path+"beat_time/*.csv"):
    name = os.path.basename(file)[:5]
    #print j, name
    #tempo_data = np.genfromtxt(path+'beat_time/M07-1beat_time.csv',delimiter=',',skip_header=1,names=None)[:,2:]
    tempo_data = np.genfromtxt(file,delimiter=',',skip_header=1,names=None)[:,2:]
    #loud_data = np.genfromtxt(path+'beat_dyn/M07-1beat_dynNORM.csv',delimiter=',',skip_header=1,names=None)[:,2:]
    
    iois = np.zeros(np.shape(tempo_data))
    for i in range(np.shape(tempo_data)[1]):
        iois[1:,i]=np.diff(tempo_data[:,i])
    
    avg_iois = iois.mean(axis=1)[1:]
    #avg_loud = loud_data.mean(axis=1)
    
    mean = avg_iois.mean()
    var = avg_iois.var()
    std = avg_iois.std()
    skew = scipy.stats.skew(avg_iois)
    kurt = scipy.stats.kurtosis(avg_iois)
    
    #plt.hist(avg_iois,density=True, histtype='stepfilled')
    #plt.figure()
    if name in only_these:
        f,axarr = plt.subplots(2)
        y = avg_iois
        x = np.linspace(min(y),max(y),40)
        y_pdf = scipy.stats.norm.pdf(x,mean,std)
        y_skew_pdf = scipy.stats.skewnorm.pdf(x,*scipy.stats.skewnorm.fit(y))
        axarr[0].plot(60/avg_iois)
        l1, = axarr[1].plot(x,y_pdf,label='PDF')
        l2, = axarr[1].plot(x,y_skew_pdf, label = 'Skew PDF')
        
        n, bins, patches = axarr[1].hist(y,40,density=True,facecolor='g',edgecolor='r', alpha=0.7)
        f.suptitle(name + ' Skew: '+str(skew), fontsize=16)
    #things[j]=[j,name,skew]
    names.append(name)
    skewness.append(skew)
    j+=1

records = np.rec.fromarrays((names,skewness),names=('maz','skew'))
most_skewed = records[records['skew'].argsort()[::-1]]
only_these = most_skewed[:10]['maz']
#sort_things = things[things[:,2].argsort()[::-1]]