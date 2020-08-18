# Written by Eileen R. Martin

import obspy
import numpy as np
import time
import sys
import scipy.fftpack as ft
from setupParams import *
import doublebeamforming as dbf


# just the first set of filenames (first window)
def filenameGenerator(stationName,startObspyTime):
	return datapath+stationName+'_'+channel+'_'+str(startObspyTime)+'_preproc.mseed'

nSensors = int(sys.argv[7])
sensorReps = int(nSensors/len(stationsA))
stationsA = stationsA*sensorReps # copies of list of stations
filenamesA = [datapath+stationA+'_'+channel+'_'+str(start)+'_preproc.mseed' for stationA in stationsA]
stationsB = stationsB*sensorReps
filenamesB = [datapath+stationB+'_'+channel+'_'+str(start)+'_preproc.mseed' for stationB in stationsB]

# book keeping on time lags
maxTau = 15*60 # max time lag we'll calculate in seconds
dummytrace = obspy.read(filenamesA[0])
dtValue = dummytrace[0].stats.delta # time between samples
nSampsPerTrace = dummytrace[0].data.size
samplesPerSec = 1.0/dtValue
print('samples per second '+str(samplesPerSec))
print('nSampsPerTrace '+str(nSampsPerTrace))
Nyquist = samplesPerSec/2
maxTauID = int(maxTau/dtValue) # number of time lag indices

startTimeNewDBF = time.time()



# need locations of stations (in meters relative to center of each array)
locationsA = dbf.calcDistFromAvg(filenamesA,'test-scripts/data/coordinatesA'+str(nSensors)+'.txt') # no. of sensors in A x 2 
locationsB = dbf.calcDistFromAvg(filenamesB,'test-scripts/data/coordinatesB'+str(nSensors)+'.txt') # no. of sensors in B x 2


# bookkeeping frequencies
nTrunc = int(np.power(2,np.floor(np.log2(nSampsPerTrace)))) # will be truncated for much faster fft
nFrq = nTrunc # number of frequencies after fourier transform
frqs = np.zeros(nFrq)
frqs[:1+int(nFrq/2)] = np.arange(1+int(nFrq/2))*Nyquist/(1+nFrq/2)
frqs[1+int(nFrq/2):] = np.flipud(-1*np.arange(1,int(nFrq/2))*Nyquist/(1+nFrq/2))

# For double beamforming, create arrays of slowness, angle and start time values
NuA = int(sys.argv[2]) # number of slownesses on A array
uA = 1/np.linspace(100,2500,num=NuA)
NuB = int(sys.argv[3]) # number of slownesses on B array
uB = 1/np.linspace(100,2500,num=NuB)
# arrays of theta angles of interest
NThA = int(sys.argv[4]) # 6 degrees per subset on A
ThA = np.linspace(-np.pi/2,np.pi/2,num=NThA)
NThB = int(sys.argv[5]) # 6 degrees per subset on B
ThB = np.linspace(-np.pi/2,np.pi/2,num=NThB)

# array patch A setup
slownessesA = np.zeros((NuA,NThA,2)) # no. of slownesses x no of angles x 2
slownessesA[:,:,0] = np.outer(uA,np.cos(ThA))
slownessesA[:,:,1] = np.outer(uA,np.sin(ThA))
# array patch B setup
slownessesB = np.zeros((NuB,NThB,2)) # no. of slownesses x no of angles x 2
slownessesB[:,:,0] = np.outer(uB,np.cos(ThB))
slownessesB[:,:,1] = np.outer(uB,np.sin(ThB))



# just process first 4 hour window (if you want to do all windows, just loop over as in preprocessing.py and increase startWindow by 4 hours each loop)
startWindow = start


# ----------------------------phase 1-------------------

##### Note: Potential for easy parallelism calculating RA and RB at same time ########
startTimePhase1 = time.time()

# array patch A calculations
RA = dbf.phase1(stationsA,frqs,nTrunc,locationsA,slownessesA,filenameGenerator,startWindow)

print('done with phase 1 patch A at time '+str(time.time()-startTimePhase1))

print('starting phase 1 patch B')

# array patch B calculations
RB = dbf.phase1(stationsB,frqs,nTrunc,locationsB,slownessesB,filenameGenerator,startWindow)

timingPhase1 = time.time() - startTimePhase1
print("Phase 1 is complete. \n Time phase 1: "+str(timingPhase1))


# ----------------------------phase 2---------------------
startTimePhase2 = time.time()

B = dbf.phase2(RA,RB,Nt)

timingPhase2 = time.time() - startTimePhase2
print("Phase 2 is complete. \n Time phase 2: "+str(timingPhase2))



timingNewDBF = time.time()-startTimeNewDBF
print('Double Beamforming is complete. \n Total Time : '+str(timingNewDBF))




# ------------------write outputs, timing-----------------
outfile = sys.argv[1]
np.savez_compressed(outfile, B=B, uA=uA, ThA=ThA, uB=uB, ThB=ThB)
plaintxt_outfile = outfile+'-plaintxt.txt'
out = open(plaintxt_outfile,'w')
out.write(outfile+' contains 6 arrays calculated with traditional double beamforming: \n B the 5D double beamforming results (vel A, theta A, vel B, theta B, t) \n uA a 1D array of A slownesses (same order as B) \n ThA a 1D array of A angles (same order as B) \n uB a 1D array of B slownesses (same order as B) \n ThB a 1D array of B angles (same order as B) \n t a 1D array of start times')
out.close()

outfileTiming = sys.argv[6]
out = open(outfileTiming,'w')
out.write("Time to do double beamforming with "+str(len(stationsA))+" and "+str(len(stationsB))+" sensors, \n")
out.write("NuA "+str(NuA)+", NuB "+str(NuB)+", NThA "+str(NThA)+", NThB "+str(NThB)+" \n")
out.write("Phase 1 : "+str(timingPhase1)+'\n')
out.write("Phase 2 : "+str(timingPhase2))
out.close()
