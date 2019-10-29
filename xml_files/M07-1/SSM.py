from music21 import *
import numpy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from fractions import Fraction
from decimal import Decimal



#COMMON DENOMINATOR FUNCTION
def GCD(a,b):
	flag = 0
	i = 0
	a = float(a)
	b = float(b)
	while flag == 0:
		d = (a*i)/b
		#gcd = a*i
		if (d%1 == 0 and i > 0):
			flag = 1
			gcd = (a*i)
		i += 1
	return(gcd)



TheFile = converter.parse('/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/xml_files/M07-1/M07-1.musicxml')
flatFile = TheFile.flat
allTimeSignatures = flatFile.getElementsByClass('TimeSignature')
fileSignature = allTimeSignatures[0]
signatureNumerator = fileSignature.numerator
signatureDenominator = fileSignature.denominator

#REPEAT SIGNS
repeats = []
fileLenght = len(TheFile.getElementsByClass('Part')[0].getElementsByClass('Measure'))
for i in range(0,fileLenght):
	barss = TheFile.getElementsByClass('Part')[0].getElementsByClass('Measure')[i]
	is_there = len(barss.getElementsByClass(bar.Repeat))
	if is_there != 0:
		for j in range(0,is_there):
			pimpis = barss.getElementsByClass(bar.Repeat)[j].direction
		hello = barss.getElementsByClass(bar.Repeat).number-1,pimpis
		repeats.append(hello)
#print(repeats)
#print(' ')

#DIFFERENT ENDINGS
#len(TheFile.getElementsByClass('Part')[0].flat.getElementsByClass(spanner.RepeatBracket))
endings = []
repeatLength = len(TheFile.getElementsByClass('Part')[0].flat.getElementsByClass('RepeatBracket'))
for k in range(0, repeatLength):
	repeatElem = TheFile.getElementsByClass('Part')[0].flat.getElementsByClass('RepeatBracket')[k]
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

piece = []
start = 0

for i in range(0,repeatLength/2):
	end = endings[i*2][1]
	for j in range(start,end+1):
		piece.append(j)
	start = repeats[i*2][0]
	end = endings[i*2][0]
	for j in range(start,end):
		piece.append(j)
	start = endings[i*2+1][0]

start = endings[len(endings)-1][0]
end = fileLenght
for j in range(start,end):
	piece.append(j)
#print(piece)
#print(len(piece))

#TheFile.getElementsByClass('Part')[0].getElementsByClass('Measure')[6].flat.notes.show('text')


fullOffsetList = []
fullDurList = []
pigPiece = []
for i in range(0,len(piece)):
	#print('Measure',i)
	for y in range (0,len(TheFile.getElementsByClass('Part'))):
		noteLength = len(TheFile.getElementsByClass('Part')[y].getElementsByClass('Measure')[piece[i]].flat.notes)
		notess = TheFile.getElementsByClass('Part')[y].getElementsByClass('Measure')[piece[i]].flat.notes
		#print('Part',y)
		for j in range(0,noteLength):
			if (notess[j].isChord == 0 and y == 0):
				fullOffsetList.append(notess[j].offset)
				fullDurList.append(notess[j].quarterLength)
				#print(notess[j].midi,notess[j].offset,notess[j].quarterLength)
				pigPiece.append([notess[j].midi,i,notess[j].offset,notess[j].quarterLength])
			if (notess[j].isChord != 0 and y != 0):
				#print('Chord','voice',y)
				#print(len(notess[j].pitches))
				for x in range(0,len(notess[j].pitches)):
					fullOffsetList.append(notess[j].quarterLength)
					fullDurList.append(notess[j].quarterLength)
					#print(notess[j].pitches[x].midi,notess[j].offset,notess[j].quarterLength)
					pigPiece.append([notess[j].pitches[x].midi,i,notess[j].offset,notess[j].quarterLength])
			if (notess[j].isChord == 0 and y != 0):
				#print('Chord','voice',y)
				fullOffsetList.append(notess[j].offset)
				fullDurList.append(notess[j].quarterLength)
				#print(notess[j].midi,notess[j].offset,notess[j].quarterLength)
				pigPiece.append([notess[j].midi,i,notess[j].offset,notess[j].quarterLength])
	#print('Chords')
	#chordis = TheFile.getElementsByClass('Part')[0].getElementsByClass('Measure')[i].getElementsByClass(chord.Chord)
	#chordis.show('text')
	#for j in range(0,len(chordis)):
	#	chordis[j].show('text')

offsetList = list(set(fullOffsetList))
durList = list(set(fullDurList))
offsetList = sorted(offsetList)
durList = sorted(durList)

temp = []
for i in range(0,len(offsetList)):
	temp.append(offsetList[i]%1)

temp = list(set(temp))
offsetList = sorted(temp)

