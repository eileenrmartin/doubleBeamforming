# Written by Eileen R. Martin

import obspy
import numpy as np
import time
import sys
from setupParams import *
import doublebeamforming as dbf


# names of files and sensors in each file for scalability tests
nSensors = int(sys.argv[8])
sensorReps = int(nSensors/len(stationsA))
stationsA = stationsA*sensorReps # copies of list of stations, just for scalability testing purposes
listOfFilenamesA = [datapath+stationA+'_'+channel+'_'+str(start)+'.mseed' for stationA in stationsA]
stationsB = stationsB*sensorReps
listOfFilenamesB = [datapath+stationB+'_'+channel+'_'+str(start)+'.mseed' for stationB in stationsB]

# read arrays that store cross-correlations
xcorrFile = sys.argv[1]
loadedArrs = np.load(xcorrFile)
xcorrs = loadedArrs['xcorrs'] # actual cross correlations (sensor A, sensor B, time lag)

# for output
outfile = sys.argv[2]

# book keeping on time between samples
dummytraceA = obspy.read(listOfFilenamesA[0])
dummytraceB = obspy.read(listOfFilenamesB[0])
dtValueA = dummytraceA[0].stats.delta # time between samples for array A
dtValueB = dummytraceB[0].stats.delta # time between samples for array B (should match A)

# For double beamforming, need to first select arrays of slowness, angle and start time values of interest
NuA = int(sys.argv[3]) # number of slownesses on A array
uA = 1/np.linspace(100,2500,num=NuA)
NuB = int(sys.argv[4]) # number of slownesses on B array
uB = 1/np.linspace(100,2500,num=NuB)
# arrays of theta angles of interest
NThA = int(sys.argv[5]) # 6 degrees per subset on A
ThA = np.linspace(-np.pi/2,np.pi/2,num=NThA)
NThB = int(sys.argv[6]) # 6 degrees per subset on B
ThB = np.linspace(-np.pi/2,np.pi/2,num=NThB)

# create arrayPatch objects
arrayA = dbf.arrayPatch(stationsA, uA, ThA, dtValueA, filenamesA)
arrayB = dbf.arrayPatch(stationsB, uB, ThB, dtValueB, filenamesB)

#start timing
startDBFTime = time.time()

# actually do the double beamforming transofrm
B = dbf.DBFAfterXcorrs(arrayPatchA, arrayPatchB, xcorrs, Nt)

# end timing
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