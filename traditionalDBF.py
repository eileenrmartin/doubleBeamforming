import obspy
import numpy as np
import time
import sys
from distFromAvg import calcDistFromAvg
from setupParams import *



nSensors = int(sys.argv[8])
sensorReps = int(nSensors/len(stationsA))
stationsA = stationsA*sensorReps # copies of list of stations
listOfFilenamesA = [datapath+stationA+'_'+channel+'_'+str(start)+'.mseed' for stationA in stationsA]
stationsB = stationsB*sensorReps
listOfFilenamesB = [datapath+stationB+'_'+channel+'_'+str(start)+'.mseed' for stationB in stationsB]
nA = len(stationsA)
nB = len(stationsB)

# read arrays that store cross-correlations
xcorrFile = sys.argv[1]
loadedArrs = np.load(xcorrFile)
xcorrs = loadedArrs['xcorrs'] # actual cross correlations (sensor A, sensor B, time lag)
nTimesXcorrs = xcorrs.shape[2]
# starting time lag IDs

t = np.arange(int(nTimesXcorrs/2)-int(Nt/2),int(nTimesXcorrs/2)+int(Nt/2))
Nt = t.size # adjust in case of int/float rounding

# for output
outfile = sys.argv[2]

# book keeping on time lags
maxTau = 15*60 # max time lag we'll calculate in seconds
dummytrace = obspy.read(listOfFilenamesA[0])
dtValue = dummytrace[0].stats.delta # time between samples

# For double beamforming, create arrays of slowness, angle and start time values
NuA = int(sys.argv[3]) # number of slownesses on A array
uA = 1/np.linspace(100,2500,num=NuA)
NuB = int(sys.argv[4]) # number of slownesses on B array
uB = 1/np.linspace(100,2500,num=NuB)
# arrays of theta angles of interest
NThA = int(sys.argv[5]) # 6 degrees per subset on A
ThA = np.linspace(-np.pi/2,np.pi/2,num=NThA)
NThB = int(sys.argv[6]) # 6 degrees per subset on B
ThB = np.linspace(-np.pi/2,np.pi/2,num=NThB)
t = np.arange(int(nTimesXcorrs/2)-int(Nt/2),int(nTimesXcorrs/2)+int(Nt/2))
Nt = t.size # adjust in case of int/float rounding
startDBFTime = time.time()

# 5D array to store beamforming values
B = np.zeros((NuA, NThA, NuB, NThB, Nt)) 
# Note: different order from Boue et al 2013 ordering of variables.
# Order is velocity A, theta A, velocity B, theta B, start time

# need locations of stations (in meters relative to center of each array)
locationsA = calcDistFromAvg(listOfFilenamesA,'data/coordinatesA'+str(nSensors)+'.txt') # no. of sensors in A x 2 
locationsB = calcDistFromAvg(listOfFilenamesB,'data/coordinatesB'+str(nSensors)+'.txt') # no. of sensors in B x 2

# actually do the double beamforming on the cross-correlations
for iA, stationA in enumerate(stationsA):
	print('station '+stationA)
	for iUA in range(NuA): # for each velocity u A 
		print('\t iUA '+str(iUA))
		for iThA in range(NThA): # for each theta A angle
			print('\t \t iThA '+str(iThA))
			thisUA = np.array([uA[iUA]*np.cos(ThA[iThA]), uA[iUA]*np.sin(ThA[iThA])])

			lagsASeconds = locationsA[:,0] * thisUA[0] + locationsA[:,1] * thisUA[1]
			lagsA = lagsASeconds / dtValue
			lagsA = lagsA.astype(int)

			for iUB in range(NuB): # for each velocity in B
				for iThB in range(NThB): # for each theta B angle
					thisUB = np.array([uB[iUB]*np.cos(ThB[iThB]), uB[iUB]*np.sin(ThB[iThB])])

					lagsBSeconds = locationsB @ thisUB
					lagsB = lagsBSeconds / dtValue
					lagsB = lagsB.astype(int)

					for iT in range(Nt):
						# starting indices for all B sensors cross-correlations with this A sensor
						tIDs = np.mod(t[iT] - lagsA + lagsB, nTimesXcorrs) # mod in case you run off edge
						laggedXcorrA = xcorrs[iA,np.arange(nB),tIDs]# grabs one correlation value per sensor at proper lag
						B[iUA,iThA,iUB,iThB,iT] = np.sum(laggedXcorrA) # stack along given slant
		

# normalize
B = B/(len(stationsA)*len(stationsB))
timingDBF = time.time() - startDBFTime
print("Double Beamforming is complete. \n Time: "+str(timingDBF))


# save the double beamforming results and text description
np.savez_compressed(outfile, B=B, uA=uA, ThA=ThA, uB=uB, ThB=ThB, times=t)
plaintxt_outfile = outfile+'-plaintxt.txt'
out = open(plaintxt_outfile,'w')
out.write(outfile+' contains 6 arrays calculated with traditional double beamforming: \n B the 5D double beamforming results (vel A, theta A, vel B, theta B, t) \n uA a 1D array of A slownesses (same order as B) \n ThA a 1D array of A angles (same order as B) \n uB a 1D array of B slownesses (same order as B) \n ThB a 1D array of B angles (same order as B) \n t a 1D array of start times')
out.close()

timingOutfilename = sys.argv[7]
out = open(timingOutfilename,'w')
out.write("Time to do double beamforming with "+str(len(stationsA))+" and "+str(len(stationsB))+" sensors, \n")
out.write("NuA "+str(NuA)+", NuB "+str(NuB)+", NThA "+str(NThA)+", NThB "+str(NThB)+" \n")
out.write(str(timingDBF))
out.close()