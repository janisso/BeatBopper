### The code belows plays back a MIDI file
# Inputs:
#   phase - calculated phase from any of the methods
#   amp - amplitude of the movement that is translated into MIDI Velocity value
#   stop_all - this is a global variable that acts as a flag to let the rest of the system know that there are no more midi messages to plahy. i.e. the file is finished
#   g - grade of the performance
#   e - which excerpt to play from the g foler
# Outputs:
#   OSC - File to load in Inscore
#   OSC - shared variable that gets
#   stop_all - global variable that is set to '1' when there are no more messages to play from the MIDI file


import lib


def phase_advance(beats,stop_all):
    playhead = 0
    while True:
        playhead += 0.01
        #print playhead
        beats.value = playhead
        lib.time.sleep(0.005)
        if stop_all.value == True:
            break
        #if playhead > 10.0:
        #    break



def play_midi(midi_path, save_path, beats, vel, stop_all):
    f = open(save_path + '/play_midi.csv', 'w+')                # open file to save log values
    f.write('time,beats,midi_note,midi_vel\n')                  # write first line with corresponding titles
    mid = lib.mido.MidiFile(midi_path)                          # save parsed MIDI file using mido library
    s_times = []  # np.zeros((times[0],2))                      # create an empty array to storenote events in the MIDI file
    port = lib.mido.open_output(lib.mido.get_output_names()[0]) # open port to send MIDI messages
    all_time = 0                                                # aggregate time for all the messages
    msg_count = 0                                               # this is to count MIDI messages with note information
    all_messages = []                                           # create an ampty array to only store note information and their position in the score
    for msg in mid:                                             # for every message in the midi file
        all_time += msg.time                                    # the file stores midi time based on previous onset, we h
        if hasattr(msg, 'note'):                                # checks that the MIDI message is Note
            #all_time += msg.time                                #
            all_messages.append(msg)                            # adds note message from MIDI file to our playback thing
            s_times.append([msg_count, all_time])               # array to store note score time
            msg_count += 1                                      # count of how many note messages there are in total
    s_times = lib.np.array(s_times)                             # convert array to numpy.array
    yo = lib.copy.deepcopy(s_times)                             # deepcopy the array so the original doesn't get manipulated
    while True:
        if len(yo) != 0:                                        # keep running the loop until there are no more notes to play
            # print 'hello',yo[0,1],unravelTime.value
            # print yo[0,1],'dfsdfsdfsdfsdfs',unravelTime.value
            if yo[0, 1] < beats.value:                          # if the playhead is larger than the first note in the array play the first note and then delete
                msgMIDI = all_messages[int(yo[0, 0])]           # add note information and it's timing to the midi message to be sent
                msgMIDI.velocity = vel.value                    # add velocity to the MIDI message to be sent
                f.write(                                        # store values for later analysis
                    "%f, %f, %f, %f\n" % (lib.time.time(), beats.value, all_messages[int(yo[0, 0])].note, vel.value))
                port.send(msgMIDI)                              # send the message using predefined port (midi device)
                #msg_count += 1
                yo = lib.np.delete(yo, 0, 0)                    # once the note has been played delete the first message
        else:                                                   # if there are no more notes to play
            f.close                                             # stop storing the values in csv
            stop_all.value = 1                                  # flag to indicate to the rest of the system that the file has finished.
            print 'MIDI Playback Finished'                      # print for use rto acknowledge
            break

def play(midi_path,save_path):
    vel = lib.multiprocessing.Value('i', 127)   # variable to store amplitude value received from Leap Motion to convert into MIDI velocity
    beats = lib.multiprocessing.Value('d', 0.0) # variable holding the advanceing beat information of the MIDI file
    stop_all = lib.multiprocessing.Value('i', False)    # boolean variable that tell rest of the system that the MIDI file has finished playing

    p_play_midi =  lib.multiprocessing.Process(target=play_midi,args=(midi_path,save_path,beats,vel,stop_all))  # process to play MIDI
    p_phase_advance = lib.multiprocessing.Process(target=phase_advance,args=(beats,stop_all))                   # process to count phase informatioin

    p_play_midi.start()
    lib.time.sleep(0.5)
    p_phase_advance.start()

    p_play_midi.join()
    lib.time.sleep(0.5)
    p_phase_advance.join()
