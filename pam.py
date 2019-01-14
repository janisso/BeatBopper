### The code belows plays back a MIDI file
# Inputs:
#   phase - calculated phase from any of the methods
#   amp - amplitude of the movement that is translated into MIDI Velocity value
#   stop_all - this is a global variable that acts as a flag to let the rest of the system know that there are no more midi messages to plahy. i.e. the file is finished
#   g - grade of the performance
#   e - which excerpt to play from the g foler

import lib
import naive
import phase_est

# Function for advnacing the playhead
def phase_advance_naive(save_path,beats,tempo,stop_all,play_flag):
    f = open(save_path + '/phase_advance_naive.csv', 'w+')                # open file to save log values
    f.write('time, beats\n')                                        # write first line with corresponding titles
    playhead = 0
    tempo_change = 120
    prev_tempo = tempo.value
    beat_counter = 0
    while True:
        # COMPARATOR
        if (prev_tempo != tempo.value):
            prev_tempo = tempo.value
            print 'Change detected', beat_counter, playhead * 2
            if play_flag.value:
                beat_counter += 1


        if play_flag.value:
            playhead += (prev_tempo/2/60.0)*0.0064
            beats.value = playhead
            f.write(  # store values for later analysis
                "%f, %f\n" % (lib.time.time(), beats.value))
            lib.time.sleep(0.005)
            #print playhead
        if stop_all.value == True:
            break

def phase_advance_comp(save_path,beats,tempo,stop_all,play_flag):
    f = open(save_path + '/phase_advance_comp.csv', 'w+')                # open file to save log values
    f.write('time, beats\n')                                        # write first line with corresponding titles
    playhead = 0
    tempo_change = 120
    beat_counter = 0

    rem = 0

    prev_tempo = tempo.value

    new_val = False

    while True:

        # COMPARATOR
        if (prev_tempo != tempo.value):
            prev_tempo = tempo.value
            new_val = True
            #print 'Change detected', beat_counter, playhead * 2

        # ONLY CHANGE TEMPO WHEN TEMPO CHANGE HAS BEEN DETECTED
        if new_val == True:# and play_flag.value:
            rem = beat_counter + 1 - playhead * 2
            tempo_change = prev_tempo * rem
            if play_flag.value:
                beat_counter += 1
            new_val = False

        if play_flag.value:
            playhead += (tempo_change/2/60.0)*0.0064
            beats.value = playhead
            f.write(  # store values for later analysis
                "%f, %f\n" % (lib.time.time(), beats.value))
            lib.time.sleep(0.005)
            #print playhea
        if stop_all.value == True:
            break

def phase_advance_bb(increment,beats,up_thresh,stop_all):
    playhead = 0
    while True:
        if playhead <= up_thresh.value:
            playhead += increment.value
            beats.value = playhead/2
        else:
            beats.value = beats.value
        lib.time.sleep(0.009)
        if stop_all.value == True:
            break

def phase_advance_demo():
    #TODO - will be a function here to advance the playhead for people to follow

# Function to change tempo and velocity using keyboard
def user_input(newstdin, tempo,vel):
    while True:
        lib.sys.stdin = newstdin
        #print 'test'
        u_input  = raw_input()
        t = u_input.split()[0]
        v = u_input.split()[1]
        tempo.value = float(t)
        vel.value = int(v) #this is where this process doesn't fail anymore
        print 'Tempo: ', t, 'Velocity: ', v

# Function to send OSC messages to InScore
def osc_cursor(beats,stop_all):
    #SETTING UP OSC CLIENT FOR INSCORE
    osc_port =lib.OSC.OSCClient()
    osc_port.connect(('localhost', 7000))   # INSCORE
    osc_msg_cursor = lib.OSC.OSCMessage()
    osc_msg_cursor.setAddress('/ITL/scene/sync')
    osc_msg_cursor.append('cursor')
    osc_msg_cursor.append('score')
    osc_port.send(osc_msg_cursor)
    while True:
        osc_msg_i = lib.OSC.OSCMessage()
        osc_msg_i.setAddress('/ITL/scene/cursor')
        osc_msg_i.append('date')
        osc_msg_i.append(int(beats.value*8))
        osc_msg_i.append(16)
        osc_port.send(osc_msg_i)
        lib.time.sleep(0.01)
        if stop_all.value:# == True:
            osc_port.close()
            break

# Function to send MIDI messages
def play_midi(midi_path, save_path, beats, midi_vel, stop_all,midi_device_nr):
    f = open(save_path + '/play_midi.csv', 'w+')                # open file to save log values
    f.write('time,beats,midi_note,midi_vel\n')                  # write first line with corresponding titles
    mid = lib.mido.MidiFile(midi_path)                          # save parsed MIDI file using mido library
    s_times = []  # np.zeros((times[0],2))                      # create an empty array to storenote events in the MIDI file
    port = lib.mido.open_output(lib.mido.get_output_names()[midi_device_nr.value]) # open port to send MIDI messages
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
            if yo[0, 1] < beats.value:                          # if the playhead is larger than the first note in the array play the first note and then delete
                msgMIDI = all_messages[int(yo[0, 0])]           # add note information and it's timing to the midi message to be sent
                if midi_vel.value > 127:
                    msgMIDI.velocity = 127
                else:
                    msgMIDI.velocity = midi_vel.value                    # add velocity to the MIDI message to be sent
                f.write(                                        # store values for later analysis
                    "%f, %f, %f, %f\n" % (lib.time.time(), beats.value, all_messages[int(yo[0, 0])].note, midi_vel.value))
                port.send(msgMIDI)                              # send the message using predefined port (midi device)
                yo = lib.np.delete(yo, 0, 0)                    # once the note has been played delete the first message
        else:                                                   # if there are no more notes to play
            f.close                                             # stop storing the values in csv
            stop_all.value = True                                 # flag to indicate to the rest of the system that the file has finished.
            print 'MIDI Playback Finished'                      # print for use rto acknowledge
            break

