import lib

def naive_tempo(palm_pos,hand_vel,hand_span,midi_vel,stop_all,arm_flag, play_flag, tempo, save_path):
    f_data = open(save_path+'/naive_tempo_data.csv', 'w+')
    f_phase = open(save_path+'/naive_phase.csv', 'w+')

    f_data.write('time, palm_pos, vel, avg_vel, avg_vel_schm, avg_acc, avg_acc_schm, avg_still_buff\n')
    f_phase.write('time, phase\n')

    avg_vel = 0
    prev_avg_vel = 0

    avg_acc = 0
    prev_avg_acc = 0
                                      # set the beat phase to 3, to set the system to start counting phase cycles from 0
    timer = -1                                                      # timer to dissalow phases that occur too soon

    curr_beat_time = lib.time.time()
    prev_beat_time = 0

    beat_dt = 0
    #tempo = 0

    start_play = False

    #SETUP CIRCULAR BUFFER FOR LPF
    circ_buff = lib.CircularBuffer(size=lib.window_length)
    rect_buff = lib.CircularBuffer(size=lib.window_length)
    for i in range(lib.window_length):
        circ_buff.append(0)
        rect_buff.append(0)

    still_buff = lib.CircularBuffer(size=10)
    for i in range(len(still_buff)):
        still_buff.append(0)
    print 'NAIVE TEMPO HERE'
    while True:
        circ_buff.append(hand_vel.value)                            # getting hand_vel.value and putting itno circular buffer
        rect_buff.append(abs(hand_vel.value))

        # getting filtered values for average
        avg_vel = sum(circ_buff*lib.coeffs)                         # filtered avg_vel
        rect_val = sum(rect_buff*lib.coeffs)
        avg_vel_schm = lib.schmit(avg_vel, 20)                      # filtered avg_vel with schmitt trigger

        still_point = lib.is_still(avg_vel,1)                     # function for checking if the hand is still,
                                                                    # if the number is set low -> hand tremor will trigger beats
                                                                    # if the number is set to high -> some of the smaller movements will not trigger beats, this needs to be explained to the use
        still_buff.append(still_point)
        still_buff_avg = sum(still_buff)/float(len(still_buff))
        if still_buff_avg > 0.8:
            is_still = True
            #print still_buff_avg
        if still_buff_avg <= 0.8:
            is_still = False
        #print is_still#, still_buff_avg

        # getting values for acceleration
        avg_acc = (avg_vel - prev_avg_vel)*100
        avg_acc_schm = lib.schmit(avg_acc,150)
        #print avg_acc_schm, prev_avg_acc_schm
        #print hand_span.value

        if (hand_span.value > 80) and (arm_flag.value == False):
            arm_flag.value = 1
            #play_flag.value = 1
            print 'ARMED'

        if is_still == False:
            # verification module
            if ((avg_vel * prev_avg_vel < 0) and (prev_avg_vel < avg_vel)):# and (timer < 0)):
                beat_phase = 0
                curr_beat_time = lib.time.time()
                beat_dt = curr_beat_time - prev_beat_time
                tempo.value = 60./beat_dt
                prev_beat_time = curr_beat_time
                #timer = timer_up
                f_phase.write('%f, %i\n' % (lib.time.time(), beat_phase))
                print 'Beat ', tempo.value, ' dt ', beat_dt, avg_vel

                #if (arm_flag.value == True) and (play_flag.value == False):
                #    play_flag.value = True
                #    print 'play now', play_flag.value

            if ((prev_avg_acc * avg_acc) <= 0):
                #midi_vel.value = abs(int((avg_vel/1500.)*127.))
                #ting = abs(int((hand_vel.value/1500.)*127.))
                ting = abs(int((rect_val / 1000.) * 127.))
                #ting = abs(hand_vel.value)
                print hand_vel.value, avg_vel, ting
                if (ting > 127):
                    midi_vel.value = 127
                else:
                    midi_vel.value = ting
                #print 'Amp ',midi_vel.value

        timer -= 1
        #f_data.write('time, palm_pos, vel, avg_vel, avg_vel_schm, avg_acc, avg_acc_schm')
        f_data.write('%f, %f, %f, %f, %f, %f, %f, %f\n'%(lib.time.time(), palm_pos.value, hand_vel.value, avg_vel, avg_vel_schm, avg_acc, avg_acc_schm, still_buff_avg))
        prev_avg_vel = avg_vel
        prev_avg_acc = avg_acc


        #print 'palm_pos ',palm_pos.value,' hand_vel ',hand_vel.value,' hand_span ',hand_span.value

        lib.time.sleep(0.005)
        if stop_all.value == True:
            break