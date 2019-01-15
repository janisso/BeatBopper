import mido
import time
import multiprocessing
import numpy as np
from scipy.optimize import least_squares
import copy
import OSC
import os
import sys
from scipy import signal
from collections import deque
import Leap
'''from scipy.io import wavfile
import sounddevice as sd

fs, beat_up = wavfile.read(os.path.dirname(os.path.abspath(__file__))+'/up.wav')
fs, beat_do = wavfile.read(os.path.dirname(os.path.abspath(__file__))+'/do.wav')'''

#SET UP WINDOW LENGTH AND HOP SIZE FOR REGRESSION
window_length = 100
#SET UP FILTER
f = 0.001
coeffs = signal.firwin(window_length, f)

'''def play_sound(fs,array):
    sd.play(array,fs)'''

#CIRCULAR BUFFER CLASS FOR STORING VALUES FOR FILTERING
class CircularBuffer(deque):
    def __init__(self, size=0):
        super(CircularBuffer, self).__init__(maxlen=size)
    @property
    def average(self):
        return sum(self)/len(self)

# SCHMIT TRIGGER TO DISCOUNT DEVIATIONS AROUND ZERO FOR VELOCITY AND ACCELERATION
def schmit(val, thresh):
    if 0 < val <= thresh:
        new_sig = thresh
    if thresh*(-1) <= val <= 0:
        new_sig = thresh*(-1)
    else:
        new_sig = val
    return new_sig

def get_samples(palm_pos, hand_vel, hand_span, stop_all, save_path):
    f = open(save_path + '/get_samples.csv', 'w+')
    f.write('time,palm_pos,palm_vel,span\n')
    controller = Leap.Controller()
    while True:
        frame = controller.frame()
        for hand in frame.hands:
            # GETTING PALM VELOCITY
            palm_pos.value = hand.palm_position.y
            #print palm_pos.value
            hand_vel.value = hand.palm_velocity.y
            # print hand.fingers[0].position
            for finger in hand.fingers:
                if finger.type == 0:
                    thumb_pos = finger.tip_position
                if finger.type == 4:
                    pinky_pos = finger.tip_position
            hand_span.value = np.sqrt(
                (thumb_pos.x - pinky_pos.x) ** 2 + (thumb_pos.y - pinky_pos.y) ** 2 + (thumb_pos.z - pinky_pos.z) ** 2)
        f.write("%f, %f, %f, %f\n" % (time.time(), palm_pos.value, hand_vel.value, hand_span.value))
        time.sleep(0.005)
        if stop_all.value == 1:
            f.close
            break

def is_still(val,thresh):
    #is_still = False
    if (val < -thresh) or (val > thresh):
        is_still = False
    else:#elif (val <= thresh) and (val >= -thresh):
        is_still = True
    return is_still