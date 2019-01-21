#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 11:45:21 2019

@author: mb
"""

import numpy as np
import os
from scipy import signal
import matplotlib.pyplot as plt
import scipy
from scipy.stats import skewnorm


#Chopin Mazurka Op.7 No.1 By Arthur Rubinstein
#9059-05

path = "/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper_study/MazurkaBL/"
for name in only_these:
    tempo_data = np.genfromtxt(path+'beat_time/'+name+'beat_time.csv',delimiter=',',skip_header=1,names=None)[:,2:]
    loud_data = np.genfromtxt(path+'beat_dyn/'+name+'beat_dynNORM.csv',delimiter=',',skip_header=1,names=None)[:,2:]
    
    iois = np.zeros(np.shape(tempo_data))
    for i in range(np.shape(tempo_data)[1]):
        iois[1:,i]=np.diff(tempo_data[:,i])
    
    avg_iois = iois.mean(axis=1)
    avg_loud = loud_data.mean(axis=1)
    avg_loud = avg_loud/avg_loud.max()
    
    f, axarr = plt.subplots(2,sharex=True)
    f.suptitle(name+'Average IOIs and Loudness')
    axarr[0].plot(iois,color='k',alpha=0.05)
    axarr[0].plot(avg_iois,color='r',lw=2)
    axarr[0].set_ylabel('IOIs')
    
    axarr[1].plot(loud_data,color='k',alpha=0.05)
    axarr[1].plot(avg_loud,color='r',lw=2)
    axarr[1].set_ylabel('Normalised Loudness')
    axarr[1].set_xlabel('Beats')
    #axarr[0].title('Average IOIs and Loudness')
    
    f, axarr = plt.subplots(2,sharex=True)
    f.suptitle(name)
    axarr[0].plot(60./avg_iois)
    axarr[1].plot(np.array(avg_loud*127).astype(int))
    
    #interpolation for MIDI playback
    syn_times = np.cumsum(avg_iois)*1.5
    syn_len = int(syn_times[-1]/0.0064)
    #count_off = 
    
    t = syn_times
    b = np.arange(len(syn_times))
    l = np.array(avg_loud*127).astype(int)
    tvals = np.linspace(0,syn_times[-1],syn_len)
    binterp = np.interp(tvals,t,b)
    linterp = np.interp(tvals,t,l).astype(int)
    
    '''plt.figure()
    plt.plot(t,b)
    plt.plot(tvals,binterp)'''
    
    #expr_perf = np.hstack((b,np.array(avg_loud*127).astype(int)))
    expr_perf = np.vstack((binterp.T,linterp.T)).T
    #expr_perf = np.vstack((b,t,l)).T
    save_path = "/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/midi_files/"+name+'/'
    if not os.path.exists(save_path):                                               # if the path does not exist create it
        os.makedirs(save_path)
    np.savetxt(save_path+name+".csv", expr_perf, delimiter=",")
    
    t_c = np.zeros(7)
    t_c[1:] = np.cumsum(np.full(6,syn_times[1]))
    b_c = np.arange(7)
    t_c_syn_len = int(t_c[-1]/0.0064)
    t_cvals = np.linspace(0,t_c[-1],t_c_syn_len)
    t_bvals = np.interp(t_cvals,t_c,b_c)
    np.savetxt(save_path+name+"countoff.csv", t_bvals, delimiter=",")

'''plt.plot(t_c,b_c)
plt.plot(t_cvals,t_bvals)



playhead = 0
dt = expr_perf[1,1]-expr_perf[0,1]
how_many = int(dt / 0.005)
for i in range(1,len(t)-1):
    for j in range(how_many):
        playhead+=0.005*dt
    dt = expr_perf[i+1,1]-expr_perf[i,1]
    how_many = int(dt / 0.005)'''



#a = np.array([1,2,3,4,5])
#b = np.diff(a)
'''beat_times = tempo_data['pid905905']
ioi = np.zeros(len(beat_times))
ioi[1:] = np.diff(beat_times)
tempo = 60/ioi
loud = loud_data['pid905905']

f, axarr = plt.subplots(2,sharex=True)
axarr[0].plot(tempo)
axarr[1].plot(loud)

plt.figure()
plt.plot(np.arange(len(beat_times)),beat_times)

np.savetxt("beat_times.csv", beat_times-beat_times[0], delimiter=",")'''
#skewnorm.stats