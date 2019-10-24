#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 14:55:52 2018

@author: mb
"""

import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt

class acc_data(object):
    def __init__(self,data):
        self.t = data[:,0]-data[0,0]
        self.ax = data[:,1]
        self.ay = data[:,2]
        self.az = data[:,3]
        self.gx = data[:,4]
        self.gy = data[:,5]
        self.gz = data[:,6]

#IMPORT TEMPO ANNOTATIONS
data = genfromtxt('juggle_data.csv',delimiter=',')[1:,:]
jug = acc_data(data)

f, axarr = plt.subplots(6,sharex=True)
axarr[0].plot(jug.t,jug.ax)
axarr[1].plot(jug.t,jug.ay)
axarr[2].plot(jug.t,jug.az)
axarr[3].plot(jug.t,jug.gx)
axarr[4].plot(jug.t,jug.gy)
axarr[5].plot(jug.t,jug.gz)

magn = np.sqrt(jug.ax**2+jug.ay**2+jug.az**2)
norm = 1/magn

linx = jug.ax*norm-jug.ax
liny = jug.ay*norm-jug.ay
linz = jug.az*norm-jug.az

linx = linx - linx.mean()
liny = liny - liny.mean()
linz = linz - linz.mean()

f, axarr = plt.subplots(5,sharex=True)
axarr[0].plot(jug.t,magn-1)
axarr[1].plot(jug.t,norm)
axarr[2].plot(jug.t,linx)
axarr[3].plot(jug.t,liny)
axarr[4].plot(jug.t,linz)

velocityx = [0]
velocityy = [0]
velocityz = [0]
for i in range(0,len(linx)-1):
    velocityx.append(velocityx[-1] + linx[i] * (jug.t[i+1])-jug.t[i])
    velocityy.append(velocityy[-1] + liny[i] * (jug.t[i+1])-jug.t[i])
    velocityz.append(velocityz[-1] + linz[i] * (jug.t[i+1])-jug.t[i])



#velx = np.cumsum(linx[1:])*np.diff(jug.t)
#vely = np.cumsum(liny[1:])*np.diff(jug.t)
#velz = np.cumsum(linz[1:])*np.diff(jug.t)

f, axarr = plt.subplots(3,sharex=True)
axarr[0].plot(jug.t,velocityx)
axarr[1].plot(jug.t,velocityy)
axarr[2].plot(jug.t,velocityz)

x_drift = np.polyfit(np.log(jug.t[1:]),velocityx[1:],1)
y = x_drift[0]*np.log(jug.t[1:])+x_drift[1]

#plt.plot(velocityx[1:]-y)
#plt.figure()
#plt.plot(jug.t,abs(jug.ax)+abs(jug.ay)+abs(jug.az))

#plt.figure()
#plt.plot(np.diff(jug.t))