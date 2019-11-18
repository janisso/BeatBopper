#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Created on Wed Jul 25 14:55:52 2018

@author: mb
"""

import numpy as np
from numpy import genfromtxt
#import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import scipy as scipy
from scipy import optimize
import warnings
from numpy.linalg import norm
from quaternion import Quaternion
#matplotlib.use('TkAgg')


def update_imu(_quaternion, samplePeriod, gyroscope, accelerometer):
    """
    Perform one update step with data from a IMU sensor array
    :param gyroscope: A three-element array containing the gyroscope data in radians per second.
    :param accelerometer: A three-element array containing the accelerometer data. Can be any unit since a normalized value is used.
    """
    q = _quaternion
    beta = 1
    gyroscope = np.array(gyroscope, dtype=float).flatten()
    #print(accelerometer)
    accelerometer = np.array(accelerometer, dtype=float).flatten()
    #print(accelerometer)
    # Normalise accelerometer measurement
    if norm(accelerometer) is 0:
        warnings.warn("accelerometer is zero")
        return
    accelerometer /= norm(accelerometer)

    # Gradient descent algorithm corrective step
    f = np.array([
        2*(q[1]*q[3] - q[0]*q[2]) - accelerometer[0],
        2*(q[0]*q[1] + q[2]*q[3]) - accelerometer[1],
        2*(0.5 - q[1]**2 - q[2]**2) - accelerometer[2]
    ])
    j = np.array([
        [-2*q[2], 2*q[3], -2*q[0], 2*q[1]],
        [2*q[1], 2*q[0], 2*q[3], 2*q[2]],
        [0, -4*q[1], -4*q[2], 0]
    ])
    step = j.T.dot(f)
    step /= norm(step)  # normalise step magnitude

    # Compute rate of change of quaternion
    qdot = (q * Quaternion(0, gyroscope[0], gyroscope[1], gyroscope[2])) * 0.5 - beta * step.T

    # Integrate to yield quaternion
    q += qdot * samplePeriod
    _quaternion = Quaternion(q / norm(q))  # normalise quaternion
    return _quaternion

class acc_data(object):
    def __init__(self,data):
        self.t = data[:,0]-data[0,0]
        self.ax = data[:,1]
        self.ay = data[:,2]
        self.az = data[:,3]
        self.gx = data[:,4]*(np.pi/180)
        self.gy = data[:,5]*(np.pi/180)
        self.gz = data[:,6]*(np.pi/180)
        self.dt = data[:,7]

#IMPORT TEMPO ANNOTATIONS
f = open('juggle_data.csv')
lines = f.readlines()
lines = lines[:-1]
        
data = genfromtxt(lines,delimiter=',')[1:,:]
jug = acc_data(data)

f, axarr = plt.subplots(6,sharex=True)
axarr[0].plot(jug.t,jug.ax)
axarr[1].plot(jug.t,jug.ay)
axarr[2].plot(jug.t,jug.az)
axarr[3].plot(jug.t,jug.gx)
axarr[4].plot(jug.t,jug.gy)
axarr[5].plot(jug.t,jug.gz)

#magn = np.sqrt(jug.ax**2+jug.ay**2+jug.az**2)
#norm = 1/magn
#norms = magn

'''linx = jug.ax*norms-jug.ax
liny = jug.ay*norms-jug.ay
linz = jug.az*norms-jug.az

#linx = linx - linx.mean()
#liny = liny - liny.mean()
#linz = linz - linz.mean()

f, axarr = plt.subplots(5,sharex=True)
axarr[0].plot(jug.t,magn-1)
axarr[1].plot(jug.t,norms)
axarr[2].plot(jug.t,linx)
axarr[3].plot(jug.t,liny)
axarr[4].plot(jug.t,linz)'''

quaternion = Quaternion(1, 0, 0, 0)

quaternions = np.zeros((len(jug.t),4))
axis = np.zeros((len(jug.t),4))
eulers = np.zeros((len(jug.t),3))

for i in range(1,len(jug.t)):
    samplePeriod = jug.dt[i]#jug.t[i]-jug.t[i-1]
    #samplePeriod = jug.t[i]-jug.t[i-1]
    quaternion = update_imu(quaternion, samplePeriod, [jug.gx[i],jug.gy[i],jug.gz[i]],[jug.ax[i],jug.ay[i],jug.az[i]])
    quaternions[i]=quaternion._q
    axis[i] = quaternion.to_angle_axis()
    eulers[i]=quaternion.to_euler_angles()
    #print(quaternion._q)

f, axarr = plt.subplots(4,sharex=True)
axarr[0].plot(jug.t,quaternions[:,0])
axarr[1].plot(jug.t,quaternions[:,1])
axarr[2].plot(jug.t,quaternions[:,2])
axarr[3].plot(jug.t,quaternions[:,3])



'''velocityx = [0]
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
axarr[2].plot(jug.t,velocityz)'''

'''poptx, pcovx = scipy.optimize.curve_fit(lambda t,a,b,c,d: -a*np.exp(b/d*t)+c,  jug.t,  velocityx)
popty, pcovy = scipy.optimize.curve_fit(lambda t,a,b,c,d: -a*np.exp(b/d*t)+c,  jug.t,  velocityy)
poptz, pcovz = scipy.optimize.curve_fit(lambda t,a,b,c,d: -a*np.exp(b/d*t)+c,  jug.t,  velocityz)


def func(x,a,b,c,d):
    return -a*np.exp(b/d*x)+c

#plt.figure()
#plt.plot(jug.t,velocityx)
f, axarr = plt.subplots(3,sharex=True)
axarr[0].plot(jug.t,velocityx-func(jug.t,poptx[0],poptx[1],poptx[2],poptx[3]))
axarr[1].plot(jug.t,velocityy-func(jug.t,popty[0],popty[1],popty[2],popty[3]))
axarr[2].plot(jug.t,velocityz-func(jug.t,poptz[0],poptz[1],poptz[2],poptz[3]))

plt.show()'''

#x_drift = np.polyfit(np.log(jug.t[1:]),velocityx[1:],1)
#y = x_drift[0]*np.log(jug.t[1:])#+x_drift[1]

#plt.figure()
#plt.plot(jug.t[1:],y)

#plt.plot(velocityx[1:]-y)
#plt.figure()
#plt.plot(jug.t,abs(jug.ax)+abs(jug.ay)+abs(jug.az))

#plt.figure()
#plt.plot(np.diff(jug.t))