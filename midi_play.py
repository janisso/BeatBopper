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
        playhead = playhead + 0.01
        beats.value = playhead
        #print 'Playhead: ', beats.value
        lib.time.sleep(0.005)
        if stop_all.value == True:
            break
        if playhead > 10.0:
            break



def play_midi(midi_path, save_path, beats, amp, stop_all):

    #path = '/Users/mb/Desktop/Janis.So/06_qmul/BB/02_inputs/inscore_stuff/main_menu/l_' + str(g) + '/'
    f = open(save_path + '/play_midi.csv', 'w+')
    f.write('time,beats,midi_note,midi_vel\n')
    #mids = ['demo', '01', '02', '03', '04', '05', '06']
    # times = [45]

    mid = lib.mido.MidiFile(midi_path)
    s_times = []  # np.zeros((times[0],2))
    port = lib.mido.open_output(lib.mido.get_output_names()[0])
    #print lib.mido.get_output_names()
    all_time = 0
    msg_count = 0
    all_messages = []
    for msg in mid:
        all_time += msg.time
        # if not msg.is_meta:
        if hasattr(msg, 'note'):
            all_time += msg.time
            all_messages.append(msg)
            s_times.append([msg_count, all_time])
            msg_count += 1
    s_times = lib.np.array(s_times)
    yo = lib.copy.deepcopy(s_times)
    while True:
        if len(yo) != 0:
            # print 'hello',yo[0,1],unravelTime.value
            # print yo[0,1],'dfsdfsdfsdfsdfs',unravelTime.value
            if yo[0, 1] < beats.value:
                # print 'hello'
                bim = amp.value
                # oscSend(str(int(unravelTime.value*4)))
                midiVel = 127 #int(abs(bim) / 1200 * 127)
                #if midiVel > 127:
                #    midiVel = 127
                msgMIDI = all_messages[int(yo[0, 0])]
                msgMIDI.velocity = midiVel
                f.write(
                    "%f, %f, %f, %f\n" % (lib.time.time(), beats.value, all_messages[int(yo[0, 0])].note, midiVel))
                # print msgMIDI.velocity,midiVel
                port.send(msgMIDI)
                # oscSend(int(unravelTime.value*4))
                # print 'Play Midi ',unravelTime.value, all_messages[int(yo[0,0])]
                msg_count += 1
                yo = lib.np.delete(yo, 0, 0)
                # sleep(0.001)
        else:
            f.close
            stop_all.value = 1
            print 'MIDI Playback Finished'
            break

def play(midi_path,save_path):
    amp = lib.multiprocessing.Value('d', 0.0)   # variable to store amplitude value received from Leap Motion to convert into MIDI velocity
    beats = lib.multiprocessing.Value('d', 0.0) # variable holding the advanceing beat information of the MIDI file
    stop_all = lib.multiprocessing.Value('i', False)    # boolean variable that tell rest of the system that the MIDI file has finished playing

    p_phase_advance = lib.multiprocessing.Process(target=phase_advance,args=(beats,stop_all))
    p_play_midi =  lib.multiprocessing.Process(target=play_midi,args=(midi_path,save_path,beats,amp,stop_all))

    p_phase_advance.start()
    p_play_midi.start()

    p_phase_advance.join()
    p_play_midi.join()