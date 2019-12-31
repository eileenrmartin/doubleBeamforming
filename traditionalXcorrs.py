# Written by Eileen R. Martin

import obspy
import numpy as np
import time
import sys
from setupParams import *


nSensors = int(sys.argv[3])
sensorReps = int(nSensors/len(stationsA))
stationsA = stationsA*sensorReps # copies of list of stations
filenamesA = [datapath+stationA+'_'+channel+'_'+str(start)+'_preproc.mseed' for stationA in stationsA]
stationsB = stationsB*sensorReps
filenamesB = [datapath+stationB+'_'+channel+'_'+str(start)+'_preproc.mseed' for stationB in stationsB]

# book keeping on time lags
maxTau = 15*60 # max time lag we'll calculate in seconds
dummytrace = obspy.read(filenamesA[0])
dtValue = dummytrace[0].stats.delta # time between samples
maxTauID = int(maxTau/dtValue) # number of time lag indices

startTimeXcorr = time.time()

# array to store cross-correlations
xcorrs = np.zeros((len(stationsA),len(stationsB), 2*maxTauID+1))

# do the cross-correlations one at a time and add into cross-correlations
for iA, stationA in enumerate(stationsA):
	print('at station '+stationA) # just while debugging
	filenameA = filenamesA[iA]
	stA = obspy.read(filenameA)
	stASubset = stA[0].data[maxTauID+1:-maxTauID-1]
	nSamp = stA[0].data.size
	nSamplesUsed = stASubset.size

	for iB, stationB in enumerate(stationsB):
		print('\t with station '+stationB)
		filenameB = filenamesB[iB]
		stB = obspy.read(filenameB)

		# do cross-correlation 
		for tau in range(-maxTauID,maxTauID+1):
			#print(tau)
			#if endID >= nSamp:
			#	print('warning, tau '+str(tau)+' endID '+str(endID))
			stBSubset = stB[0].data[maxTauID+tau:maxTauID+nSamplesUsed+tau]
			xcorrs[iA,iB,tau+maxTauID] = np.inner(stASubset,stBSubset)
		

timingXcorr = time.time()-startTimeXcorr
print("Cross-correlations are complete. \n Time: "+str(timingXcorr))

# write outputs
outfile = sys.argv[1]
np.savez_compressed(outfile, xcorrs=xcorrs)
plaintxt_outfile = outfile+'-plaintxt.txt'
out = open(plaintxt_outfile,'w')
out.write("Cross-correlations time to calculate : "+str(timingXcorr))
out.close()

timingOutfile = sys.argv[2]
out = open(timingOutfile,'w')
out.write("Time to cross correlate two patches with "+str(len(stationsA))+" and "+str(len(stationsB))+" sensors: \n")
out.write(str(timingXcorr))
out.close()