### This is the main file that controls rest of the files. It initiates sets up some of the global variables

import argparse
import pam
import lib

#FUNCTION TO SEND OSC MESSAGES TO INSCORE
def osc_send_i(address,var):
    osc_msg = lib.OSC.OSCMessage()
    osc_msg.setAddress(address)
    for i in range(len(var)):
        osc_msg.append(var[i])
    osc_client.send(osc_msg)

#FUNCTION TO COLLECT LEAP MOTION DATA FOR NAVIGATION
def demoMenu():
    controller = lib.Leap.Controller()
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
            hand_span = lib.np.sqrt((thumb_pos.x-pinky_pos.x)**2+(thumb_pos.y-pinky_pos.y)**2+(thumb_pos.z-pinky_pos.z)**2)
            x_pos = x/150
            y_pos = (y-200)/200*(-1)
        print hand_span
        osc_send_i('/ITL/scene/menuBall',['x',x_pos])
        osc_send_i('/ITL/scene/menuBall',['y',y_pos])
        osc_send_i('/ITL/scene/menuBall',['scale',(hand_span-40)/100])
        #THIS IF STATEMENT INSIDE THE BUTTON
        if (-0.5 < x_pos < 0.5) and (-0.5 < y_pos < 0.5) and (flag == 0):
            osc_send_i('/ITL/scene/button',['effect','none'],)
            osc_send_i('/ITL/scene/menuBall',['alpha',127])
            osc_send_i('/ITL/scene/demoText',['alpha',255])
            #print 'in'
            flag = 1
        #THIS IF STATEMENT OUTSIDE THE BUTTON
        if ((x_pos < (-0.5)) or (x_pos > (0.5))) or ((y_pos < (-0.5)) or (y_pos > (0.5))) and (flag == 1):
            osc_send_i('/ITL/scene/button',['effect','blur',32])
            osc_send_i('/ITL/scene/menuBall',['alpha',255])
            osc_send_i('/ITL/scene/demoText',['alpha',0])
            flag = 0
        #THIS IF STATEMENT FOR CHOOSING A BUTTON
        if (flag == 1) and (hand_span< 60):
            break
        lib.time.sleep(0.05)

