### This is the main file that controls rest of the files. It initiates sets up some of the global variables

import argparse
import pam_test
import lib

if __name__ == '__main__':
    parser = argparse.ArgumentParser()                                              # declaration of arguments
    parser.add_argument('-m', '--method', help='Enter Rubato induction method: 0-Naive; 1-Compensation; 2-Phase estimation; 3-Demo')
    #parser.add_argument('-s', '--save_path', help='Enter path to save log files')   # path to save log files
    args = parser.parse_args()                                                      # variable to store list of user input variables                                               # variable to store User ID
    #midi_file = args.midi_file                                                           # variable to store the name of the MIDI file, all the MIDI files should be stored in midi_files folder of the project
    midi_device = 0#int(args.midi_device)
    #tempo_method = int(args.method)
    #save_path = args.save_path                                                     # variable to save log files

    curr_path = lib.os.path.dirname(lib.os.path.abspath(__file__))                          # paht where this file is running from
    save_path = '/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/DRIFT'                               # path to store data in csv file
    #midi_path = curr_path + '/midi_files/' + midi_file + '/' + midi_file# + '.mid'                     # paht of the midi file to play

    if not lib.os.path.exists(save_path):                                               # if the path does not exist create it
        lib.os.makedirs(save_path)

    #print 'User ID: ', user_id                                                      # Printing stuff for debugging
    print 'Save Path: ', save_path

    #STORE METHODS ARRAY
    ms = []
    for i in range(len(args.method)):
        ms.append(int(args.method[i]))

    #SETTING UP OSC CLIENT FOR INSCOR
    lib.time.sleep(3)

    lib.time.sleep(2)
    pam_test.play(save_path+'/'+str(i)+'_'+str(ms[i]), midi_device, ms[i], 0)
    print 'Program Terminated'