### This is the main file that controls rest of the files. It initiates sets up some of the global variables

import argparse
import os
import midi_play

if __name__ == '__main__':

    parser = argparse.ArgumentParser()                                              # declaration of arguments
    parser.add_argument('-u', '--user_id', help='Enter user ID')                    # user_id
    parser.add_argument('-m', '--midi', help='Enter MIDI file to played back')      # MIDI file to open
    #parser.add_argument('-s', '--save_path', help='Enter path to save log files')   # path to save log files
    args = parser.parse_args()                                                      # variable to store list of user input variables
    user_id = int(args.user_id)                                                     # variable to store User ID
    midi_file = args.midi                                                           # variable to store the name of the MIDI file, all the MIDI files should be stored in midi_files folder of the project
    #save_path = args.save_path                                                     # variable to save log files

    curr_path = os.path.dirname(os.path.abspath(__file__))
    save_path = curr_path + '/users/' + str(user_id)
    midi_path = curr_path + '/midi_files/' + midi_file + '.mid'

    if not os.path.exists(save_path):
         os.makedirs(save_path)

    print 'User ID: ', user_id
    print 'MIDI File: ', midi_path
    print 'Save Path: ', save_path

    midi_play.play(midi_path,save_path)