def retryMenu(retry):
    controller = lib.Leap.Controller()
    flag = 0
    x_pos = 0
    y_pos = 0
    hand_span = 65

    osc_send_i('/ITL/scene/textL',['set', 'txt', 'Listen'])
    osc_send_i('/ITL/scene/textL',['fontSize',64])
    osc_send_i('/ITL/scene/textL',['x',-0.6])
    osc_send_i('/ITL/scene/textL',['y',0])
    osc_send_i('/ITL/scene/textL',['alpha',0])

    osc_send_i('/ITL/scene/textQ',['set', 'txt', 'Next'])
    osc_send_i('/ITL/scene/textQ',['fontSize',64])
    osc_send_i('/ITL/scene/textQ',['x',0.6])
    osc_send_i('/ITL/scene/textQ',['y',0])
    osc_send_i('/ITL/scene/textQ',['alpha',0])

    osc_send_i('/ITL/scene/textR',['set','txt','Record'])
    osc_send_i('/ITL/scene/textR',['fontSize',64])
    osc_send_i('/ITL/scene/textR',['x',0])
    osc_send_i('/ITL/scene/textR',['y',0])
    osc_send_i('/ITL/scene/textR',['alpha',0])

    osc_send_i('/ITL/scene/menuBall1',['set','ellipse',0.5,0.5])
    osc_send_i('/ITL/scene/menuBall1',['color',255,255,0])

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
            hand_span = lib.np.sqrt((thumb_pos.x-pinky_pos.x)**2+(thumb_pos.y-pinky_pos.y)**2+(thumb_pos.z-pinky_pos.z)**2)
            x_pos = x/150
            y_pos = (y-200)/200*(-1)
        print x_pos, y_pos#hand_span
        osc_send_i('/ITL/scene/menuBall1',['x',x_pos])
        osc_send_i('/ITL/scene/menuBall1',['y',y_pos])
        osc_send_i('/ITL/scene/menuBall1',['scale',(hand_span-40)/100])

        #THIS IF STATEMENT INSIDE THE LISTEN BUTTON
        if (((-0.9) < x_pos < -0.3) and (-0.3 < y_pos < 0.3)) and (flag != 1):#(-0.5 < y_pos < 0.5)) and (flag == 0):
            print 'in L'
            osc_send_i('/ITL/scene/buttonL',['effect','none'],)
            osc_send_i('/ITL/scene/textL', ['alpha', 255])

            osc_send_i('/ITL/scene/buttonR',['effect','blur',32])
            osc_send_i('/ITL/scene/textR', ['alpha', 0])

            osc_send_i('/ITL/scene/buttonQ', ['effect', 'blur', 32])
            osc_send_i('/ITL/scene/textQ',['alpha',0])

            osc_send_i('/ITL/scene/menuBall1', ['alpha', 127])

            flag = 1

        #THIS IF STATEMENT INSIDE THE RECORD BUTTON
        if ((0.3 > x_pos > -0.3) and (-0.5 < y_pos < 0.5)) and (flag != 2):#(-0.5 < y_pos < 0.5)) and (flag == 0):
            print 'in R'
            osc_send_i('/ITL/scene/buttonR',['effect','none'],)
            osc_send_i('/ITL/scene/textR', ['alpha', 255])

            osc_send_i('/ITL/scene/buttonQ',['effect','blur',32])
            osc_send_i('/ITL/scene/textQ', ['alpha', 0])

            osc_send_i('/ITL/scene/buttonL', ['effect', 'blur', 32])
            osc_send_i('/ITL/scene/textL',['alpha',0])

            osc_send_i('/ITL/scene/menuBall1', ['alpha', 127])

            flag = 2

        #THIS IF STATEMENT INSIDE THE QUIT BUTTON
        if ((0.9 > x_pos > 0.3) and (-0.3 < y_pos < 0.3)) and (flag != 3):#(-0.5 < y_pos < 0.5)) and (flag == 0):
            print 'in Q'
            osc_send_i('/ITL/scene/buttonQ',['effect','none'],)
            osc_send_i('/ITL/scene/textQ', ['alpha', 255])

            osc_send_i('/ITL/scene/buttonR',['effect','blur',32])
            osc_send_i('/ITL/scene/textR',['alpha',0])

            osc_send_i('/ITL/scene/buttonL', ['effect', 'blur', 32])
            osc_send_i('/ITL/scene/textL', ['alpha', 0])

            osc_send_i('/ITL/scene/menuBall1', ['alpha', 127])

            flag = 3

        #THIS STATEMENT FOR OUTSIDE OF BUTTONS
        if ((y_pos < (-0.3)) or (y_pos > 0.3)) and (flag != 4):
            osc_send_i('/ITL/scene/buttonL', ['effect', 'blur', 32])
            osc_send_i('/ITL/scene/buttonR',['effect','blur',32])
            osc_send_i('/ITL/scene/buttonQ',['effect','blur',32])
            osc_send_i('/ITL/scene/textL', ['alpha', 0])
            osc_send_i('/ITL/scene/textR',['alpha',0])
            osc_send_i('/ITL/scene/textQ',['alpha',0])
            flag = 4

        #THIS IF STATEMENT FOR CHOOSING A BUTTON
        if (flag == 1) and (hand_span< 60):
            retry.value = 0
            break
        if (flag == 2) and (hand_span< 60):
            retry.value = 1
            break
        if (flag == 3) and (hand_span< 60):
            retry.value = 2
            break
        lib.time.sleep(0.05)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()                                              # declaration of arguments
    parser.add_argument('-u', '--user_id', help='Enter user ID')                    # user_id
    parser.add_argument('-f', '--midi_file', help='Enter MIDI file to be played back')      # MIDI file to open
    parser.add_argument('-d', '--midi_device', help='Enter MIDI device Nr.')  # MIDI file to open
    parser.add_argument('-m', '--method', help='Enter Rubato induction method: 0-Naive; 1-Compensation; 2-Phase estimation; 3-Demo')
    #parser.add_argument('-s', '--save_path', help='Enter path to save log files')   # path to save log files
    args = parser.parse_args()                                                      # variable to store list of user input variables
    user_id = int(args.user_id)                                                     # variable to store User ID
    midi_file = args.midi_file                                                           # variable to store the name of the MIDI file, all the MIDI files should be stored in midi_files folder of the project
    midi_device = int(args.midi_device)
    tempo_method = int(args.method)

    #save_path = args.save_path                                                     # variable to save log files

    curr_path = lib.os.path.dirname(lib.os.path.abspath(__file__))                          # paht where this file is running from
    #save_path = curr_path + '/users/' + str(user_id)                                # path to store data in csv file
    save_path = curr_path + '/users/' + str(user_id) + '/02_intention_studies/'
    midi_path = curr_path + '/midi_files/' + midi_file + '/' + midi_file# + '.mid'                     # paht of the midi file to play

    if not lib.os.path.exists(save_path):                                               # if the path does not exist create it
         lib.os.makedirs(save_path)

    print 'User ID: ', user_id                                                      # Printing stuff for debugging
    print 'MIDI File: ', midi_path
    print 'Save Path: ', save_path

    # STORE METHODS ARRAY
    ms = []
    for i in range(len(args.method)):
        ms.append(int(args.method[i]))

    # Open InScore appR
    lib.os.system('open /Applications/INScoreViewer-1.21.app')                          # Open up InScore
    lib.time.sleep(5)                                                                   # Give some time to load

    # Set up global OSC client
    osc_client = lib.OSC.OSCClient()                                                    # Create an OSC client
    osc_client.connect(('localhost', 7000))                                         # Connect to InScore

    #SETTING UP OSC CLIENT FOR INSCOR
    lib.time.sleep(3)
    osc_send_i('/ITL/scene',['load','/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/menu/main_menu.inscore'])
    lib.time.sleep(1)
    lib.os.system('open -a Terminal')

    retry = lib.multiprocessing.Value('i', 0)
    demo_p = lib.multiprocessing.Process(target=demoMenu,args=())
    demo_p.start()
    demo_p.join()                                               # Give some time to laod
    #osc_client.close()

    l = 0
    r = 0

    #SELECTING SOCRES AND MENU
    for i in range(len(ms)):
        count = 0
        while True:
            # OPENING INSCORE
            # os.system('open '+ curr_path+'/inscore_stuff/demo/demo.inscore')                # Load the score
            lib.os.system('open ' + midi_path + '.inscore')  # Load the score
            # os.system('open ' + curr_path + '/midi_files/' + midi_file + '/' + midi_file + '.inscore')  # Load the score
            lib.time.sleep(2)
            lib.os.system('open -a Terminal')
            osc_send_i('/ITL/scene/demoText1', ['set', 'txt', str(user_id) + ' I ' + str(i + 1) + ' L: ' + str(l) + ' R: ' + str(r)])
            osc_send_i('/ITL/scene/demoText1', ['fontSize', 15])
            osc_send_i('/ITL/scene/demoText1', ['y', -0.8])
            if retry.value == 0:
                osc_send_i('/ITL/scene/demoText2', ['set', 'txt', 'Listening'])
                osc_send_i('/ITL/scene/demoText2', ['fontSize', 20])
                osc_send_i('/ITL/scene/demoText2', ['y', -0.7])
                pam.play(midi_path, save_path+'/'+str(i)+'_'+str(ms[i])+'/'+str(count)+'_p', midi_device, 3, 1)             # Initialize MIDI playback
                l+=1

            elif retry.value == 1:
                osc_send_i('/ITL/scene/demoText2', ['set', 'txt', 'Listening'])
                osc_send_i('/ITL/scene/demoText2', ['fontSize', 20])
                osc_send_i('/ITL/scene/demoText2', ['y', -0.7])
                pam.play(midi_path, save_path + '/' + str(i) + '_' + str(ms[i]) + '/' + str(count) + '_p', midi_device, 3, 1)  # Initialize MIDI playback

                osc_send_i('/ITL/scene/demoText2', ['set', 'txt', 'Recording'])
                pam.play(midi_path, save_path+'/'+str(i)+'_'+str(ms[i])+'/'+str(count)+'_c', midi_device, ms[i], 1)
                r+=1

            p0 = lib.multiprocessing.Process(target=retryMenu, args=(retry,))
            osc_client = lib.OSC.OSCClient()
            osc_client.connect(('localhost', 7000))  # INSCORE
            osc_send_i('/ITL/scene',
                     ['load', '/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/menu/listen_record.inscore'])
            lib.os.system('open -a Terminal')
            p0 = lib.multiprocessing.Process(target=retryMenu, args=(retry,))
            p0.start()
            p0.join()
            #osc_send_i('/ITL/scene/*', 'del')
            if retry.value == 0 or retry.value == 1:
                count += 1
                #osc_client.close()
            if retry.value == 2:
                osc_client.close()
                break                                                        # Close OSC client once the playback has finished
            #count += 1
    lib.subprocess.call(['osascript', '-e', 'quit app "/Applications/INScoreViewer-1.21.app"'])
    lib.sys.exit(-1)
    print 'Program Terminated'