import matplotlib.pylab as plt
import numpy as np
import os
from scipy import stats

curr_path = os.path.dirname(os.path.abspath(__file__))                          # paht where this file is running from

naive_data = np.genfromtxt(curr_path+'/1/naive_tempo_data.csv',delimiter=',',names=True)
phase_data = np.genfromtxt(curr_path+'/1/naive_phase.csv',delimiter=',',names=True)

t_0 = naive_data['time'][0]

naive_data['time'] = naive_data['time'] - t_0
phase_data['time'] = phase_data['time'] - t_0

f, axarr = plt.subplots(2, sharex=True)#(1, sharex=True)

#axarr[0].plot(naive_data['time'],naive_data['palm_pos'],'.')

axarr[0].plot(naive_data['time'],naive_data['vel'],label='Raw Vel')
axarr[0].plot(naive_data['time'],naive_data['avg_vel'],label='Avg Vel')
axarr[0].plot(naive_data['time'],naive_data['avg_vel_schm'],label='Avg Vel Schm')
axarr[0].axhline(y=2, color='r',linestyle='--',lw=0.5)
axarr[0].axhline(y=-2, color='r',linestyle='--',lw=0.5)
axarr[0].axhline(color='b',linestyle='--',lw=0.5)
#axarr[1].axhline(y=-40, color='r','--')
axarr[0].legend()

avg_accel_t = naive_data['time'][1:]
avg_accel = np.diff(naive_data['avg_vel'])

axarr[0].plot(phase_data['time'],phase_data['phase'], 'x',label='Raw Vel')
axarr[1].plot(avg_accel_t, avg_accel)

zero_crossings = np.where(np.diff(np.sign(avg_accel)))[0]
axarr[1].plot(avg_accel_t[zero_crossings],avg_accel[zero_crossings],'gx')
axarr[0].plot(avg_accel_t[zero_crossings],naive_data['avg_vel'][zero_crossings],'gx')


