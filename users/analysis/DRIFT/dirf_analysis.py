#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 16:19:01 2019

@author: mb
"""

import numpy as np
import matplotlib.pyplot as plt
import copy
import mido
from sklearn.metrics import mean_squared_error
from math import sqrt
import pandas as pd


def get_zero_cross(sig):
    #idx = []
    #for i in range(1,len(sig)):
    #    if ((sig[i]*sig[i-1]) < 0) and (sig[i-1] < 0):
    #        idx
    idx = np.where(np.diff(np.sign(sig)))[0]
    pos_idx = np.where(sig[idx]<0)[0]
    return idx[pos_idx]


def get_midi(midifile):
    mid = mido.MidiFile(midifile)                          # save parsed MIDI file using mido library
    s_times = []  # np.zeros((times[0],2))                      # create an empty array to storenote events in the MIDI file
    #port = lib.mido.open_output(lib.mido.get_output_names()[midi_device_nr.value]) # open port to send MIDI messages
    all_time = 0                                                # aggregate time for all the messages
    msg_count = 0                                               # this is to count MIDI messages with note information
    all_messages = []                                           # create an ampty array to only store note information and their position in the score
    for msg in mid:                                             # for every message in the midi file
        all_time += msg.time                                    # the file stores midi time based on previous onset, we h
        if hasattr(msg, 'note'):                                # checks that the MIDI message is Note
            #if hasattr(msg, 'note_on'):
            #if msg.type == 'note_on':
            #    print 'note_on'
            #all_time += msg.time                                #
            all_messages.append(msg)                            # adds note message from MIDI file to our playback 
            s_times.append([msg_count, all_time, msg.type,msg.note])               # array to store note score time
            msg_count += 1
    s_times = np.array(s_times)                             # convert array to numpy.array
    yo = copy.deepcopy(s_times)                             # deepcopy the array so the original doesn't get 
    return all_messages, yo

def get_beat_idx(yo):
    idx_no = np.where(yo[:,2]=='note_on')[0]
    mod_seq_no = yo[idx_no]
    val, idx = np.unique(mod_seq_no[:,1],return_index = True)
    mod_seq_no_uni =mod_seq_no [idx]
    mod_seq_no_round = np.round(mod_seq_no_uni[:,1].astype(float)*2)/2
    diff = mod_seq_no_round-mod_seq_no_uni[:,1].astype(float)
    exclude = np.where(abs(diff)>0.05)[0]
    idx = np.ma.array(idx,mask=False)
    idx.mask[exclude] = True
    idx = idx.compressed()
    #idx_no[idx]
    return idx_no[idx]



sample_data = np.genfromtxt("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/DRIFT/get_samples.csv",delimiter=',',names=True)
start_t = sample_data['time'][0]
sample_data['time']=sample_data['time']-start_t

midi_msg, midi_yo = get_midi("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/DRIFT/midi_drift.mid")
midi_idx = get_beat_idx(midi_yo)
midi_idx = np.sort(midi_idx)
#midi_idx = midi_idx[:-1]

idx = get_zero_cross(sample_data['palm_vel'])
idx = np.delete(idx, 95)
idx = idx[:120]

each_beat = np.genfromtxt("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/DRIFT/0_1/get_samples.csv",delimiter=',',names=True)
each_beat_beats = np.genfromtxt("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/DRIFT/0_1/naive_phase.csv",delimiter=',',names=True)
each_beat_midi = np.genfromtxt("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/DRIFT/0_1/play_midi.csv",delimiter=',',names=True)[midi_idx]

start_t = each_beat['time'][0]
each_beat['time']=each_beat['time']-start_t
each_beat_beats['time']=each_beat_beats['time'] - start_t
each_beat_midi['time'] = each_beat_midi['time'] - start_t



borch = np.genfromtxt("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/DRIFT/0_0/get_samples.csv",delimiter=',',names=True)
borch_beats = np.genfromtxt("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/DRIFT/0_0/naive_phase.csv",delimiter=',',names=True)
borch_midi = np.genfromtxt("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/DRIFT/0_0/play_midi.csv",delimiter=',',names=True)[midi_idx]

start_t = borch['time'][0]
borch['time']=borch['time']-start_t
borch_beats['time']=borch_beats['time'] - start_t
borch_midi['time'] = borch_midi['time'] - start_t



phase = np.genfromtxt("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/DRIFT/0_2/get_samples.csv",delimiter=',',names=True)
phase_beats = np.genfromtxt("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/DRIFT/0_2/phase_phase.csv",delimiter=',',names=True)
phase_midi = np.genfromtxt("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/DRIFT/0_2/play_midi.csv",delimiter=',',names=True)[midi_idx]


start_t = phase['time'][0]
phase['time']=phase['time']-start_t
phase_beats['time']=phase_beats['time']-start_t
phase_beats = phase_beats[np.where(phase_beats['phase']==0)[0]]
phase_midi['time'] = phase_midi['time'] - start_t

#plt.figure()
#plt.plot(sample_data['time'],sample_data['palm_vel'],label='Orig')
#plt.plot(each_beat['time'],each_beat['palm_vel'],label='Each Beat')
#plt.plot(borch['time'],borch['palm_vel'],label='Borch')
#plt.plot(phase['time'],phase['palm_vel'],label='Phase')
#plt.legend()

####SIGNALS TO SAVE AND SEND TO R
t = sample_data['time'][:idx[-1]]
d = sample_data['palm_vel'][:idx[-1]]

df = np.column_stack((t,d))
df_r = pd.DataFrame(df,columns=['time','vel'])
df_r.to_csv('hand_vel.csv', sep=',',index=False)

beat_idx = pd.DataFrame(idx,columns=['idx'])
beat_idx.to_csv('idx.csv', sep = ',',index=False)


f, axarr = plt.subplots(4,sharex=True)
axarr[0].plot(sample_data['time'],sample_data['palm_vel'],label='Orig')
for num in range(len(idx)):
    x = sample_data['time'][idx[num]]
    axarr[0].text(x,0,str(num))
    axarr[0].axvline(x=x)

axarr[1].plot(each_beat['time'],each_beat['palm_vel'],label='Each Beat')
for xc in each_beat_beats['time']:
    axarr[1].axvline(x=xc)
for xc in each_beat_midi['time']:
    axarr[1].axvline(x=xc,color='r')

axarr[2].plot(borch['time'],borch['palm_vel'],label='Borch')
for xc in borch_beats['time']:
    axarr[2].axvline(x=xc)
for xc in borch_midi['time']:
    axarr[2].axvline(x=xc,color='r')

axarr[3].plot(phase['time'],phase['palm_vel'],label='Phase')
for xc in phase_beats['time']:
    axarr[3].axvline(x=xc)
for xc in phase_midi['time']:
    axarr[3].axvline(x=xc,color='r')


f,axarr = plt.subplots(4,sharex=True)
axarr[0].plot(60/np.diff(sample_data['time'][idx]))
axarr[1].plot(60/np.diff(each_beat_midi['time']))
axarr[2].plot(60/np.diff(borch_midi['time']))
axarr[3].plot(60/np.diff(phase_midi['time']))

diff_eb = sample_data['time'][idx] - (0.9986403921196217*each_beat_midi['time'])
diff_b = sample_data['time'][idx] - (0.9972039345621371*borch_midi['time'])
#diff_b = diff_b - diff_b[0] 
diff_p = sample_data['time'][idx] - (1.0108968212391725*phase_midi['time'])

rmse_eb = np.sqrt((diff_eb**2).mean())
rmse_b = np.sqrt((diff_b**2).mean())
rmse_p = np.sqrt((diff_p**2).mean())

arr_r = np.concatenate((np.array([0]),sample_data['time'][idx]))
arr_c = np.zeros(len(arr_r))
arr_c[1:] = arr_r[1:]-diff_eb
arr_n = np.zeros(len(arr_r))
arr_n[1:] = arr_r[1:]-diff_b
arr_p = np.zeros(len(arr_r))
arr_p[1:] = arr_r[1:]-diff_p

#hhh = np.column_stack((np.array(range(1,121)),sample_data['time'][idx],diff_eb.T,diff_b.T,diff_p.T))
hhh = np.column_stack((np.array(range(1,122)),arr_r,arr_n,arr_c,arr_p))

plt.figure()
plt.plot(diff_eb)
plt.plot(diff_b)
plt.plot(diff_p)


np.diff(sample_data['time'][idx]).std()
np.diff(each_beat_midi['time']).std()
np.diff(borch_midi['time']).std()
np.diff(phase_midi['time']).std()

sample_data['time'][idx[97]]
each_beat['time']

drift = pd.DataFrame(hhh,columns=['beat','time','naive','each_beat','phase'])
drift.to_csv('drift_t.csv', sep=',',index=False)
