import lib

#REGRESSION CLASS
class REG():
    def __init__(self,window_length,guess_amp):
        self.est_frac = (5*2*lib.np.pi)/1000
        self.est_phase = 0
        self.est_std = 250
        self.prev_std = 0
        self.counts = 0
        self.prev_phase = 0
        self.wl = window_length
        self.t = lib.np.linspace(0,window_length,num=window_length,endpoint=False)

    def doReg(self,q,u_phase,q1,midi_vel,stop_all,savePath):
        f = open(savePath+'/do_reg.csv','w+')
        f.write('time,est_amp,est_freq,est_phase\n')
        while True:
            if not q.empty():
                #print 'reg here'
                start = lib.time.time()
                yo = q.get()
                data = yo[0]
                if len(lib.np.unique(data))>1:
                    #print data
                    #nr = yo[1]
                    guess_std = 1000#self.est_std
                    guess_phase = self.est_phase + self.est_frac*50/(2*lib.np.pi)
                    guess_frac = self.est_frac+0.006
                    optimize_func = lambda x: x[0]*lib.np.sin(self.t*x[1]+x[2]) - data
                    #self.est_std, self.est_frac, self.est_phase = least_squares(optimize_func, [guess_std, guess_frac, guess_phase],bounds=([0,0,self.est_phase],[1500,5,self.est_phase+np.pi/2]),max_nfev=100).x
                    self.est_std, self.est_frac, self.est_phase = lib.least_squares(optimize_func, [guess_std, guess_frac, guess_phase],bounds=([0.0000001,0.0005,self.est_phase],[3000,0.15,lib.np.inf]),max_nfev=50).x
                    if (self.est_phase < self.prev_phase) or (self.est_phase > self.prev_phase+lib.np.pi):
                        #self.est_phase = self.prev_phase
                        self.est_phase = u_phase.value
                    if (self.est_std > 1200):
                        self.est_std = self.prev_std
                    midi_vel.value = int(abs(self.est_std)/1200*127)
                    self.prev_std = self.est_std
                    self.prev_phase = self.est_phase
                    self.prev_frac = self.est_frac
                    q1.put([self.est_phase, self.est_frac])
                    f.write("%f, %f, %f, %f\n"%(lib.time.time(),self.est_std,self.est_frac,self.est_phase))
                    self.counts+=1
                    #print 'reg_phase',self.est_phase/(2*lib.np.pi)
            if stop_all.value == 1:
                f.close
                break

