import matplotlib.pylab as plt
import numpy as np
import os
from scipy import stats

curr_path = os.path.dirname(os.path.abspath(__file__))                          # paht where this file is running from

data = np.genfromtxt(curr_path+'/1/phase_advance.csv',delimiter=',')[1:]

time = data[:,0]
phase = data[:,1]

d_time = np.diff(time)

m_med = np.median(d_time)
m_mean = np.mean(d_time)

plt.figure()
plt.plot(d_time)

print m_med
print m_mean