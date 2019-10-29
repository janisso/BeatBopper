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
def demoMenu(retry):
    controller = lib.Leap.Controller()
    flag = 0
    x_pos = 0
    y_pos = 0.5
    hand_span = 65

    rec_size = 0.66
    half_rec_size = rec_size / 2
    middles = [-0.66, 0, 0.66]
    names = ['piece', 'section', 'quit']

    for i, name in enumerate(names):
        osc_send_i('/ITL/scene/text_'+name, ['set', 'txt', name])
        osc_send_i('/ITL/scene/text_'+name, ['fontSize', 64])
        osc_send_i('/ITL/scene/text_'+name, ['x', middles[i]])
        osc_send_i('/ITL/scene/text_'+name, ['y', 0])
        osc_send_i('/ITL/scene/text_'+name, ['alpha', 0])

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
        #print x_pos, y_pos#hand_span
        osc_send_i('/ITL/scene/menuBall1',['x',x_pos])
        osc_send_i('/ITL/scene/menuBall1',['y',y_pos])
        osc_send_i('/ITL/scene/menuBall1',['scale',(hand_span-40)/100])

        for i, mid in enumerate(middles):
            alpha_these = lib.copy.deepcopy(names)
            alpha_these.pop(i)
            if (((mid - half_rec_size/2) < x_pos < (mid + half_rec_size/2)) and (-half_rec_size < y_pos < half_rec_size)) and (flag != (i+1)):
                osc_send_i('/ITL/scene/'+names[i],['effect','none'],)
                osc_send_i('/ITL/scene/menuBall1', ['alpha', 127], )
                osc_send_i('/ITL/scene/text_'+names[i], ['alpha', 255])
                for name in alpha_these:
                    osc_send_i('/ITL/scene/'+name, ['effect', 'blur', 32])
                    osc_send_i('/ITL/scene/text_'+name, ['alpha', 0])
                flag = i+1
                print(flag)

        #THIS STATEMENT FOR OUTSIDE OF BUTTONS
        if ((y_pos < (-0.2)) or (y_pos > 0.2)) and (flag != 3):
            for name in names:
                osc_send_i('/ITL/scene/'+name, ['effect', 'blur', 32])
                osc_send_i('/ITL/scene/text_',['alpha',0])
            flag = 4
        print(flag)

        #THIS IF STATEMENT FOR CHOOSING A BUTTON
        if (flag == 1) and (hand_span < 60):
            retry.value = 0
            break
        if (flag == 2) and (hand_span < 60):
            retry.value = 1
            break
        if (flag == 3) and (hand_span < 60):
            retry.value = 2
            break
        lib.time.sleep(0.05)