#temp = []
for i in range(0,len(offsetList)):
	a = Fraction(offsetList[i]).limit_denominator().numerator
	b = Fraction(offsetList[i]).limit_denominator().denominator
	temp = [a,b]
	offsetList[i]=temp

#offsetList = sorted(list(set(offsetList)))

for i in range(0,len(durList)):
	a = Fraction(durList[i]).limit_denominator().numerator
	b = Fraction(durList[i]).limit_denominator().denominator
	temp = [a,b]
	durList[i]=temp#Fraction(durList[i]).limit_denominator()

temp = [offsetList[0]]
#temp = offsetList[0]
for i in range(0, len(offsetList)):
	flag = 0
	for j in range(0,len(temp)):
		if offsetList[i] == temp[j]:
			flag += 1
	if flag == 0:
		temp.append(offsetList[i])

offsetList = temp
#print(' ')
#print(offsetList)

#print(' ')
#print(durList)

#GET THE DENOMINATOR FROM OFFSETS
cd = 0
pt = 0
t = 0
for i in range(0,len(offsetList)-1):
	pt = t
	t = GCD(offsetList[i][1],offsetList[i+1][1])
	if t > pt:
		cd = t
#print(cd)

cd = 0
pt = 0
t = 0
#GET THE DENOMINATOR FROM DURATIONS
for i in range(0,len(durList)-1):
	pt = t
	t = GCD(durList[i][1],durList[i+1][1])
	if t > pt:
		cd = t
#print(cd)

totIndex = len(piece)*signatureNumerator*cd
thing = numpy.zeros((totIndex,127))
onsetThing = numpy.zeros((totIndex,127))
onsetThingRot = numpy.zeros((127,totIndex))

for i in range(0,len(pigPiece)):
	#for j in range(0,len(pigPiece[i])):
	midiPitch = pigPiece[i][0]
	noteMeasure = pigPiece[i][1]
	noteOffset = pigPiece[i][2]
	noteDuration = pigPiece[i][3]
	globalOffset = noteMeasure*signatureNumerator+noteOffset
	indexOffset = int(globalOffset * cd)
	indexDuration = int(noteDuration / (1.0/cd))
	o=0
	#print(midiPitch,noteMeasure,noteOffset,noteDuration,globalOffset,indexOffset,indexDuration)
	for k in range(indexOffset,indexOffset+indexDuration):
		thing[k][midiPitch]=1
		peter = 1 - o*(1.0/(4*cd))
		onsetThing[k][midiPitch]=peter
		onsetThingRot[midiPitch][k]=peter
		o+=1

#print(onsetThing[0])
#thing.reshape(totIndex,127)
#thing = thing[::-1]
#thing = zip(thing)
plt.imshow(thing)
plt.figure()
imgplot = plt.imshow(onsetThing)
imgplot.set_cmap('hot')
plt.colorbar()
plt.figure()
imgplot = plt.imshow(onsetThingRot)
imgplot.set_cmap('hot')
plt.colorbar()
plt.show()

numrows = len(thing)

