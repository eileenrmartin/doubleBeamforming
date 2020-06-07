# Written by Eileen R. Martin 
#
# Use example:
# plotScalingWithSensors.py inter-results/oldXcorrTiming_ inter-results/oldDBFtiming_ inter-results/newtiming_ ${nVelsAngles} 9 18 36 72

import numpy as np 
import matplotlib.pyplot as plt 
import sys
import os.path

# read inputs about start of filenames
startOldXcorrFiles = sys.argv[1]
startOldDBFFiles = sys.argv[2]
startNewFiles = sys.argv[3]
nVelsAngles = int(sys.argv[4])
nArgs = len(sys.argv)
nSensorsPerPatch = []
for i in range(5,nArgs):
	nSensorsPerPatch.append(int(sys.argv[i]))

def readOldXcorrTiming(nSensors):
	filename = startOldXcorrFiles+str(nSensors)+'.txt'
	if os.path.exists(filename):
		infile = open(filename,'r')
		lines = infile.readlines()
		time = float(lines[1].strip())
		infile.close()
		return time
	else: 
		return -1

def readOldDBFTiming(nSensors):
	filename = startOldDBFFiles+str(nSensors)+'_'+str(nVelsAngles)+'.txt'
	if os.path.exists(filename):
		infile = open(filename,'r')
		lines = infile.readlines()
		time = float(lines[2].strip())
		infile.close()
		return time
	else:
		return -1

def readNewDBFTiming(nSensors):
	filename = startNewFiles+str(nSensors)+'_'+str(nVelsAngles)+'.txt'
	if os.path.exists(filename):
		infile = open(filename,'r')
		lines = infile.readlines()
		phase1line = lines[2]
		ph1words = phase1line.split()
		phase1Time = float(ph1words[3].strip())
		phase2line = lines[3]
		ph2words = phase2line.split()
		phase2Time = float(ph2words[3].strip())
		return (phase1Time, phase2Time)
	else:
		return (-1,-1)

# read the timings for each test
timeOldXCorr = []
timeOldDBF = []
timeNewPhase1 = []
timeNewPhase2 = []
for nSensors in nSensorsPerPatch:
	time = readOldXcorrTiming(nSensors)
	if time > 0:
		timeOldXCorr.append(time)
	time = readOldDBFTiming(nSensors)
	if time > 0:
		timeOldDBF.append(time)
	(phase1, phase2) = readNewDBFTiming(nSensors)
	if phase1 > 0 and phase2 > 0:
		timeNewPhase1.append(phase1)
		timeNewPhase2.append(phase2)
# turn lists into arrays 
nSensors = np.asarray(nSensorsPerPatch)
timeOldXCorr = np.asarray(timeOldXCorr)
timeOldDBF = np.asarray(timeOldDBF)
timeNewPhase1 = np.asarray(timeNewPhase1)
timeNewPhase2 = np.asarray(timeNewPhase2)

minVal = min([np.min(timeOldXCorr), np.min(timeOldDBF), np.min(timeNewPhase1), np.min(timeNewPhase2)])
maxVal = max([np.max(timeOldXCorr), np.max(timeOldDBF), np.max(timeNewPhase1), np.max(timeNewPhase2)])
print(timeOldXCorr)
print(timeOldDBF)
print(timeNewPhase1)
print(timeNewPhase2)

# scatter plot
ax = plt.subplot(111)
ax.scatter(nSensors[:timeOldXCorr.size],timeOldXCorr,c='r',marker='o',s=40,label='old corrs.')
ax.scatter(nSensors[:timeOldDBF.size],timeOldDBF,c='g',marker='h',s=40,label='old DBF')
ax.scatter(nSensors[:timeNewPhase1.size],timeNewPhase1,c='b',marker='*',s=40,label='new phase 1')
ax.scatter(nSensors[:timeNewPhase2.size],timeNewPhase2,c='k',marker='v',s=40,label='new phase 2')
ax.legend(loc='upper left')
ax.set_ylim(minVal*.9,maxVal*1.1)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('number of sensors',fontsize=16)
ax.set_ylabel('time (s)',fontsize=16)
ax.set_title('Scaling with sensors',fontsize=20)
plt.tight_layout()
plt.savefig('fig/scalingWithSensor.pdf')
plt.clf()


