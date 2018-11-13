import Leap
import time
import numpy as np

def get_samples(palm_pos, hand_vel,hand_span,stop_all, save_path):
    f = open(save_path + '/get_samples.csv', 'w+')
    f.write('time,palm_pos,palm_vel,span\n')
    controller = Leap.Controller()
    while True:
        frame = controller.frame()
        for hand in frame.hands:
            # GETTING PALM VELOCITY
            palm_pos.value = hand.palm_position.y
            hand_vel.value = hand.palm_velocity.y
            # print hand.fingers[0].position
            for finger in hand.fingers:
                if finger.type == 0:
                    thumb_pos = finger.tip_position
                if finger.type == 4:
                    pinky_pos = finger.tip_position
            hand_span.value = np.sqrt(
                (thumb_pos.x - pinky_pos.x) ** 2 + (thumb_pos.y - pinky_pos.y) ** 2 + (thumb_pos.z - pinky_pos.z) ** 2)
        f.write("%f, %f, %f, %f\n" % (time.time(), palm_pos.value, hand_vel.value, hand_span.value))
        time.sleep(0.01)
        if stop_all.value == 1:
            f.close
            break