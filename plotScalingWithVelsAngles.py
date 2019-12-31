# Written by Eileen R. Martin 
#
# Use example:
# 	python plotScalingWithVelsAngles.py inter-results/oldXcorrTiming_ inter-results/oldDBFtiming_ inter-results/newtiming_ ${nSensors} 2 4 8 16


import numpy as np 
import matplotlib.pyplot as plt 
import sys


# read inputs about start of filenames
startOldXcorrFiles = sys.argv[1]
startOldDBFFiles = sys.argv[2]
startNewFiles = sys.argv[3]
nSensors = int(sys.argv[4])
nArgs = len(sys.argv)
nAngleVels = []
for i in range(5,nArgs):
	nAngleVels.append(int(sys.argv[i]))


def readOldXcorrTiming(nVelsAngles):
	filename = startOldXcorrFiles+str(nSensors)+'.txt'
	infile = open(filename,'r')
	lines = infile.readlines()
	time = float(lines[1].strip())
	infile.close()
	return time

def readOldDBFTiming(nVelsAngles):
	filename = startOldDBFFiles+str(nSensors)+'_'+str(nVelsAngles)+'.txt'
	infile = open(filename,'r')
	lines = infile.readlines()
	time = float(lines[2].strip())
	infile.close()
	return time

def readNewDBFTiming(nVelsAngles):
	filename = startNewFiles+str(nSensors)+'_'+str(nVelsAngles)+'.txt'
	infile = open(filename,'r')
	lines = infile.readlines()
	phase1line = lines[2]
	ph1words = phase1line.split()
	phase1Time = float(ph1words[3].strip())
	phase2line = lines[3]
	ph2words = phase2line.split()
	phase2Time = float(ph2words[3].strip())
	return (phase1Time, phase2Time)


# read the timings for each test
timeOldXCorr = []
timeOldDBF = []
timeNewPhase1 = []
timeNewPhase2 = []
for nVA in nAngleVels:
	timeOldXCorr.append(readOldXcorrTiming(nVA))
	timeOldDBF.append(readOldDBFTiming(nVA))
	(phase1, phase2) = readNewDBFTiming(nVA)
	timeNewPhase1.append(phase1)
	timeNewPhase2.append(phase2)
# turn lists into arrays 
nAngleVels = np.asarray(nAngleVels)
timeOldXCorr = np.asarray(timeOldXCorr)
timeOldDBF = np.asarray(timeOldDBF)
timeNewPhase1 = np.asarray(timeNewPhase1)
timeNewPhase2 = np.asarray(timeNewPhase2)

minVal = min([np.min(timeOldXCorr), np.min(timeOldDBF), np.min(timeNewPhase1), np.min(timeNewPhase2)])
maxVal = max([np.max(timeOldXCorr), np.max(timeOldDBF), np.max(timeNewPhase1), np.max(timeNewPhase2)])

# scatter plot
ax = plt.subplot(111)
ax.scatter(nAngleVels,timeOldXCorr,c='r',marker='o',s=40,label='old corrs.')
ax.scatter(nAngleVels,timeOldDBF,c='g',marker='h',s=40,label='old DBF')
ax.scatter(nAngleVels,timeNewPhase1,c='b',marker='*',s=40,label='new phase 1')
ax.scatter(nAngleVels,timeNewPhase2,c='k',marker='v',s=40,label='new phase 2')
ax.legend(loc='lower right')
ax.set_ylim(minVal*.9,maxVal*1.1)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('number of angles = number of velocities',fontsize=16)
ax.set_ylabel('time (s)',fontsize=16)
ax.set_title('Scaling w. no. angles & velocities per patch',fontsize=20)
plt.tight_layout()
plt.savefig('fig/scalingWithVelsAngles.pdf')
plt.clf()
