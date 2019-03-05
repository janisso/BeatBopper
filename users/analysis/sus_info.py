#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 17:54:51 2019

@author: mb
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns
sns.set()

curr_path = os.path.dirname(os.path.abspath(__file__)) 
loc_info = pd.read_csv('pinfo.csv')


sus0 = pd.read_csv(curr_path+'/sus0/sus0.csv')
sus0['4. It took me a long time to understand how the system works']=6-sus0['4. It took me a long time to understand how the system works']
sus1 = pd.read_csv(curr_path+'/sus1/sus1.csv')
sus1['4. It took me a long time to understand how the system works']=6-sus1['4. It took me a long time to understand how the system works']
sus2 = pd.read_csv(curr_path+'/sus2/sus2.csv')
sus2['4. It took me a long time to understand how the system works']=6-sus2['4. It took me a long time to understand how the system works']

cols = ['ID','1','2','3','4','5','6','7','8','9','10']
s0 = pd.DataFrame(columns=sus0.columns)
s1 = pd.DataFrame(columns=sus0.columns)
s2 = pd.DataFrame(columns=sus0.columns)

tries = ['p1','p2','p3']

for j in range(len(tries)):
    for counter, value in enumerate(loc_info[tries[j]]):
        if value == 0:
            s0.loc[len(s0)] = sus0.iloc[counter]
        if value == 1:
            s1.loc[len(s1)] = sus1.iloc[counter]
        if value == 2:
            s2.loc[len(s2)] = sus2.iloc[counter]
s0.columns = cols
s1.columns = cols
s2.columns = cols

syses = [s0,s1,s2]

for k in range(3):

    l1 = np.zeros(10)
    l2 = np.zeros(10)
    l3 = np.zeros(10)
    l4 = np.zeros(10)
    l5 = np.zeros(10)
    
    data_points = [l1,l2,l3,l4,l5]
    ind = np.arange(10)
    
    for i in range(1,11):
        for j in range(1,6):
            if j in syses[k][str(i)].value_counts():
                #print s0[str(i)].value_counts()[j]
                data_points[j-1][i-1]=syses[k][str(i)].value_counts()[j]
                
    plt.figure()
    p1 = plt.bar(ind,l1)
    p2 = plt.bar(ind,l2,bottom=l1)
    p3 = plt.bar(ind,l3,bottom=l1+l2)
    p4 = plt.bar(ind,l4,bottom=l1+l2+l3)
    p5 = plt.bar(ind,l5,bottom=l1+l2+l3+l4)

#2 in s0['1'].value_counts().unique()
#s1['1'].value_counts()
#s2['1'].value_counts()