def phase_tempo(q,palm_pos,hand_vel,hand_span,stop_all,arm_flag, play_flag,u_phase, up_thresh, save_path):
    f_data = open(save_path+'/phase_tempo_data.csv', 'w+')
    f_phase = open(save_path+'/phase_phase.csv', 'w+')

    f_data.write('time, palm_pos, vel, avg_vel, avg_vel_schm, avg_acc, avg_acc_schm, avg_still_buff\n')
    f_phase.write('time, phase\n')

    avg_vel = 0
    prev_avg_vel = 0

    avg_acc = 0
    prev_avg_acc = 0

    avg_vel_schm = 0
    prev_avg_vel_schm = 0

    avg_acc_schm = 0
    prev_avg_acc_schm = 0

    beat_phase = 3                                                  # set the beat phase to 3, to set the system to start counting phase cycles from 0

    timer = -1                                                      # timer to dissalow phases that occur too soon
    timer_up = 10
    window_time = 0

    is_still = False


    curr_beat_time = lib.time.time()
    prev_beat_time = 0

    beat_dt = 0
    #tempo = 0

    #SETUP CIRCULAR BUFFER FOR LPF
    circ_buff = lib.CircularBuffer(size=lib.window_length)
    for i in range(lib.window_length):
        circ_buff.append(0)

    circ_buff_reg = lib.CircularBuffer(size = 400)
    for i in range(400):
        circ_buff_reg.append(0)
    reg_data = lib.np.zeros(len(circ_buff_reg))

    still_buff = lib.CircularBuffer(size=10)
    for i in range(len(still_buff)):
        still_buff.append(0)

    while True:
        #print 'Phase Est'
        circ_buff.append(hand_vel.value)                            # getting hand_vel.value and putting itno circular buffer
        circ_buff_reg.append(hand_vel.value)

        # getting filtered values for average
        avg_vel = sum(circ_buff*lib.coeffs)                         # filtered avg_vel
        avg_vel_schm = lib.schmit(avg_vel, 100)                      # filtered avg_vel with schmitt trigger

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
            print 'Armed'

        if is_still == False:
            if arm_flag.value:
                # verification module
                if ((avg_vel_schm * prev_avg_vel_schm < 0) and (prev_avg_vel_schm < avg_vel_schm) and (beat_phase == 3)):# and (timer < 0)):
                    print 'Beat 0', u_phase.value / (2*lib.np.pi)
                    beat_phase = 0
                    timer = timer_up
                    u_phase.value += lib.np.pi/2
                    if play_flag.value:
                        up_thresh.value += 0.25
                    f_phase.write('%f, %i\n' % (lib.time.time(), beat_phase))
                    #if (arm_flag.value == True) and (play_flag.value == False):
                    play_flag.value = True
                    #print 'play now', play_flag.value

                if ((avg_acc_schm * prev_avg_acc_schm < 0) and (beat_phase == 0) and (timer < 0) and (avg_vel_schm > 0)):
                    print 'Beat 1', u_phase.value / (2*lib.np.pi)
                    beat_phase = 1
                    timer = timer_up
                    u_phase.value += lib.np.pi/2
                    if play_flag.value:
                        up_thresh.value += 0.25
                    f_phase.write('%f, %i\n' % (lib.time.time(), beat_phase))

                if ((avg_vel_schm * prev_avg_vel_schm < 0) and (beat_phase == 1) and (timer < 0)):
                    print 'Beat 2', u_phase.value / (2 * lib.np.pi)
                    beat_phase = 2
                    timer = timer_up
                    u_phase.value += lib.np.pi / 2
                    if play_flag.value:
                        up_thresh.value += 0.25
                    f_phase.write('%f, %i\n' % (lib.time.time(), beat_phase))

                if ((avg_acc_schm * prev_avg_acc_schm < 0) and (beat_phase == 2) and (timer < 0) and (avg_vel_schm < 0)):
                    print 'Beat 3', u_phase.value / (2 * lib.np.pi)
                    beat_phase = 3
                    timer = timer_up
                    u_phase.value += lib.np.pi / 2
                    if play_flag.value:
                        up_thresh.value += 0.25
                    f_phase.write('%f, %i\n' % (lib.time.time(), beat_phase))
                #if (window_time >= 50) and : #TO DO -> port phase estimation algorithm till the end
            timer -= 1

        if (window_time >= 50):
            window_time = 0
            for i in range(len(circ_buff_reg)):
                reg_data[i] = circ_buff_reg[i]
            q.put((reg_data,0))
        window_time += 1
        #print window_time


        #f_data.write('time, palm_pos, vel, avg_vel, avg_vel_schm, avg_acc, avg_acc_schm')
        f_data.write('%f, %f, %f, %f, %f, %f, %f, %f\n'%(lib.time.time(), palm_pos.value, hand_vel.value, avg_vel, avg_vel_schm, avg_acc, avg_acc_schm, still_buff_avg))
        prev_avg_vel = avg_vel
        prev_avg_vel_schm = avg_vel_schm

        prev_avg_acc = avg_acc
        prev_avg_acc_schm = avg_acc_schm

        #print 'palm_pos ',palm_pos.value,' hand_vel ',hand_vel.value,' hand_span ',hand_span.value

        lib.time.sleep(0.001)
        if stop_all.value == True:
            break

def phase_comp(q1, play_flag, increment, stop_all, save_path):
    f = open(save_path + '/print_phase.csv', 'w+')
    f.write('time,phase_from_reg,phase_for_plbck,plbck_pos\n')
    preffP = 0
    curr_time = lib.time.time()
    prev_time = lib.time.time()
    curr_date = 0
    prev_date = 0
    temp_date = 0
    prev_temp_date = temp_date
    prev_playback_start = 0
    phase_at_start = 0
    phase4plbck = 0
    while True:
        if not q1.empty():
            array = q1.get()
            fP = array[0]
            fS = array[1]
            if prev_playback_start != play_flag.value:
                prev_playback_start = 1
                phase_at_start = fP
                #print 'start countoff'
            if play_flag.value != 0:
                phase4plbck = fP - phase_at_start
            curr_time = lib.time.time()
            curr_date = phase4plbck
            print increment.value, curr_date
            if curr_date < prev_date:
                curr_date = prev_date
            time_diff = (curr_time - prev_time) / 0.011
            increment.value = (curr_date + fS * 1000 * time_diff - prev_date) / (2 * lib.np.pi) / (time_diff / 0.011)
            prev_time = curr_time
            prev_date = curr_date
            f.write("%f, %f, %f, %f\n" % (lib.time.time(), fP, phase4plbck, curr_date))
        if stop_all.value == 1:
            break