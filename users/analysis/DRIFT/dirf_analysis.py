#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 16:19:01 2019

@author: mb
"""

import numpy as np
import matplotlib.pyplot as plt

def get_zero_cross(sig):
    #idx = []
    #for i in range(1,len(sig)):
    #    if ((sig[i]*sig[i-1]) < 0) and (sig[i-1] < 0):
    #        idx
    idx = np.where(np.diff(np.sign(sig)))[0]
    pos_idx = np.where(sig[idx]<0)[0]
    return idx[pos_idx]


sample_data = np.genfromtxt("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/DRIFT/get_samples.csv",delimiter=',',names=True)

idx = get_zero_cross(sample_data['palm_vel'])

plt.plot(sample_data['time'],sample_data['palm_vel'])
plt.plot(sample_data['time'][idx],sample_data['palm_vel'][idx],'o')

