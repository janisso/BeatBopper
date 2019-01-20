import matplotlib.pylab as plt
import numpy as np
import os
from scipy import stats

curr_path = os.path.dirname(os.path.abspath(__file__))                          # paht where this file is running from

naive_data = np.genfromtxt(curr_path+'/999/naive_tempo_data.csv',delimiter=',',names=True)
phase_data = np.genfromtxt(curr_path+'/999/naive_phase.csv',delimiter=',',names=True)

def compMeth(seconds,catchUp):
    seconds = seconds - seconds[0]
    dt1 = seconds[1]-seconds[0]
    vu1 = 1/dt1
    vm1 = vu1
    rem1 = 0
    advanced = 0
    a = 0
    
    #catchUp = 0.25
    
    phassess = np.zeros((len(seconds)*2,3))
    
    for i in range(1,len(seconds)):
        #advanced = (vm1*(dt1*(rem1+0.5))+vu1*(dt1*0.5))
        dt = seconds[i]-seconds[i-1]
        #advanced = vm1*(dt*catchUp)+vu1*(dt*(1-catchUp))
        advanced = vm1*(dt*(rem1+catchUp))+vu1*(dt*(1-catchUp))
        a += advanced
        vu = 1/dt
        #em = 1 - vu1*dt#advanced
        rem = 1 - dt*vu1
        vm = (rem+catchUp)/(dt*catchUp)
        #print tempo1[i],a,advanced,rem
        phassess[2*i] = [seconds[i],vm, 1-catchUp-rem]
        phassess[2*i+1] = [seconds[i]+dt*catchUp,vu,rem+catchUp]
        #phassess.append([seconds[i],vm])
        #phassess.append([seconds[i]+dt*0.25,vu])
        vm1 = vm
        rem1 = rem
        dt1 = dt
        vu1 = vu
    phassess = phassess[1:-1]
        
    return phassess[:,0],np.cumsum(phassess[:,2])#*np.pi*2

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

comp_phase, comp_time = compMeth(phase_data['time'],0.25)

plt.figure()
plt.plot(phase_data['time']-phase_data['time'][0],np.arange(len(phase_data)),label='Phase Data')
plt.plot(comp_phase,comp_time,label='Compensation')
plt.legend()
