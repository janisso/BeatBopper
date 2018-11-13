import time

def naive_tempo(palm_pos,hand_vel,hand_span,stop_all,arm_flag):
    while True:
        #print hand_span.value
        if (hand_span.value > 80) and (arm_flag.value == False):
            arm_flag.value = 1
            print 'Armed'
        #print 'palm_pos ',palm_pos.value,' hand_vel ',hand_vel.value,' hand_span ',hand_span.value
        time.sleep(0.005)
        if stop_all.value == True:
            break