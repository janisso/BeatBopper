from mingus.midi import fluidsynth
from mingus.containers.note import Note

fluidsynth.init("/Users/js/Desktop/sounds/Nice-Keys-PlusSteinway-JNv2.0.sf2")
fluidsynth.play_Note(Note("C-5"))