import lib

def naive_tempo(palm_pos,hand_vel,hand_span,stop_all):
    while True:
        print 'palm_pos ',palm_pos.value,' hand_vel ',hand_vel.value,' hand_span ',hand_span.value
        lib.time.sleep(0.005)
        if stop_all.value == True:
            break