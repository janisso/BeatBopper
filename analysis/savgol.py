#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 13:06:42 2019

@author: mb
"""

import numpy as np
import matplotlib.pyplot as plt
'''
I need to caputre a low-frequency oscillation with only 1 time unit of data.
So far, I have not been able to find a way to make the fft resolution < 1.
'''
timeResolution = 10000.
mytimes = np.linspace(0, 1, timeResolution)
mypressures = np.sin(2 * np.pi * mytimes / 100)


fft = np.fft.fft(mypressures[:])
T = mytimes[1] - mytimes[0]
N = mypressures.size

# fft of original signal is limitted by the maximum time
f = np.linspace(0, 1 / T, N)
filteredidx = f > 0.001
freq = f[filteredidx][np.argmax(np.abs(fft[filteredidx][:N//2]))]
print('freq bin is is ', f[1] - f[0]) # 1.0
print('frequency is ', freq) # 1.0
print('(real frequency is 0.01)')

import scipy.signal as ss

plt.figure(1)
plt.subplot(121)
plt.plot(mytimes, mypressures)
plt.subplot(122)
plt.plot(mytimes, ss.detrend(mypressures))
plt.figure(2)

mycorrupted = mypressures + 0.00001 * np.random.normal(size=mypressures.shape)
plt.plot(mytimes, ss.detrend(mycorrupted))
plt.plot(mytimes, ss.detrend(mypressures))

width, order = 8999, 3
hw = (width+3) // 2
dsdt = ss.savgol_filter(mypressures, width, order, 1, 1/timeResolution)[hw:-hw]
d3sdt3 = ss.savgol_filter(mypressures, width, order, 3, 1/timeResolution)[hw:-hw]
est_freq_clean = np.nanmean(np.sqrt(-d3sdt3/dsdt) / (2 * np.pi))

dsdt = ss.savgol_filter(mycorrupted, width, order, 1, 1/timeResolution)[hw:-hw]
d3sdt3 = ss.savgol_filter(mycorrupted, width, order, 3, 1/timeResolution)[hw:-hw]
est_freq_noisy = np.nanmean(np.sqrt(-d3sdt3/dsdt) / (2 * np.pi))

#print(f"Estimated freq clean signal: {est_freq_clean:10.6f}")
#print(f"Estimated freq noisy signal: {est_freq_noisy:10.6f}")