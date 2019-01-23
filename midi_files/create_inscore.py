#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 17:49:04 2019

@author: mb
"""
import os
import glob

path = "/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper_study/MazurkaBL/"
save_path = "/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/midi_files/"
not_these = ['M07-1','M63-3','M59-3','M24-2']
for file in glob.glob(path+"beat_time/*.csv"):
    name = os.path.basename(file)[:5]
    if name not in not_these:
        f=open(save_path+name+'/'+name+'.inscore','w+')
        f.write('/ITL/scene/* del;\n')
        f.write('/ITL get musicxml-version;\n')
        f.write('/ITL/scene/score set musicxmlf "'+name+'.xml";\n')
        f.write('/ITL/scene/score columns 1;\n')
        f.write('/ITL/scene/score scale 0.25;\n')
        f.write('/ITL/scene/cursor set rect 0.02 0.8;\n')
        f.write('/ITL/scene/cursor color 0 0 255;\n')
        f.write('/ITL/scene/sync cursor score;\n')
        f.close()