def play(midi_path,save_path,midi_device, tempo_method):
    newstdin = lib.os.fdopen(lib.os.dup(lib.sys.stdin.fileno()))

    tempo = lib.multiprocessing.Value('d', 120.0)
    midi_vel = lib.multiprocessing.Value('i', 127)                   # variable to store amplitude value received from Leap Motion to convert into MIDI velocity
    beats = lib.multiprocessing.Value('d', -0.0000001)                 # variable holding the advanceing beat information of the MIDI file
    stop_all = lib.multiprocessing.Value('i', False)            # boolean variable that tell rest of the system that the MIDI file has finished playing

    palm_pos = lib.multiprocessing.Value('d',0.0)
    hand_vel = lib.multiprocessing.Value('d',0.0)
    hand_span = lib.multiprocessing.Value('d',0.0)

    arm_flag = lib.multiprocessing.Value('i', False)            # boolean variable
    play_flag = lib.multiprocessing.Value('i', False)            # boolean variable

    midi_device_nr = lib.multiprocessing.Value('i', midi_device)

    print 'Tempo Method ',tempo_method

    #p_user_input = lib.multiprocessing.Process(target=user_input, args=(newstdin,tempo,midi_vel))

    p_play_midi = lib.multiprocessing.Process(target=play_midi,args=(midi_path,save_path,beats,midi_vel,stop_all,midi_device_nr))  # process to play MIDI
    if tempo_method == 0:
        print tempo_method
        p_phase_advance = lib.multiprocessing.Process(target=phase_advance_naive,args=(save_path,beats,tempo,stop_all,play_flag))                   # process to count phase informatioin
        p_tempo = lib.multiprocessing.Process(target=naive.naive_tempo, args=(palm_pos, hand_vel, hand_span, midi_vel, stop_all, arm_flag, play_flag, tempo, save_path))
    if tempo_method == 1:
        print tempo_method
        p_phase_advance = lib.multiprocessing.Process(target=phase_advance_comp,args=(save_path,beats,tempo,stop_all,play_flag))                   # process to count phase informatioin
        p_tempo = lib.multiprocessing.Process(target=naive.naive_tempo, args=(palm_pos, hand_vel, hand_span, midi_vel, stop_all, arm_flag, play_flag, tempo, save_path))
    if tempo_method == 2:
        r = phase_est.REG(400, 1)
        q = lib.multiprocessing.Queue()
        q1 = lib.multiprocessing.Queue()
        u_phase = lib.multiprocessing.Value('d', 0.0)
        up_thresh = lib.multiprocessing.Value('d', 0.0)#                                                          q, palm_pos, hand_vel, hand_span, stop_all, arm_flag, u_phase, up_thresh, save_path
        amp = lib.multiprocessing.Value('d', 0.0)
        increment = lib.multiprocessing.Value('d', 0.0)
        p_reg = lib.multiprocessing.Process(target=r.doReg, args=(q, u_phase, q1, midi_vel, stop_all, save_path))
        p_phase_comp = lib.multiprocessing.Process(target=phase_est.phase_comp, args=(q1, play_flag, increment, stop_all, save_path))
        p_phase_advance = lib.multiprocessing.Process(target=phase_advance_bb,args=(increment, beats, up_thresh, stop_all))                   # process to count phase informatioin
        p_tempo = lib.multiprocessing.Process(target=phase_est.phase_tempo, args=(q, palm_pos, hand_vel, hand_span, stop_all, arm_flag, play_flag, u_phase, up_thresh, save_path))


    p_osc_cursor = lib.multiprocessing.Process(target=osc_cursor,args=(beats,stop_all))
    p_get_samples = lib.multiprocessing.Process(target=lib.get_samples, args=(palm_pos, hand_vel, hand_span, stop_all, save_path))

    #p_user_input.start()

    p_get_samples.start()
    p_tempo.start()
    p_play_midi.start()

    if tempo_method == 2:
        p_reg.start()
        p_phase_comp.start()
        print 'started reg'

    lib.time.sleep(0.5)
    p_phase_advance.start()
    p_osc_cursor.start()

    #p_user_input.join()

    if tempo_method == 2:
        p_reg.join()
        p_phase_comp.join()
        print 'joined reg'

    p_get_samples.join()
    p_tempo.join()

    p_play_midi.join()
    lib.time.sleep(0.5)
    p_phase_advance.join()
    p_osc_cursor.join()