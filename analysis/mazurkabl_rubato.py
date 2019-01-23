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
import seaborn as sns
import pandas as pd
from mpl_toolkits.axes_grid1 import make_axes_locatable
import peakutils

sns.set(color_codes=True)

path = "/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper_study/MazurkaBL/"
j = 0
#things = np.zeros((46,3)).dtype([('i',int),('name','|S5'),('skew',float)])

#names = ['M07-1','M17-4','M24-2','M24-4','M63-3']
names = 'M24-2'
skewness = []
for file in glob.glob(path+"beat_time/*.csv"):
    name = os.path.basename(file)[:5]
    if name:# in names:#== 'M07-1':#in only_these:
        #print j, name
        #tempo_data = np.genfromtxt(path+'beat_time/M07-1beat_time.csv',delimiter=',',skip_header=1,names=None)[:,2:]
        tempo_data = np.genfromtxt(file,delimiter=',',skip_header=1,names=None)[:,2:]
        timing = np.genfromtxt(file,delimiter=',',skip_header=1,names=None)[:,:2]
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
    
        
        y = avg_iois
        x = np.linspace(min(y),max(y),40)
        y_pdf = scipy.stats.norm.pdf(x,mean,std)
        y_skew_pdf = scipy.stats.skewnorm.pdf(x,*scipy.stats.skewnorm.fit(y))
        
        #plt.figure()
        #sns.jointplot(x='x',y='y',data=avg_iois)
        #plt.plot(avg_iois)
        #sns.boxplot(x=avg_iois)
        
        #plt.figure()
        s = pd.Series(avg_iois)
        q1 = s.describe()['25%']
        q3 = s.describe()['75%']
        iqr = scipy.stats.iqr(avg_iois)
        dist = max(avg_iois)-min(avg_iois)
        frac = 1.4-min(avg_iois)
        thresh = frac/dist
        #thresh = (max(avg_iois)-min(avg_iois))
        #thresh = ((q3+iqr*1.5)-min(avg_iois))/(max(avg_iois)-min(avg_iois))
        indexes = peakutils.indexes(avg_iois, thres=thresh)#thresh/max(avg_iois),min_dist=0)
        if True in (avg_iois[indexes]>1.5):
            
            f,axarr = plt.subplots(2)
            axarr[0].plot(60/avg_iois)
            l1, = axarr[1].plot(x,y_pdf,label='PDF')
            l2, = axarr[1].plot(x,y_skew_pdf, label = 'Skew PDF')
            
            n, bins, patches = axarr[1].hist(y,40,density=True,facecolor='g',edgecolor='r', alpha=0.7)
            f.suptitle(name + ' Skew: '+str(skew)+' STD: '+str(std), fontsize=16)
            fig, axarr = plt.subplots()
            axarr.plot(avg_iois)
            axarr.axhline(y=1.4)#q3+iqr*1.5)
            #axarr.plot(peaks,avg_iois[peaks])
            axarr.axhline(y=s.describe()['min'])#-q1*1.5)
            
            print name,
            print np.vstack((indexes,timing[indexes].T)).T
            axarr.plot(indexes,avg_iois[indexes],'o')
            #axarr.axhline(y=s.describe()['75%'])#+s.describe()['75%']*1.5)
            divider = make_axes_locatable(axarr)
            ax_histy = divider.append_axes("right", 1.2, pad=0.1, sharey=axarr)
            ax_histy.hist(avg_iois,bins=40,orientation='horizontal')
            ax_boxy = divider.append_axes("left", 1.2, pad=0.1, sharey=axarr)
            sns.boxplot(x=avg_iois,orient='v')
            fig.suptitle(name, fontsize=16)     
        #things[j]=[j,name,skew]
        #names.append(name)
        #skewness.append(std)
    #j+=1

'''records = np.rec.fromarrays((names,skewness),names=('maz','skew'))
most_skewed = records[records['skew'].argsort()[::-1]]
only_these = most_skewed[:10]['maz']'''
#sort_things = things[things[:,2].argsort()[::-1]]
