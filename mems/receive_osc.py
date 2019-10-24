#!/usr/bin/env python3
from OSC import OSCServer
import sys
from time import sleep
import time
from playsound import playsound
import sys
import multiprocessing
import types
import argparse

#tempo = raw_input('Enter Tempo ')

savePath = '/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/mems/'
f = open(savePath+'juggle_data.csv','w+')
f.write('time, a_x, a_y, a_z, g_x, g_y, g_z \n')

#def write_lines(args):
#	f.write("%f, %s, %f, %f, %f\n"%(time.time(),args[0],args[1],args[2],args[3]))

# this method of reporting timeouts only works by convention
# that before calling handle_request() field .timed_out is 
# set to False
def handle_timeout(self):
    self.timed_out = True

def acc_callback(path, tags, args, source):
    f.write("%f, %f, %f, %f, %f, %f, %f\n"%(time.time(),args[0],args[1],args[2],args[3],args[4],args[5]))
    print args

# user script that's called by the game engine every frame
def each_frame(server):  
    # clear timed_out flag
    server.timed_out = False
    # handle all pending requests then return
    while not server.timed_out:
        server.handle_request()


def frame(savePath):
    print 'getting osc'
    # funny python's way to add a method to an instance of a class
    server = OSCServer( ("192.168.1.209", 12000) )
    server.timeout = 0
    run = True
    server.handle_timeout = types.MethodType(handle_timeout, server)
    server.addMsgHandler( "/acc", acc_callback )
    while True:
        each_frame(server)
        #print 'hello'
        sleep(0.001)
    return


if __name__ == "__main__":
	#print 'play sound'
	q = multiprocessing.Queue()
	savePath = '/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/mems/'#'/Users/mb/Desktop/Janis.so/06_qmul/CHI_2019/audio/tempo_midi/python_audio/'
	frame_ting = multiprocessing.Process(target=frame,args=(savePath,))
	#play_ting = multiprocessing.Process(target=play_sound,args=(savePath,q))
	#play_the_sound = multiprocessing.Process(target=play_the_sound,args=(q,))
	frame_ting.start()
	#play_ting.start()
	#play_the_sound.start()
	frame_ting.join()
	#play_ting.join()
	#play_the_sound.join()
	print 'starting'