#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 00:54:25 2019

@author: mb
"""
import numpy as np
import os
from scipy import signal
import matplotlib.pyplot as plt

from collections import deque

class CircularBuffer(deque):
    def __init__(self, size=0):
        super(CircularBuffer, self).__init__(maxlen=size)
    @property
    def average(self):
        return sum(self)/len(self)
    
window_length = 100
#SET UP FILTER
f = 0.001
coeffs = signal.firwin(window_length, f)
circ_buff = CircularBuffer(size=window_length)

for i in range(window_length):
    circ_buff.append(0)
    
#from scipy.signal import hilbert, chirp

'''duration = 10.0
fs = 400.0
samples = int(fs*duration)
t = np.arange(samples) / fs

signal = chirp(t, 1.0, t[-1], 10.0)
signal *= (1.0 + 0.5 * np.sin(2.0*np.pi*3.0*t))

analytic_signal = hilbert(signal)
amplitude_envelope = np.abs(analytic_signal)

plt.plot(t, signal, label='signal')
plt.plot(t, amplitude_envelope, label='envelope')
plt.show()'''




curr_path = os.path.dirname(os.path.abspath(__file__))                          # paht where this file is running from

naive_data = np.genfromtxt('/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/999/03_pref_studies/0_0/naive_tempo_data.csv',delimiter=',',names=True)
phase_data = np.genfromtxt('/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/999/03_pref_studies/0_0/naive_phase.csv',delimiter=',',names=True)
midi_data = np.genfromtxt('/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/999/03_pref_studies/0_0/play_midi.csv',delimiter=',',names=True)

t = naive_data['time']
midi_time = midi_data['time'] - t[0]
t = t-t[0]
vel = naive_data['vel']
avg_rect = np.zeros(len(vel))



#plt.plot(t,rect)

indices = []
#prev = rect[0]
for i in range(0,len(t)):
    circ_buff.append(abs(vel[i]))
    avg_rect[i] = sum(circ_buff*coeffs)
    '''if rect[i]<prev:
        indices.append(i)
    prev = rect[i]'''

#plt.plot(t[indices],rect[indices],'x')
f, axarr = plt.subplots(2,sharex=True)
axarr[0].plot(t,vel)
axarr[0].plot(t,abs(vel))
axarr[0].plot(t,avg_rect)
axarr[1].plot(midi_time,midi_data['midi_vel'])