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
import scipy.stats as stats
#sns.set()
def set_style():
    # This sets reasonable defaults for font size for
    # a figure that will go in a paper
    sns.set_context("paper")
    
    # Set the font to be serif, rather than sans
    sns.set(font='serif')
    
    # Make the background white, and specify the
    # specific font family
    sns.set_style("white", {
        "font.family": "serif",
        "font.serif": ["Times", "Palatino", "serif"]
    })

    
def plot_ting(s0_sums,s1_sums,s2_sums,title):
    op = 0.2
    
    #####PLOTTING BAR CHARTS
    # data to plot
    n_groups = 5
     
    # create plot
    
    # width as measured in inkscape
    width = 6.9
    height = width / 1.618
    
    #fig, ax = plt.subplots()
    
    fig, ax = plt.subplots()
    #fig.subplots_adjust(left=.15, bottom=.16, right=.99, top=.97)
    index = np.arange(n_groups)
    bar_width = 0.25
    opacity = 1
     
    rects1 = plt.bar(index, s0_sums, bar_width,
    #alpha=opacity,
    color=likert_colors_op,
    edgecolor='black',
    linewidth = 0.3,
    label='Naive')
    for rect in rects1:
        rect.set_edgecolor('white')
     
    rects2 = plt.bar(index + 0.025 + bar_width, s1_sums, bar_width,
    #alpha=opacity,
    color=likert_colors_op,
    linewidth = 0.3,
    #hatch='\\\\',
    #edgecolor='black',
    label='Comp')
    for rect in rects2:
        rect.set_hatch('\\\\\\')
        rect.set_edgecolor('white')
    
    rects3 = plt.bar(index + .05 + bar_width*2, s2_sums, bar_width,
    #alpha=opacity,
    color=likert_colors_op,
    linewidth = 0.3,
    #hatch='oo',
    #edgecolor='black',
    label='Phase')
    for rect in rects3:
        rect.set_hatch('oo')
        rect.set_edgecolor('white')
    
    plt.xlabel('Likert-Units')
    plt.ylabel('Scores')
    plt.title(title)
    plt.xticks(index + bar_width, ('Strongly\n Disagree', 'Disagree', 'Neutral', 'Agree','Strongly\n Agree'))
    #plt.grid(False)
    plt.legend(loc=2)
    
    golden_mean = (np.sqrt(5)-1.0)/2.0
    fig.set_size_inches(6.9, 6.9*golden_mean)
    
    plt.tight_layout()
    
    plt.rc('font', family='serif', serif='Times')
    #plt.rc('text', usetex=True)
    plt.rc('xtick', labelsize=8)
    plt.rc('ytick', labelsize=8)
    plt.rc('axes', labelsize=8)
    
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

#set_style()

curr_path = os.path.dirname(os.path.abspath(__file__)) 
loc_info = pd.read_csv('/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/pinfo.csv')

sus0 = pd.read_csv(curr_path+'/sus0/sus0.csv')
sus0['4. It took me a long time to understand how the system works']=6-sus0['4. It took me a long time to understand how the system works']
sus1 = pd.read_csv(curr_path+'/sus1/sus1.csv')
sus1['4. It took me a long time to understand how the system works']=6-sus1['4. It took me a long time to understand how the system works']
sus2 = pd.read_csv(curr_path+'/sus2/sus2.csv')
sus2['4. It took me a long time to understand how the system works']=6-sus2['4. It took me a long time to understand how the system works']

cols = ['ID','1','2','3','4','5','6','7','8','9','10']

sus0.columns = cols
sus1.columns = cols
sus2.columns = cols


s0 = pd.DataFrame(columns=sus0.columns)
s1 = pd.DataFrame(columns=sus0.columns)
s2 = pd.DataFrame(columns=sus0.columns)

tries = ['p1','p2','p3']




#THIS ONE HERE IS WRONG, ALL THE STUFF WE HAVE BEEN DOING IS ON THE ORDER OF THE SYSTEM RATHER THAN ON THE ACTUAL TING...
for j in range(len(tries)):
    for counter, value in enumerate(loc_info[tries[j]]):
        if value == 0:
            s0.loc[len(s0)] = sus0.iloc[counter]
        if value == 1:
            s1.loc[len(s1)] = sus1.iloc[counter]
        if value == 2:
            s2.loc[len(s2)] = sus2.iloc[counter]
            
            
for counter, value in enumerate(loc_info[tries[0]]):
    print counter, value
    if value == 0:
        s0.loc[len(s0)] = sus0.iloc[counter]
    if value == 1:
        s1.loc[len(s1)] = sus1.iloc[counter]
    if value == 2:
        s2.loc[len(s2)] = sus2.iloc[counter]
            
            
            
            
            
            
            
s0.columns = cols
s1.columns = cols
s2.columns = cols

s0 = s0.sort_values(by=['ID'])
s1 = s1.sort_values(by=['ID'])
s2 = s2.sort_values(by=['ID'])


