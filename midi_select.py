import mido

for i in range(len(mido.get_output_names())):
    print str(i)+' - '+ mido.get_output_names()[i]