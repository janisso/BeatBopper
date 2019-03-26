#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 20:29:23 2019

@author: mb
"""

import matplotlib.pyplot as plt
import os
import numpy as np
import pandas as pd
import mido
import copy
from scipy import stats

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

def get_zero_cross(sig):
    #idx = []
    #for i in range(1,len(sig)):
    #    if ((sig[i]*sig[i-1]) < 0) and (sig[i-1] < 0):
    #        idx
    idx = np.where(np.diff(np.sign(sig)))[0]
    pos_idx = np.where(sig[idx]<0)[0]
    return idx[pos_idx]
            

e1_msg, e1_yo = get_midi("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/midi_files/demo/demo.mid")
beats = get_beat_idx(e1_yo)
e1_yo[:,1]=e1_yo[:,1].astype(float)*2
beats = np.sort(np.append(beats,len(e1_yo)-1))
path = '/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/'
e1_yo[beats]

times = np.zeros(81)
count = 0

for u in range(1,6):
    # Set the directory you want to start from\
    rootDir = path+str(u)+'/01_pref_studies/'
    #for k in range(1,2):
    #print rootDir
    for dirName, subdirList, fileList in os.walk(rootDir):
        #print('Found directory: %s' % dirName)
        #if len(subdirList)==3:
        #print dirName
        for j in subdirList:
            if len(j)==3:
                BBdir = dirName+j
                f, axarr = plt.subplots(3)
                #print BBdir
                for BBdirName, BBsubdirList, BBfileList in os.walk(BBdir):
                    #print BBsubdirList
                    if (BBdirName[-1] == str(0)):
                        method = 'Borch'
                    if (BBdirName[-1] == str(1)):
                        method = 'Beat'
                    if (BBdirName[-1] == str(2)):
                        method = 'Phase'
                    print BBdirName[-1]
                    print method
                    #for l in BBfileList:
                    #if l == 'get_samples.csv':
                    #######GET MIDI
                    l = 'play_midi.csv'
                    #print method
                    #f, axarr = plt.subplots(2, sharex = True)
                    #plt.figure()
                    fileName = BBdirName+'/'+l
                    p_seq = np.genfromtxt(fileName,delimiter=',',names=True)
                    p_ioi = np.diff(p_seq['time'][beats])
                    start_t = p_seq['time'][0]
                    #axarr[1].plot(p_seq['time'][2:],p_ioi[1:])
                    p_seq['time'] = p_seq['time']-start_t
                    #plt.plot(p_seq['beats'][beats][2:],p_ioi[1:])
                    p_time = p_seq['time'][-1]-p_seq['time'][0]
                    times[count]=p_time
                    #print 'yeeeeee'
                    ######GET HAND MOVEMENT
                    fn = BBdirName+'/get_samples.csv'
                    get_samples = pd.DataFrame(np.genfromtxt(fn,delimiter=',',names=True))[['time','palm_vel']]
                    get_samples['time']=get_samples['time']-start_t
                    axarr[0].plot(get_samples['time'],get_samples['palm_vel'])
                    ######GET SMOOTHED HAND MOVEMENT
                    if (method == 'Borch') or (method == 'Beat'):
                        fn = BBdirName+'/naive_tempo_data.csv'
                    else:
                        fn = BBdirName+'/phase_tempo_data.csv'
                    avg_vel = pd.DataFrame(np.genfromtxt(fn,delimiter=',',names=True))[['time','avg_vel']]
                    avg_vel['time']=avg_vel['time']-start_t
                    axarr[0].plot(avg_vel['time'],avg_vel['avg_vel'])
                    idx = get_zero_cross(avg_vel['avg_vel'])
                    axarr[0].plot(avg_vel['time'][idx],avg_vel['avg_vel'][idx],'o')
                    axarr[0].set_title(str(u) + ' '+ method)
                    h_ioi = np.diff(avg_vel['time'][idx])
                    axarr[1].hist(h_ioi,bins=50,normed=True)
                    ioi_stats = stats.describe(h_ioi)
                    axarr[1].set_title('mu '+str(np.around(ioi_stats.mean,decimals=2)))
                    ######
                    #####GET THE BEATS FROM THE METHOD
                    
                                        
                    
                    count += 1
                    
                            
                            
                            
#                            
#                        if l == 'play_midi.csv':
#                            print method
#                            #f, axarr = plt.subplots(2, sharex = True)
#                            #plt.figure()
#                            fileName = BBdirName+'/'+l
#                            p_seq = np.genfromtxt(fileName,delimiter=',',names=True)
#                            p_ioi = np.diff(p_seq['time'][beats])
#                            start_t = p_seq['time'][0]
#                            #axarr[1].plot(p_seq['time'][2:],p_ioi[1:])
#                            p_seq['time'] = p_seq['time']-start_t
#                            #plt.plot(p_seq['beats'][beats][2:],p_ioi[1:])
#                            p_time = p_seq['time'][-1]-p_seq['time'][0]
#                            times[count]=p_time
#                            #print 'yeeeeee'
#                            count += 1
#                            
#
#lens = times/60.


