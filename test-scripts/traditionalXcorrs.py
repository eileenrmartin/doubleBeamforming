# Written by Eileen R. Martin

import obspy
import numpy as np
import time
import sys
from setupParams import * # to get stations, filenames, times
import doublebeamforming as dbf

# names of files and sensors in each file
nSensors = int(sys.argv[3])
sensorReps = int(nSensors/len(stationsA))
stationsA = stationsA*sensorReps # copies of list of stations, just for scalability testing purposes
filenamesA = [datapath+stationA+'_'+channel+'_'+str(start)+'_preproc.mseed' for stationA in stationsA]
stationsB = stationsB*sensorReps
filenamesB = [datapath+stationB+'_'+channel+'_'+str(start)+'_preproc.mseed' for stationB in stationsB]


# book keeping on time lags and time sampling for both arrays
maxTau = 15*60 # max time lag we'll calculate in seconds
dummytraceA = obspy.read(filenamesA[0])
dummytraceB = obspy.read(filenamesB[0])
dtValueA = dummytraceA[0].stats.delta # time between samples, array A
dtValueB = dummytraceB[0].stats.delta # time between samples, array B (should match A)

# create arrayPatch objects
dummyU = np.array([0]) # dummy array of slownesses, don't use in this part of example
dummyTh = np.array([0]) # dummy array of angles, don't use in this part of example
arrayA = dbf.arrayPatch(stationsA, dummyU, dummyTh, dtValueA, filenamesA, 'data/coordinatesA'+str(nSensors)+'.txt')
arrayB = dbf.arrayPatch(stationsB, dummyU, dummyTh, dtValueB, filenamesB, 'data/coordinatesB'+str(nSensors)+'.txt')

# start timing 
startTimeXcorr = time.time()

# actually do the cross-correlations for this set of files
xcorrs = dbf.xCorrsAcrossArrays(arrayA, arrayB, maxTau)

# end timing
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