'''
#SSM FOR ABSOLUTE PITCH AND PITCH CLASS
print('Gathering data for AP and PC')
ap = numpy.zeros((numrows,88))
pc = numpy.zeros((numrows,12))

for i in range(0,numrows):
	for j in range(0,len(thing[0])):
		if thing[i][j] != 0:
			ap[i][j - 21 - 1] = 1
			pc[i][j%12] += 1
numpy.savetxt("ap.csv",ap,delimiter=",")
numpy.savetxt("pc.csv",pc,delimiter=",")

print('Doing SSM for AP and PC')

ap_ssm = numpy.zeros((numrows,numrows))
pc_ssm = numpy.zeros((numrows,numrows))
#a_ap = numpy.zeros((1,88))
#a_pc = numpy.zeros((1,12))


for k in range (0,numrows):
	print(k)
	#a_ap = ap[k]
	#a_pc = pc[k]
	#print(a)
	for l in range (0,numrows):
		#b_ap = numpy.array(ap[l])
		#b_pc = numpy.array(pc[l])
		d_ap = numpy.linalg.norm((ap[k]-ap[l]), ord = 1)
		d_pc = numpy.linalg.norm((pc[k]-pc[l]), ord = 1)
		ap_ssm[k][l] = d_ap
		pc_ssm[k][l] = d_pc


#SSM FOR INTERVAL RELATED THINGS
print('Gathering data for AI and IC')
ai = numpy.zeros((numrows-1,88*2+1))
upi = numpy.zeros((numrows-1,88))
ic = numpy.zeros((numrows-1,7))

for i in range(0,numrows-1):
	#print(i)
	#print(i)
	a = [j for j, e in enumerate(thing[i+1]) if e != 0]#GET THE STUFF FROM NEXT FRAME
	b = [j for j, e in enumerate(thing[i]) if e != 0]#GET THE STUFF FROM CURRENT FRAME
	for j in range(0,len(a)):
		for k in range(0,len(b)):
			ai[i][88-(a[j]-b[k])] += 1
			zhenja = abs((a[j]-b[k])%12)
			upi[i][abs(a[j]-b[k])] += 1
			if zhenja == 0:
				ic[i][0] += 1
			elif zhenja == 1 or zhenja == 11:
				ic[i][1] += 1
			elif zhenja == 2 or zhenja == 10:
				ic[i][2] += 1
			elif zhenja == 3 or zhenja == 9:
				ic[i][3] += 1
			elif zhenja == 4 or zhenja == 8:
				ic[i][4] += 1
			elif zhenja == 5 or zhenja == 7:
				ic[i][5] += 1
			elif zhenja == 6:
				ic[i][6] += 1
numpy.savetxt("ai.csv",ai,delimiter=",")
numpy.savetxt("ic.csv",ic,delimiter=",")
ai_ssm = numpy.zeros((numrows-1,numrows-1))
ic_ssm = numpy.zeros((numrows-1,numrows-1))
upi_ssm = numpy.zeros((numrows-1,numrows-1))

print('Doing SSM for AI and IC')
for k in range (0,numrows-1):
	#a_ai = numpy.array(ai[k])
	#a_ic = numpy.array(ic[k])
	print(k)
	for l in range (0,numrows-1):
		#b_ai = numpy.array(ai[l])
		#b_ic = numpy.array(ic[l])
		d_ai = numpy.linalg.norm((ai[k]-ai[l]), ord = 1)
		d_ic = numpy.linalg.norm((ic[k]-ic[l]), ord = 1)
		d_upi = numpy.linalg.norm((upi[k]-upi[l]), ord = 1)
		ai_ssm[k][l] = d_ai
		ic_ssm[k][l] = d_ic 
		upi_ssm[k][l] = d_upi

#fig = plt.figure()
#fig.suptitle('Pitchez', fontsize=14, fontweight='bold')
#plt.imshow(ap_ssm)

fig = plt.figure()
fig.suptitle('Absolute Interval', fontsize=14, fontweight='bold')
plt.imshow(ai_ssm)

#fig = plt.figure()
#fig.suptitle('Pitch Class', fontsize=14, fontweight='bold')
#plt.imshow(pc_ssm)

fig = plt.figure()
fig.suptitle('Interval Class', fontsize=14, fontweight='bold')
plt.imshow(ic_ssm)

fig = plt.figure()
fig.suptitle('Unordered Pitch Interval', fontsize=14, fontweight='bold')
plt.imshow(upi_ssm)

#print(ic[0])
#print(ap[0])
#print(pc[96])

#numcols = len(thing[0])



#plt.imshow(d_e)
plt.show()
'''


#print(len(pigPiece))



#u = GCD(87,21)
#print(u)
#COMMON DENOMINATOR FINDING
'''a = 87.0
b = 21.0
i = 0
flag = 0
#print(flag)
while flag == 0:
	d = (a*i)/b
	print(d)
	if (d%1 == 0 and i > 0):
		flag = 1
		GCD = (a*i)
	i += 1
print(' ')
print(int(GCD))



'''

'''
##BELOW IS THE CODE FOR HARMONY SYMBOLS

def zerolistmaker(n):
    listofzeros = [0] * n
    return listofzeros


chroma = []
lastChord = None

for i in range(0,len(piece)):
	h = TheFile.getElementsByClass('Part')[0].getElementsByClass('Measure')[piece[i]].getElementsByClass(harmony.ChordSymbol)
	#h = TheFile.getElementsByClass('Part')[0].getElementsByClass('Measure')[i].getElementsByClass(harmony.ChordSymbol)#get the harmony from the measure
	bar = zerolistmaker(12)
	if len(h) == 0:#chech if there are any harmonies in this measure
		h = lastChord#if there aren't use previous harmony
	else:
		h = h
	#print(i)
	#print(h.pitches)
	pitchLength = len(h.pitches)
	#print(pitchLength)
	for j in range (0,pitchLength):
		#print(j)
		a = h.pitches[j].pitchClassString
		if a == 'A':
			a = 10
		#print(a)
		bar[int(a)]=1
	chroma.append(bar)
	lastChord = h
	#print(bar)

numrows = len(chroma)
numcols = len(chroma[0])

d_e = numpy.zeros((numrows,numrows))
for k in range (0,numrows):
	a = numpy.array(chroma[k])
	#print(a)
	for l in range (0,numrows):
		b = numpy.array(chroma[l])
		d = numpy.linalg.norm((a-b), ord = 1)
		d_e[k][l]=d 
		#print(d)
#numrows = len(d_e)
#numcols = len(d_e[0])
#print(d_e)
#print(numrows,numcols)
plt.imshow(d_e)
plt.colorbar(orientation='vertical')
plt.show()'''

'''newFile = []
for i in range(0,len(piece)):
	newFile.append(TheFile.measure(i))
newFile.show()'''