syses = [s0,s1,s2]

#(0.698, 0.133, 0.133,0.2)
op = 1
likert_colors = ['firebrick','lightcoral','gainsboro','cornflowerblue', 'darkblue']
likert_colors_op = [(36/250., 44/250., 162/255.,op),
                    (177/255., 206/255., 232/255.,op),
                    (230/255., 230/255., 230/255.,op),
                    (173/255., 237/255., 205/255.,op),
                    (37/255., 162/255., 36/255.,op)]

likert_colors = likert_colors_op
hatches = [None,'\\\\','oo']

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
    
    l1 = l1 / 28 * 100
    l2 = l2 / 28 * 100
    l3 = l3 / 28 * 100
    l4 = l4 / 28 * 100
    l5 = l5 / 28 * 100
    mid = 0#(l1+l2+l3)-(l3/2)
    
    #plt.figure()
    p1 = plt.barh(ind*4+k,l1,left=-mid,color=likert_colors[0],hatch=hatches[0])
    p2 = plt.barh(ind*4+k,l2,left=l1-mid,color=likert_colors[1],hatch=hatches[0])
    p3 = plt.barh(ind*4+k,l3,left=l1+l2-mid,color=likert_colors[2],hatch=hatches[0])
    p4 = plt.barh(ind*4+k,l4,left=l1+l2+l3-mid,color=likert_colors[3],hatch=hatches[0])
    p5 = plt.barh(ind*4+k,l5,left=l1+l2+l3+l4-mid,color=likert_colors[4],hatch=hatches[0])
    plt.suptitle('System '+str(k+1))
    
#s2.to_csv(curr_path+'/02_phase/sus2.csv', sep=',')

s0['s']=0
s1['s']=1
s2['s']=2

frames = pd.concat([s0, s1, s2])
frames = frames.drop(['ID'], axis=1)
#frames.to_csv(curr_path+'/sus_data.csv', sep=',')

'''s0 = s0.drop(['ID','s'],axis=1)
s1 = s1.drop(['ID','s'],axis=1)
s2 = s2.drop(['ID','s'],axis=1)
s2 = s2.astype(int)

s0_sums = (sum(s0.where(s0==1).count(1)),sum(s0.where(s0==2).count(1)),sum(s0.where(s0==3).count(1)),sum(s0.where(s0==4).count(1)),sum(s0.where(s0==5).count(1)))
s1_sums = (sum(s1.where(s1==1).count(1)),sum(s1.where(s1==2).count(1)),sum(s1.where(s1==3).count(1)),sum(s1.where(s1==4).count(1)),sum(s1.where(s1==5).count(1)))
s2_sums = (sum(s2.where(s2==1).count(1)),sum(s2.where(s2==2).count(1)),sum(s2.where(s2==3).count(1)),sum(s2.where(s2==4).count(1)),sum(s2.where(s2==5).count(1)))

for i in range(1,11):
    arr0 = s0[cols[i]]
    arr1 = s1[cols[i]]
    arr2 = s2[cols[i]]
    
    s0_sums = (arr0.where(arr0==1).count(),arr0.where(arr0==2).count(),arr0.where(arr0==3).count(),arr0.where(arr0==4).count(),arr0.where(arr0==5).count())
    s1_sums = (arr1.where(arr1==1).count(),arr1.where(arr1==2).count(),arr1.where(arr1==3).count(),arr1.where(arr1==4).count(),arr1.where(arr1==5).count())
    s2_sums = (arr2.where(arr2==1).count(),arr2.where(arr2==2).count(),arr2.where(arr2==3).count(),arr2.where(arr2==4).count(),arr2.where(arr2==5).count())
    plot_ting(s0_sums,s1_sums,s2_sums,sus0.columns[i])
 
#plt.tight_layout()

#for i in range(1,11):
#    print s0[str(i)].where(s0[str(i)]==1).count()
    
#kruskal = np.zeros(2)

kruskall = pd.DataFrame(columns=['system','question','rater','likert'])

for j in range(1,11):
    df = pd.DataFrame(columns=['system','question','rater','likert'])
    df['system'] = frames['s']
    df['question'] = str(cols[j])
    df['rater'] = frames['ID']
    df['likert'] = frames[cols[j]]
    #kruskall.append(frames[['s',cols[j],'ID']])
    #kruskal= np.vstack([kruskal,frames[[cols[j],'s']]])
    kruskall = kruskall.append(df)

#kruskal = kruskal[1:]

#kruskall['answers']=kruskal[:,0]
#kruskall['sys']=kruskal[:,1]
#kruskall.astype(int).to_csv(curr_path+'/kruskal.csv', sep=',',index=False)


#stats.kruskal(s0,s1,s2)
#####code from https://stackoverflow.com/questions/23142358/create-a-diverging-stacked-bar-chart-in-matplotlib'''