def sectionMenu(section_select):
    controller = lib.Leap.Controller()
    flag = 0
    x_pos = 0
    y_pos = 0.5
    hand_span = 65

    rec_size = 0.4
    half_rec_size = rec_size / 2
    middles = [-0.8, -0.4, 0, 0.4, 0.8]
    names = ['section_0', 'section_1', 'section_2', 'section_3', 'section_4']

    for i, name in enumerate(names):
        osc_send_i('/ITL/scene/text_'+name, ['set', 'txt', name])
        osc_send_i('/ITL/scene/text_'+name, ['fontSize', 64])
        osc_send_i('/ITL/scene/text_'+name, ['x', middles[i]])
        osc_send_i('/ITL/scene/text_'+name, ['y', 0])
        osc_send_i('/ITL/scene/text_'+name, ['alpha', 0])

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
        #print x_pos, y_pos#hand_span
        osc_send_i('/ITL/scene/menuBall1',['x',x_pos])
        osc_send_i('/ITL/scene/menuBall1',['y',y_pos])
        osc_send_i('/ITL/scene/menuBall1',['scale',(hand_span-40)/100])

        for i, mid in enumerate(middles):
            alpha_these = lib.copy.deepcopy(names)
            alpha_these.pop(i)
            if (((mid - half_rec_size/2) < x_pos < (mid + half_rec_size/2)) and (-half_rec_size < y_pos < half_rec_size)) and (flag != (i+1)):
                osc_send_i('/ITL/scene/'+names[i],['effect','none'],)
                osc_send_i('/ITL/scene/menuBall1', ['alpha', 127], )
                osc_send_i('/ITL/scene/text_'+names[i], ['alpha', 255])
                for name in alpha_these:
                    osc_send_i('/ITL/scene/'+name, ['effect', 'blur', 32])
                    osc_send_i('/ITL/scene/text_'+name, ['alpha', 0])
                flag = i+1
                print(flag)

        #THIS STATEMENT FOR OUTSIDE OF BUTTONS
        if ((y_pos < (-0.2)) or (y_pos > 0.2)) and (flag != 3):
            for name in names:
                osc_send_i('/ITL/scene/'+name, ['effect', 'blur', 32])
                osc_send_i('/ITL/scene/text_',['alpha',0])
            flag = 6
            print(flag)

        #THIS IF STATEMENT FOR CHOOSING A BUTTON
        if (flag == 1) and (hand_span < 60):
            section_select.value = 0
            break
        if (flag == 2) and (hand_span < 60):
            section_select.value = 1
            break
        if (flag == 3) and (hand_span < 60):
            section_select.value = 2
            break
        if (flag == 4) and (hand_span < 60):
            section_select.value = 3
            break
        if (flag == 5) and (hand_span < 60):
            section_select.value = 4
            break
        lib.time.sleep(0.05)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()                                              # declaration of arguments
    parser.add_argument('-u', '--user_id', help='Enter user ID')                    # user_id
    parser.add_argument('-f', '--midi_file', help='Enter MIDI file to be played back')      # MIDI file to open
    parser.add_argument('-d', '--midi_device', help='Enter MIDI device Nr.')  # MIDI file to open
    parser.add_argument('-m', '--method', help='Enter Rubato induction method: 0-Naive; 1-Compensation; 2-Phase estimation; 3-Demo')
    parser.add_argument('-s', '--seq', help='Enumerate the system')
    #parser.add_argument('-s', '--save_path', help='Enter path to save log files')   # path to save log files
    args = parser.parse_args()                                                      # variable to store list of user input variables
    user_id = int(args.user_id)                                                     # variable to store User ID
    midi_file = args.midi_file                                                           # variable to store the name of the MIDI file, all the MIDI files should be stored in midi_files folder of the project
    midi_device = int(args.midi_device)
    seq = int(args.seq)
    #tempo_method = int(args.method)
    #save_path = args.save_path                                                     # variable to save log files

    curr_path = lib.os.path.dirname(lib.os.path.abspath(__file__))                          # paht where this file is running from
    save_path = curr_path + '/music_practice/users/'+ str(user_id) + '/express_studies/'                               # path to store data in csv file
    midi_path = curr_path + '/xml_files/M07-1/'

    if not lib.os.path.exists(save_path):                                               # if the path does not exist create it
         lib.os.makedirs(save_path)

    #import os
    #dirname = os.path.dirname(__file__)

    print 'User ID: ', user_id                                                      # Printing stuff for debugging
    print 'MIDI File: ', midi_path
    print 'Save Path: ', save_path

    #STORE METHODS ARRAY
    ms = args.method
    #for i in range(len(args.method)):
    #    ms.append(int(args.method[i]))

    # Open InScore appR
    lib.os.system('open /Applications/INScoreViewer-1.21.app')                          # Open up InScore
    lib.time.sleep(5)                                                                   # Give some time to load

    # Connect to InScore

    #SETTING UP OSC CLIENT FOR INSCOR
    #lib.time.sleep(3)

    #MAIN MENU
    #for i in range(len(ms)):
    while True:
        # Set up global OSC client
        osc_client = lib.OSC.OSCClient()  # Create an OSC client
        osc_client.connect(('localhost', 7000))
        osc_send_i('/ITL/scene', ['load', curr_path+'/menu/practice_menu.inscore'])
        lib.time.sleep(1)
        lib.os.system('open -a Terminal')
        retry = lib.multiprocessing.Value('i', 0)
        demo_p = lib.multiprocessing.Process(target=demoMenu, args=(retry,))
        demo_p.start()
        demo_p.join()  # Give some time to laod
        osc_client.close()
        if retry.value == 0:
            print('Piece')
            lib.os.system('open ' + midi_path + 'M07-1.inscore')
            lib.time.sleep(1)
            osc_client = lib.OSC.OSCClient()  # Create an OSC client
            osc_client.connect(('localhost', 7000))
            osc_send_i('/ITL/scene', ['load', midi_path + 'M07-1.inscore'])
            #lib.os.system('open -a Terminal')
            osc_client.close()
            lib.os.system('open -a Terminal')
            pam.play(midi_path+'M07-1', save_path + '/' + str(0) + '_' + str(ms), midi_device, 2, 0)
            #lib.time.sleep(2)
        if retry.value == 1:
            print('Section')
            osc_client = lib.OSC.OSCClient()  # Create an OSC client
            osc_client.connect(('localhost', 7000))
            osc_send_i('/ITL/scene', ['load', curr_path + '/menu/song_select.inscore'])
            lib.time.sleep(1)
            lib.os.system('open -a Terminal')
            section_select = lib.multiprocessing.Value('i', 0)
            select_p = lib.multiprocessing.Process(target=sectionMenu, args=(section_select,))
            select_p.start()
            select_p.join()  # Give some time to laod
            osc_client.close()
            print('You selected section_'+str(section_select.value))
        if retry.value == 2:
            print('Quit')
            break

    '''lib.os.system('open ' + midi_path + '.inscore')  # Load the score
    # os.system('open ' + curr_path + '/midi_files/' + midi_file + '/' + midi_file + '.inscore')  # Load the score
    lib.time.sleep(2)
    lib.os.system('open -a Terminal')
    osc_client = lib.OSC.OSCClient()
    osc_client.connect(('localhost', 7000))  # INSCORE
    osc_send_i('/ITL/scene/demoText1', ['set', 'txt', str(user_id)+' P '+str(i+1)])
    osc_send_i('/ITL/scene/demoText1', ['fontSize', 20])
    osc_send_i('/ITL/scene/demoText1', ['y', -0.8])'''
    #pam.play(midi_path, save_path+'/'+str(i)+'_'+str(ms[i]), midi_device, ms[i], 0)


    # osc_send_i('/ITL/scene/*', ['del'])
    # osc_send_i('/ITL/scene', ['load', curr_path+'/menu/load_next.inscore'])
    #
    # osc_send_i('/ITL/scene/sysid', ['set', 'txt', 'SUS '+ str(seq)])
    # osc_send_i('/ITL/scene/sysid', ['fontSize', 18])
    # osc_send_i('/ITL/scene/sysid', ['y', -0.2])
    # osc_send_i('/ITL/scene/sysid', ['alpha', 0.1])
    #
    #
    # osc_send_i('/ITL/scene/userid', ['set', 'txt', 'Your participant ID is '+ str(user_id)])
    # osc_send_i('/ITL/scene/userid', ['fontSize', 40])
    # osc_send_i('/ITL/scene/userid', ['y', 0.2])
    # #osc_send_i('/ITL/scene/uinscore',['watch', 'mouseDown', '( /ITL browse "' + links[seq-1]+'" )'])
    # #lib.subprocess.call(['osascript', '-e', 'quit app "/Applications/INScoreViewer-1.21.app"'])
    # #lib.sys.exit(-1)
    print 'Program Terminated'