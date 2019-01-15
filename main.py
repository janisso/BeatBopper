### This is the main file that controls rest of the files. It initiates sets up some of the global variables

import argparse
import os
import pam
import OSC
import time
import lib

#FUNCTION TO SEND OSC MESSAGES TO INSCORE
def osc_send_i(address,var):
    osc_msg = OSC.OSCMessage()
    osc_msg.setAddress(address)
    for i in range(len(var)):
        osc_msg.append(var[i])
    osc_client.send(osc_msg)


#FUNCTION TO COLLECT LEAP MOTION DATA FOR NAVIGATION
def demoMenu():
    controller = Leap.Controller()
    flag = 0
    x_pos = 0
    y_pos = 0
    hand_span = 65
    while True:
        frame = controller.frame()
        for hand in frame.hands:
            #GETTING PALM VELOCITY
            x = hand.palm_position.x
            y = hand.palm_position.y
            for finger in hand.fingers:
                if finger.type == 0:
                    thumb_pos = finger.tip_position
                if finger.type == 2:
                    pinky_pos = finger.tip_position
            hand_span = np.sqrt((thumb_pos.x-pinky_pos.x)**2+(thumb_pos.y-pinky_pos.y)**2+(thumb_pos.z-pinky_pos.z)**2)
            x_pos = x/150
            y_pos = (y-200)/200*(-1)
        print hand_span
        oscSendI('/ITL/scene/menuBall',['x',x_pos])
        oscSendI('/ITL/scene/menuBall',['y',y_pos])
        oscSendI('/ITL/scene/menuBall',['scale',(hand_span-40)/100])
        #THIS IF STATEMENT INSIDE THE BUTTON
        if (-0.5 < x_pos < 0.5) and (-0.5 < y_pos < 0.5) and (flag == 0):
            oscSendI('/ITL/scene/button',['effect','none'],)
            oscSendI('/ITL/scene/menuBall',['alpha',127])
            oscSendI('/ITL/scene/demoText',['alpha',255])
            #print 'in'
            flag = 1
        #THIS IF STATEMENT OUTSIDE THE BUTTON
        if ((x_pos < (-0.5)) or (x_pos > (0.5))) or ((y_pos < (-0.5)) or (y_pos > (0.5))) and (flag == 1):
            oscSendI('/ITL/scene/button',['effect','blur',32])
            oscSendI('/ITL/scene/menuBall',['alpha',255])
            oscSendI('/ITL/scene/demoText',['alpha',0])
            flag = 0
        #THIS IF STATEMENT FOR CHOOSING A BUTTON
        if (flag == 1) and (hand_span< 60):
            break
        sleep(0.05)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()                                              # declaration of arguments
    parser.add_argument('-u', '--user_id', help='Enter user ID')                    # user_id
    parser.add_argument('-f', '--midi_file', help='Enter MIDI file to be played back')      # MIDI file to open
    parser.add_argument('-d', '--midi_device', help='Enter MIDI device Nr.')  # MIDI file to open
    parser.add_argument('-m', '--method', help='Enter Rubato induction method: 0-Naive; 1-Compensation; 2-Phase estimation')
    #parser.add_argument('-s', '--save_path', help='Enter path to save log files')   # path to save log files
    args = parser.parse_args()                                                      # variable to store list of user input variables
    user_id = int(args.user_id)                                                     # variable to store User ID
    midi_file = args.midi_file                                                           # variable to store the name of the MIDI file, all the MIDI files should be stored in midi_files folder of the project
    midi_device = int(args.midi_device)
    tempo_method = int(args.method)
    #save_path = args.save_path                                                     # variable to save log files

    curr_path = os.path.dirname(os.path.abspath(__file__))                          # paht where this file is running from
    save_path = curr_path + '/users/' + str(user_id)                                # path to store data in csv file
    midi_path = curr_path + '/midi_files/' + midi_file + '/' + midi_file + '.mid'                     # paht of the midi file to play

    if not os.path.exists(save_path):                                               # if the path does not exist create it
         os.makedirs(save_path)

    print 'User ID: ', user_id                                                      # Printing stuff for debugging
    print 'MIDI File: ', midi_path
    print 'Save Path: ', save_path

    # Open InScore appR
    os.system('open /Applications/INScoreViewer-1.21.app')                          # Open up InScore
    time.sleep(5)                                                                   # Give some time to load

    # Set up global OSC client
    osc_client = OSC.OSCClient()                                                    # Create an OSC client
    osc_client.connect(('localhost', 7000))                                         # Connect to InScore

    #OPENING INSCORE
    #os.system('open '+ curr_path+'/inscore_stuff/demo/demo.inscore')                # Load the score
    os.system('open ' + curr_path + '/midi_files/' + midi_file + '/' + midi_file + '.inscore')  # Load the score
    time.sleep(2)
    os.system('open -a Terminal')                                                   # Give some time to laod

    #SELECTING SOCRES AND MENUS


    pam.play(midi_path, save_path, midi_device, tempo_method)                                     # Initialize MIDI playback
    osc_client.close()                                                              # Close OSC client once the playback has finished

    print 'Program Terminated'
