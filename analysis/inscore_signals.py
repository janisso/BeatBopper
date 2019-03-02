#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 15:22:58 2019

@author: mb
"""

import matplotlib.pyplot as plt
import numpy as np

times = np.genfromtxt('/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/midi_files/M68-2_e1/M68-2orig_beats.csv')
iois = np.diff(times)
tempo = 60/iois
min_tempo = min(tempo)
max_tempo = max(tempo)
norm_tempo = (tempo - min_tempo)/(max(tempo)-min(tempo))

[print i * 0.5 for i  in norm_tempo]
