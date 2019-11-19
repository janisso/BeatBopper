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
from calibraxis import Calibraxis
#matplotlib.use('TkAgg')

c = Calibraxis()
cal_points = np.array([[0.07778838, 0.02505269, 0.88501839],
                   [ 0.73871366,  0.0255498,  -0.81387024],
                   [-0.95695496, -0.01158575,  0.11527143],
                   [ 0.42802767,  0.75920515, -0.6072115 ],
                   [ 0.99437399, -0.11401009,  0.02588071],
                   [-0.04117689,  0.20844233,  0.85707983],
                   [ 0.85112945,  0.02989109, -0.67080324],
                   [ 0.90229526,  0.25129969, -0.49528233],
                   [-0.25559073, -0.28405265,  0.80770797],
                   [ 0.99941998,  0.03766609, -0.04686234],
                   [0.04151319, 1.0228318,  0.14966903]])
# Add points to calibration object's storage.
c.add_points(cal_points)
# Run the calibration parameter optimization.
c.calibrate_accelerometer()

def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / N

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
        #self.t = data[:,0]-data[0,0]
        N = 1
        self.ax = running_mean(data[:,1],N)#-(-0.01950705)
        self.ay = running_mean(data[:,2],N)#-(-0.05369358)
        self.az = running_mean(data[:,3],N)#-(1-0.88403344)
        self.gx = (data[N-1:,4]*(np.pi/180))#-0.01372574
        self.gy = (data[N-1:,5]*(np.pi/180))#-0.0159745
        self.gz = (data[N-1:,6]*(np.pi/180))#-(-0.06697223)
        self.dt = data[N-1:,7]
        self.t = np.cumsum(self.dt)-self.dt[0]

class raw_data(object):
    def __init__(self,data):
        #self.t = data[:,0]-data[0,0]
        self.ax = data[:,1]
        self.ay = data[:,2]
        self.az = data[:,3]
        self.gx = data[:,4]
        self.gy = data[:,5]
        self.gz = data[:,6]
        self.dt = data[:,7]
        self.t = np.cumsum(self.dt)-self.dt[0]
        
def rot_point(arr,_quaternion):
    x = arr[0]
    y = arr[1]
    z = arr[2]
    u_q = Quaternion(0, x, y, z)
    _q_n = _quaternion._q/np.sqrt(_quaternion._q[0]**2+_quaternion._q[1]**2+_quaternion._q[2]**2+_quaternion._q[3]**2)
    temp_q = Quaternion(_q_n)
    v_q = temp_q.__mul__(u_q)
    v_q = v_q.__mul__(temp_q.conj())
    v = v_q._q
    return v
    

#IMPORT TEMPO ANNOTATIONS
f = open('juggle_data.csv')
lines = f.readlines()
lines = lines[:-1]
        
data = genfromtxt(lines,delimiter=',')[1:,:]
jug = acc_data(data)
avg_x = jug.ax.mean()
avg_y = jug.ay.mean()
avg_z = jug.az.mean()

print(np.array([jug.ax.mean(),jug.ay.mean(),jug.az.mean()]))
print(np.array([jug.gx.mean(),jug.gy.mean(),jug.gz.mean()]))

r = open('raw_juggle_data.csv')
r_lines = r.readlines()
r_lines = r_lines[:-1]
raw_data = genfromtxt(r_lines,delimiter=',')[1:,1:-1]
print(raw_data.T.mean(axis=1))


#CALIBRATION ROUTINE
points = np.zeros((len(jug.t),3))
points[:,0]=jug.ax
points[:,1]=jug.ay
points[:,2]=jug.az


new_points = np.array(c.batch_apply(points))
#new_points = points
'''c = Calibraxis()
# Add points to calibration object's storage.
c.add_points(points)
# Run the calibration parameter optimization.
c.calibrate_accelerometer()
c.batch_apply(points)'''

jug.ax = new_points[:,0]
jug.ay = new_points[:,1]
jug.az = new_points[:,2]

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
Rs = np.zeros((len(jug.t),4))
new_point = np.zeros((len(jug.t),3))

#gravity = np.array([0, 0, 1])
#plt.figure()
for i in range(0,len(jug.t)):
    samplePeriod = jug.dt[i]#jug.t[i]-jug.t[i-1]
    #samplePeriod = jug.t[i]-jug.t[i-1]
    quaternion = update_imu(quaternion, samplePeriod, [jug.gx[i],jug.gy[i],jug.gz[i]],[jug.ax[i],jug.ay[i],jug.az[i]])
    quaternions[i]=quaternion._q
    axis[i] = quaternion.to_angle_axis()
    eulers[i]=quaternion.to_euler_angles()
    temp_point = rot_point([jug.ax[i],jug.ay[i],jug.az[i]],quaternion)
    new_point[i] = temp_point[1:]
    #new_point[i,2] -= 1
    #print(temp_point)
    #plt.plot(i,temp_point[0],'x')
    #theta = axis[i,0]
    #theta = axis[i,0]
    #theta = axis[i,0]
    #Rs[i]=
    #print(quaternion._q)

#gravity_vec = np.array([jug.ax.mean(),jug.ay.mean(),jug.az.mean()])
#print(gravity_vec)
#gravity_vec = np.array([0.03754126, 0.03242338, 0.88529325])
gravity_vec = np.array([0, 0, 0.88403344])

lin_acc = new_point - gravity_vec
#lin_acc = new_point - gravity_vec


f, axarr = plt.subplots(3,sharex=True)
axarr[0].plot(jug.t,lin_acc[:,0])
axarr[1].plot(jug.t,lin_acc[:,1])
axarr[2].plot(jug.t,lin_acc[:,2])



'''f, axarr = plt.subplots(4,sharex=True)
axarr[0].plot(jug.t,quaternions[:,0])
axarr[1].plot(jug.t,quaternions[:,1])
axarr[2].plot(jug.t,quaternions[:,2])
axarr[3].plot(jug.t,quaternions[:,3])'''


velocityx = [0]
velocityy = [0]
velocityz = [0]
for i in range(1,len(new_point)):
    velocityx.append(velocityx[-1] + lin_acc[i,0] * (jug.dt[i]))
    velocityy.append(velocityy[-1] + lin_acc[i,1] * (jug.dt[i]))
    velocityz.append(velocityz[-1] + lin_acc[i,2] * (jug.dt[i])-0.001515375817199184)

#velx = np.cumsum(linx[1:])*np.diff(jug.t)
#vely = np.cumsum(liny[1:])*np.diff(jug.t)
#velz = np.cumsum(linz[1:])*np.diff(jug.t)

f, axarr = plt.subplots(4,sharex=True)
axarr[0].plot(jug.t,np.sqrt(np.array(velocityx)**2+np.array(velocityy)**2+np.array(velocityz)**2))
axarr[1].plot(jug.t,velocityx)
axarr[2].plot(jug.t,velocityy)
axarr[3].plot(jug.t,velocityz)

distancex = [0]
distancey = [0]
distancez = [0]
for i in range(1,len(new_point)):
    distancex.append(distancex[-1] + velocityx[i] * (jug.dt[i]))
    distancey.append(distancey[-1] + velocityy[i] * (jug.dt[i]))
    distancez.append(distancez[-1] + velocityz[i] * (jug.dt[i]))
    

f, axarr = plt.subplots(3,sharex=True)
axarr[0].plot(jug.t,distancex)
axarr[1].plot(jug.t,distancey)
axarr[2].plot(jug.t,distancez)

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


