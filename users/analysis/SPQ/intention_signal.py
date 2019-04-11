#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 22:41:41 2019

@author: mb
"""

import numpy as np
import copy
import mido
import matplotlib.pyplot as plt
import os
import pandas as pd
#from ggplot import *
from plotnine import *

theme_set(theme_classic())


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

def rmse(predictions, targets):
    return np.sqrt(((predictions - targets) ** 2).mean())

def get_lims(d1,d2,d3,d4):
    arr = [d1,d2,d3,d4]
    x_min = 0
    x_max = 0
    for i in arr:
        if i[0]<x_min:
            x_min=i[0]
        if i[-1]>x_max:
            x_max=i[-1]
    return x_min,x_max

e1_t = np.genfromtxt("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/midi_files/M33-1_e1/M33-1_e1orig_beats.csv")
e1_msg, e1_yo = get_midi("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/midi_files/M33-1_e1/M33-1_e1.mid")

e2_t = np.genfromtxt("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/midi_files/M07-1_e1/M07-1_e1orig_beats.csv")
e2_msg, e2_yo = get_midi("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/midi_files/M07-1_e1/M07-1_e1.mid")
e2_mag_2, e2_yo_2 = get_midi("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/midi_files/M07-1_e1/M07-1_e1_11.mid")

e3_t = np.genfromtxt("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/midi_files/M63-3_e1/M63-3_e1orig_beats.csv")
e3_msg, e3_yo = get_midi("/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/midi_files/M63-3_e1/M63-3_e1.mid")

indices = [get_beat_idx(e1_yo),get_beat_idx(e2_yo),get_beat_idx(e3_yo)]
i_e2 = get_beat_idx(e2_yo_2)

path = '/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/'
#user = str(1)
##user_data_path = path+user+'/'+
#
#mid_mod = np.genfromtxt('/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/10/02_intention_studies/1/0_0/1_p/play_midi.csv',delimiter=',',names=True)
#mid_mod['time']=mid_mod['time']-mid_mod['time'][0]
#
#mid_perf = np.genfromtxt('/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/10/02_intention_studies/1/2_2/1_c/play_midi.csv',delimiter=',',names=True)
##mid_perf['time'][0]=mid_perf['time'][1]#-mid_perf['time'][0]
#mid_perf['time']=mid_perf['time']-mid_perf['time'][0]
#
#plt.plot(mid_mod['time'])
#plt.plot(mid_perf['time'])

######## DIRECTORY TRAVERSS
# Import the os module, for the os.walk function

big_ting = np.zeros((27,10))

df = pd.DataFrame(index = np.arange(16),
                  data=np.zeros((16,5)),
                  columns = ['beat','m_ioi','e_ioi','b_ioi','p_ioi'])
df['beat']=range(1,17)

labels = ['b_ioi','e_ioi','p_ioi']

for u in range(24,25):
    big_ting[u-1,0]=u
    # Set the directory you want to start from\
    for e in range(1):#EXCERPT
        rootDir = path+str(u)+'/02_intention_studies/'
        #for k in range(1,2):
        newDir = rootDir+str(e)# = path+str(i)+'/02_intention_studies'
        #print rootDir
        for dirName, subdirList, fileList in os.walk(newDir):
            #print('Found directory: %s' % dirName)
            #if len(subdirList)==3:
            for j in subdirList:
                if len(j)==3:
                    for m in range(3):
                        if j[2]==str(m): #METHOD
                            BBdir = dirName+'/'+j
                            for BBdirName, BBsubdirList, BBfileList in os.walk(BBdir):
                                #print BBdirName
                                if len(BBsubdirList):
                                    t = 0
                                    rms_min = 1000000000000000
                                    f,axarr = plt.subplots(4,sharex=True)
                                    #print BBsubdirList
                                    mod_seqDir = BBdirName+'/'+BBsubdirList[0]
                                    fileName = mod_seqDir+'/'+'play_midi.csv'
                                    mod_seq = np.genfromtxt(fileName,delimiter=',',names=True)
                                    mod_seq = mod_seq
                                    time_s = mod_seq['time'][0]
                                    #axarr[0].plot(np.diff(e2_t[:-1]))
                                    if (e==1) and (u<16):
                                        t_m= mod_seq['time'][i_e2]-time_s
                                        m_ioi = np.diff(t_m)
                                    else:
                                        t_m = mod_seq['time'][indices[e]]-time_s
                                        m_ioi = np.diff(t_m)
                                    df['m_ioi']=m_ioi
                                    axarr[0].plot(t_m[1:],m_ioi)
                                    for ii in t_m:
                                        axarr[0].axvline(x=ii)
                                    df_m = pd.DataFrame(data=np.column_stack((t_m[1:],m_ioi)),
                                                        columns = ['time','ioi'])
#                                    p1 = ggplot(aes(x='time',y='ioi'),data=df_m)+geom_line()+\
#                                        geom_vline(xintercept=t_m,color="gray")+\
#                                        labs(x='',y='IOI (s)')
#                                    ggsave(p1,'test_gg.pdf', scale = 1, width = 8.4, height = 1.43, units = "in", dpi = 75)
                                    #ggsave(p1,'test_gg.pdf', scale = 1, width = 8.4, height = 2.87, units = "in", dpi = 75)
                                    #p1.make()
                                    #geom_vline(data = idx, aes(xintercept = as.numeric(time)),color="gray",size=0.5)
                                    #mod_seq['time']=mod_seq['time']-mod_seq['time'][0]
                                    #plt.plot(mod_seq['time'])
                                #print BBdirName,BBsubdirList
                                for l in BBfileList:
                                    if BBdirName[-1]!='p':
                                        #print BBdirName
                                        if l == 'play_midi.csv':
                                            fileName = BBdirName+'/'+l
                                            mid_seq = np.genfromtxt(fileName,delimiter=',',names=True)
                                            time_s = mid_seq['time'][0]
                                            #GET HAND MOVEMENT DEETS
                                            if m==2:
                                                hd = np.genfromtxt(BBdirName+'/phase_tempo_data.csv',delimiter=',',names=True)
                                                hd['time'] = hd['time']-time_s
                                                p_d = np.genfromtxt(BBdirName+'/phase_phase.csv',delimiter=',',names=True)
                                                p_d = p_d[np.where(p_d['phase']==0)[0]]
                                            else:
                                                hd = np.genfromtxt(BBdirName+'/naive_tempo_data.csv',delimiter=',',names=True)
                                                hd['time'] = hd['time']-time_s
                                                p_d = np.genfromtxt(BBdirName+'/naive_phase.csv',delimiter=',',names=True)
                                            df_h = pd.DataFrame(data=np.column_stack((hd['time'],hd['vel'],hd['avg_vel'])),
                                                                columns=['time','vel','avg_vel'])
                                            axarr[1].plot(hd['time'],hd['vel'])
                                            axarr[1].plot(hd['time'],hd['avg_vel'])             
                                            ###PHASE INFORMATION FROM ZERO CROSSES
                                            p_d['time']=p_d['time']-time_s
#                                            ggplot(aes(x='time',y='vel'),data=df_h)+geom_line()+\
#                                                geom_vline(xintercept=p_d['time'],color="gray",size=0.5)+\
#                                                geom_line(aes(x='time',y='avg_vel'),data=df_h)
                                            h_ioi = np.diff(p_d['time'])
                                            axarr[2].plot(p_d['time'][1:],h_ioi)
                                            for ii in p_d['time'][p_d['time']>0]:
                                                axarr[1].axvline(x=ii)
                                                axarr[2].axvline(x=ii)

                                                
                                            df_h_ioi = pd.DataFrame(data=np.column_stack((p_d['time'][1:],h_ioi)),
                                                        columns = ['time','ioi'])
                                            
                                            #axarr[2].plot(pd['time'][1:],h_ioi)
                                            #GET IOI FOR THE MIDI PERF
                                            if (e==1) and (u<16):
                                                t_p= mid_seq['time'][i_e2]-time_s
                                                p_ioi = np.diff(t_p)
                                            else:
                                                t_p = mid_seq['time'][indices[e]]-time_s
                                                p_ioi = np.diff(t_p)
                                            df[labels[m]]=p_ioi
                                            
                                            df_m_ioi = pd.DataFrame(data=np.column_stack((t_p[1:],p_ioi)),
                                                        columns = ['time','ioi'])
                                            
                                            fig = plt.gcf()
                                            ax = plt.gca()
                                            axarr[3].plot(t_p[1:],p_ioi)
                                            for ii in t_p:
                                                axarr[3].axvline(x=ii)
                                            plt.suptitle(str(u) + ' ' + str(e) + ' ' + str(m))
                                            rms_e = rmse(p_ioi,m_ioi)
                                            #if rms_e < rms_min:
                                            #    rms_min = rms_e
                                            #index = e*3+1+m
                                            #big_ting[u-1,index]=rms_min
                                            #mid_seq
                                            print 'User: ',u,' Excerpt: ', e, ' Method: ', m, ' Try: ',t,' RMS: ', rms_e
                                            t += 1
                                            
                                            x_min, x_max = get_lims(t_m,np.array(df_h['time']),np.array(p_d['time']),t_p)
                                            
                                            p1 = ggplot(aes(x='time',y='ioi'),data=df_m)+geom_line()+\
                                                geom_vline(xintercept=t_m,color="gray")+\
                                                labs(x='',y='IOI (s)')+\
                                                theme(axis_ticks_major_x=element_blank(),
                                                      axis_text_x=element_blank())+\
                                                      xlim(x_min-0.5, x_max+0.5)
                                            #p1 = p1 + theme(axis.title.y = element_text(margin = margin(t = 0, r = 10, b = 0, l = 0)))
                                            #ggsave(p1,'01_test_gg.pdf', scale = 1, width = 8.4, height = 1.43, units = "in", dpi = 75)
                                            
                                            
                                            p2 = ggplot(aes(x='time',y='vel'),data=df_h)+geom_line()+\
                                                geom_line(aes(x='time',y='avg_vel'),data=df_h,color='blue')+\
                                                geom_vline(xintercept=p_d['time'],color="gray")+\
                                                labs(x='',y='Velocity (mm/s)')+\
                                                theme(axis_ticks_major_x=element_blank(),
                                                      axis_text_x=element_blank())+\
                                                      xlim(x_min-0.5, x_max+0.5)
                                            
                                            p3 = ggplot(aes(x='time',y='ioi'),data=df_h_ioi)+geom_line()+\
                                                geom_vline(xintercept=p_d['time'][p_d['time']>0],color="gray")+\
                                                labs(x='',y='IOI (s)')+\
                                                theme(axis_ticks_major_x=element_blank(),
                                                      axis_text_x=element_blank())+\
                                                      xlim(x_min-0.5, x_max+0.5)
                                            
                                            p4 = ggplot(aes(x='time',y='ioi'),data=df_m_ioi)+geom_line()+\
                                                labs(x='Time (s)',y='IOI (s)')+\
                                                geom_vline(xintercept=t_p,color="gray")+\
                                                      xlim(x_min-0.5, x_max+0.5)





#ggarrange(p1,p2,p3,p4,labels=c('a','b','c'),ncol=1,nrow=4)
#fig7, ax7 = plt.subplots()
#ax7.set_title('Multiple Samples with Different sizes')
#ax7.boxplot(big_ting[:,1:])

#p = np.vstack((np.arange(1,len(m_ioi)+1),m_ioi,p_ioi)).T
#beats = np.arange(1,len(m_ioi)+1)

#df = pd.DataFrame(index = np.arange(len(m_ioi)),
#                  data = p,
#                  columns = ['beat','m_ioi','p_ioi'])

#df.to_csv('/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/SPQ/rmse_plot/ioi_sig.csv', sep=',',index=False)

#ggplot(aes(x='beat'), data=df) +\
#    geom_line(aes(y='m_ioi'), color='blue',linetype = "dashed") +\
#    geom_point(aes(y='m_ioi'), color='blue') +\
#    geom_line(aes(y='p_ioi'), color='red') +\
#    geom_point(aes(y='p_ioi'), color='red')
    
    
    
#ggplot(df, aes(x=beat,
#                    y=m_ioi) + geom_line() +\
#                  geom_point()+\
#  labs(title="Estimated Marginal Means of RMSE",x="Excerpt", y = "Estimated Marginal Means")+\
#  scale_colour_manual(values= c("#003f5c", "#7a5195", "#ef5675"))+\
#  theme_minimal()


#from rpy2.robjects import pandas2ri
#pandas2ri.activate()
#from rpy2.robjects.packages import importr
#base = importr('base')

#to_R = pd.DataFrame(big_ting,columns=['id','e1_n','e1_c','e1_p','e2_n','e2_c','e2_p','e3_n','e3_c','e3_p'])
#to_R.to_csv('intention_rmse.csv', sep=',',index=False)
#base.summary(to_R)
#
#from rpy2 import robjects as ro
#ro.globalenv['df'] = to_R
#indexes = idx_no[idx]
#
#yo = e1_yo
#yo[:,1]=yo[:,1].astype(float)