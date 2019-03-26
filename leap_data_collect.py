import pam
import lib


if __name__ == '__main__':
    path = str('/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/DRIFT')
    ####DECLARE VARIABLES AND PROCESSES
    #save_path = lib.multiprocessing.Value('i',
    #                                     False)  # boolean variable that tell rest of the system that the MIDI file has finished playing
    stop_all = lib.multiprocessing.Value('i', False)            # boolean variable that tell rest of the system that the MIDI file has finished playing
    palm_pos = lib.multiprocessing.Value('d', 0.0)
    hand_vel = lib.multiprocessing.Value('d', 0.0)
    hand_span = lib.multiprocessing.Value('d', 0.0)
    p_get_samples = lib.multiprocessing.Process(target=lib.get_samples,
                                                args=(palm_pos, hand_vel, hand_span, stop_all, path))

    ######START PROCESS
    p_get_samples.start()

    #####JOINE PROCESS
    p_get_samples.join()