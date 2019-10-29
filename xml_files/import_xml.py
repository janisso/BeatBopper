#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
import music21
music21.environment.UserSettings()['warnings'] = 0

import os
dirname = os.path.dirname(__file__)

#GET THE FILE, EXTRACT SIGNATURE
file_name = music21.converter.parse(dirname+'/M07-1/M07-1.musicxml')

flat_file = file_name.flat
allTimeSignatures = flat_file.getElementsByClass('TimeSignature')
fileSignature = allTimeSignatures[0]
signatureNumerator = fileSignature.numerator
signatureDenominator = fileSignature.denominator

#len_measures = 

#section = file_name.measures(1,5)
#fp = section.write('xml', fp='/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/xml_files/M07-1/section.xml')

#print('Measure',i)
#for y in range (0,len(file_name.getElementsByClass('Part'))):
#	noteLength = len(file_name.getElementsByClass('Part')[y].getElementsByClass('Measure')[piece[i]].flat.notes)
#	notess = file_name.getElementsByClass('Part')[y].getElementsByClass('Measure')[piece[i]].flat.notes

#for part in file_name.getElementsByClass('Part'):
#    length = len(part.getElementsByClass('Measure'))
#    print(length)
#    #for measure in part:
#    #    print measure
    
#REPEAT SIGNS, UNFOLD THE FILE
repeats = []
fileLenght = len(file_name.getElementsByClass('Part')[0].getElementsByClass('Measure'))
for i in range(0,fileLenght):
	barss = file_name.getElementsByClass('Part')[0].getElementsByClass('Measure')[i]
	is_there = len(barss.getElementsByClass(music21.bar.Repeat))
	if is_there != 0:
		for j in range(0,is_there):
			pimpis = barss.getElementsByClass(music21.bar.Repeat)[j].direction
		hello = barss.getElementsByClass(music21.bar.Repeat).number-1,pimpis
		repeats.append(hello)

#DIFFERENT ENDINGS
#len(TheFile.getElementsByClass('Part')[0].flat.getElementsByClass(spanner.RepeatBracket))
endings = []
repeatLength = len(file_name.getElementsByClass('Part')[0].flat.getElementsByClass('RepeatBracket'))
for k in range(0, repeatLength):
	repeatElem = file_name.getElementsByClass('Part')[0].flat.getElementsByClass('RepeatBracket')[k]
	#repeatElem.elements
	#print(repeatElem.number)
	#print(repeatElem)
	#print(len(repeatElem))
	almond = []
	for l in range(0,len(repeatElem)):
		almond.append(repeatElem[l].number-1)
		#print(repeatElem[l])
	endings.append(almond)
	#print(' ')
#print(endings)

sections = []

section1 = file_name.measures(0,24)
sections.append(section1)

section2 = file_name.measures(25,44)
sections.append(section2)

section3 = file_name.measures(25,43)
section3.getElementsByClass('Part')[0].append(file_name.getElementsByClass('Part')[0].getElementsByClass('Measure')[44])
section3.getElementsByClass('Part')[1].append(file_name.getElementsByClass('Part')[1].getElementsByClass('Measure')[44])
sections.append(section3)

section4 = file_name.measures(46,65)
sections.append(section4)

section5 = file_name.measures(46,63)
section5.getElementsByClass('Part')[0].append(file_name.getElementsByClass('Part')[0].getElementsByClass('Measure')[65])
section5.getElementsByClass('Part')[1].append(file_name.getElementsByClass('Part')[1].getElementsByClass('Measure')[65])
section5.getElementsByClass('Part')[0].append(file_name.getElementsByClass('Part')[0].getElementsByClass('Measure')[66])
section5.getElementsByClass('Part')[1].append(file_name.getElementsByClass('Part')[1].getElementsByClass('Measure')[66])
#section5_b = file_name.measures(67,68)
#section5 = music21.stream.Stream()
#section5.insert(section5_a)
#section5.append(section5_b)
sections.append(section5)

#section3_a.show('text')
#section3_a.show('text')

for i, section in enumerate(sections):
    fp = section.write('xml', fp=dirname+'/M07-1/section_'+str(i)+'.xml')
    fp = section.write('midi',
					   fp=dirname+'/M07-1/section_' + str(i) + '.mid')