#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 11:51:22 2019

@author: mb
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns
import scipy.stats as stats

from ggplot import *

def return_ordered(spq,titles,loc_info):
    spq_order = pd.DataFrame(np.nan, index=range(len(spq)), columns=spq.columns)
    #spq_order['id'] = spq['id']
    for i in range(len(spq)):
        order = loc_info.loc[i][titles]
        #print order
        df = spq.iloc[i]
        for j in range(0,3):
            #first = df == j
            mask = (df == j)
            if sum(mask):
                idx = np.where(mask==True)[0].tolist()
                spq_order.iloc[i,idx]=order[j]
    spq_order['id']=spq['id']
    print spq_order
    
    #spq_order = spq_order.astype(int)
    return spq_order

#curr_path = os.path.dirname(os.path.abspath(__file__)) 
loc_info = pd.read_csv('/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/pinfo.csv')

spq_01 = pd.read_csv('01_spq.csv')
spq_02 = pd.read_csv('02_spq.csv')
spq_03 = pd.read_csv('03_spq.csv')

spq_01.iloc[:,1:] = spq_01.iloc[:,1:]-1
spq_02.iloc[:,1:] = spq_02.iloc[:,1:]-1
spq_03.iloc[:,1:] = spq_03.iloc[:,1:]-1

tits1 = ['i1_1','i1_2','i1_3']
tits2 = ['i2_1','i2_2','i2_3']
tits3 = ['i3_1','i3_2','i3_3']

spq_01_order = return_ordered(spq_01,tits1,loc_info).fillna(3).astype(int)
spq_02_order = return_ordered(spq_02,tits2,loc_info).fillna(3).astype(int)
spq_03_order = return_ordered(spq_03,tits3,loc_info).fillna(3).astype(int)

frames = [spq_01_order,spq_02_order,spq_03_order]
framess = [spq_01,spq_02,spq_03]
#frames = [spq_02_order,spq_03_order]
#frames = spq_01_order
all_ting = pd.concat(frames)
#all_ting = spq_01_order
            
    #for j in range(len(order)):
    #    condition = df == order[j]
    #    #print condition
    #print df
    #print 'First: ',order[0],'Second: ',order[1],'Third: ',order[2]
    #print spq_01.loc[i]
qs = ['q1','q2','q3','q4','q5','q6']

for i in qs:
    counts = all_ting[i].value_counts()
    print counts

df = all_ting[qs[:-1]]
dfl = df.values.tolist()#pd.value_counts(df.values.tolist())
flat_list = [item for sublist in l for item in sublist]
counts = pd.value_counts(flat_list)

pd.value_counts([i for i in spq_01_order['q1']])




chisq_system = pd.DataFrame(columns=['rater','excerpt','question','pref'])
chisq_order = pd.DataFrame(columns=['rater','excerpt','questions','order'])

'''for j in range(1,11):
    df = pd.DataFrame(columns=['system','question','rater','pref'])
    df['system'] = frames['s']
    df['question'] = str(cols[j])
    df['rater'] = frames['ID']
    df['likert'] = frames[cols[j]]
    #kruskall.append(frames[['s',cols[j],'ID']])
    #kruskal= np.vstack([kruskal,frames[[cols[j],'s']]])
    kruskall = kruskall.append(df)'''
    
#cols = ['ID','1','2','3','4','5','6']
count = 0
for i in range(len(frames)):
    #df = pd.DataFrame(columns=['rater','system','question','pref'])
    system = frames[i]
    for j in range(0,6):
        question = qs[j]
        for k in range(np.shape(frames[0])[0]):
            rater = system['id'][k]
            #df['rater']=rater
            #df['system']=i
            #df['questions']=question
            #df['pref']=system[question][k]
            
            chisq_system.loc[count] = [rater,i,question,system[question][k]]#pd.DataFrame([rater,i,question,system[question][k]],columns=['rater','system','question','pref'])
            chisq_order.loc[count] = [rater,i,question,framess[i][question][k]]#pd.DataFrame([rater,i,question,system[question][k]],columns=['rater','system','question','pref'])
            count += 1
            #chisq_system = chisq_system.append(df)

#kruskal = kruskal[1:]

#kruskall['answers']=kruskal[:,0]
#kruskall['sys']=kruskal[:,1]

chisq_system.to_csv('chisq_system.csv', sep=',',index=False)
chisq_order.to_csv('chisq_order.csv', sep=',',index=False)
