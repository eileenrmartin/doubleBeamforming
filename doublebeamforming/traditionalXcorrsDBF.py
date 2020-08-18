# Written by Eileen R. Martin

import numpy as np
import obspy
from distFromAvg import calcDistFromAvg


def xCorrsAcrossArrays(arrayPatchA, arrayPatchB, maxTau):
	# PURPOSE:
	# Calculate cross-correlations between all sensors in 
	# arrayPatchA with all sensors in arrayPatchB between -maxTau
	# and +maxTau seconds (assuming the files all cover the same time 
	# window). Note: If you have many separate time windows split up 
	# by separate files, create a new arrayPatch for each time window 
	# and call this for each time window (averaging as you go along).
	#
	# INPUTS: 
	# arrayPatchA, the first arrayPatch (defined in arrays.py)
	# arrayPatchB, the second arrayPatch (should have same dtValue as A)
	# maxTau, a float representing max time lag of cross-correlations in seconds
	# OUTPUT:
	# xcorrs, a numpy array with (num. stations A) x (num. stations B) x (# of time lags including negative, 0 and positive)

	# check if dt are same
	dtValue = arrayPatchA.dtValue
	BdtValue = arrayPatchB.dtValue
	if(abs(dtValue-BdtValue) > 0.00001*abs(dtValue)):
		print("ERROR in xCorrsAcrossArrays: dtValue did not match between patches. Interpolate your data so they match.")
		return 


	# array to store cross-correlations
	maxTauID = int(maxTau/dtValue)
	xcorrs = np.zeros((arrayPatchA.n,arrayPatchB.n, 2*maxTauID+1))

	# do the cross-correlations one at a time and add into cross-correlations
	stationsA = arrayPatchA.stations # list of all station names in array patch A (def. in arrays.py)
	stationsB = arrayPatchB.stations # list of all station names in array patch B (def. in arrays.py)
	for iA, stationA in enumerate(stationsA):
		print('at station '+stationA) # help keep track of how far you've made it
		filenameA = arrayPatchA.filenames[iA] # check the filename for this array A station's data
		stA = obspy.read(filenameA) # read data for this station in A
		stASubset = stA[0].data[maxTauID+1:-maxTauID-1] # data of interest for a given time lag range
		nSamplesUsed = stASubset.size # number of time samples actually being used in calculating the cross-correlation

		for iB, stationB in enumerate(stationsB):
			print('\t with station '+stationB)
			filenameB = arrayPatchB.filenames[iB] # check the filename for this array B station's data
			stB = obspy.read(filenameB) # read data for this station in B

			# do cross-correlation, which is a bunch of inner products in time domain
			for tau in range(-maxTauID,maxTauID+1):
				stBSubset = stB[0].data[maxTauID+tau:maxTauID+nSamplesUsed+tau] # time lagged compared to stASubset by tau time samples
				xcorrs[iA,iB,tau+maxTauID] = np.inner(stASubset,stBSubset) 
	
	return xcorrs


def DBFAfterXcorrs(arrayPatchA, arrayPatchB, xcorrs, Nt):
	# PURPOSE:
	# Calculate the double beamforming transform between array patch A and array patch B based
	# on the cross correlations in xcorrs.
	#
	# INPUTS: 
	# arrayPatchA, the first arrayPatch (defind in arrays.py)
	# arrayPatchB, the second arrayPatch (should have same dtValue as A)
	# maxTau, a float representing max time lag of cross-correlations in seconds
	# xcorrs, a numpy array with (num. stations A) x (num. stations B) x (# of time lags including negative, 0 and positive) representing all cross-correlations
	# Nt, an int representing number of starting time lags to consider
	# 
	# OUTPUTS:
	# B, a numpy array with (num. slowness A) x (num. angles A) x (num. slowness B) x (num. angles B) x (num. start times) representing the double beamforming transform

	# get slowness and angle parameters from both array patches
	NuA = arrayPatchA.Nu # no. slowness A
	uA = arrayPatchA.u # slownesses A
	NThA = arrayPatchA.NTh # no. angles A
	ThA = arrayPatchA.Th # angles A
	NuB = arrayPatchB.Nu # no. slowness B
	uB = arrayPatchB.u # slownesses B
	NThB = arrayPatchB.NTh # no angles B
	ThB = arrayPatchB.Th # angles B
	# get stations and filenames from both array patches
	stationsA = arrayPatchA.stations # list of station names A
	stationsB = arrayPatchB.stations # list of station names B
	nA = len(stationsA)
	nB = len(stationsB)
	listOfFilenamesA = arrayPatchA.filenames # list of files containing relevant data A
	listOfFilenamesB = arrayPatchB.filenames # list of files containing relevant data B
	# need locations of stations (in meters relative to center of each array)
	locationsA = calcDistFromAvg(listOfFilenamesA,arrayPatchA.coordinatesFile) # no. of sensors in A x 2 
	locationsB = calcDistFromAvg(listOfFilenamesB,arrayPatchB.coordinatesFile) # no. of sensors in B x 2


	# check if dt are same
	dtValue = arrayPatchA.dtValue
	BdtValue = arrayPatchB.dtValue
	if(abs(dtValue-BdtValue) > 0.00001*abs(dtValue)):
		print("ERROR in DBFAfterXcorrs: dtValue did not match between patches. Interpolate your data so they match.")
		return 

	# figure out how many time lags there are
	nTimesXcorrs = xcorrs.shape[2]
	# starting time lag IDs
	t = np.arange(int(nTimesXcorrs/2)-int(Nt/2),int(nTimesXcorrs/2)+int(Nt/2))
	Nt = t.size # adjust in case of int/float rounding


	# create 5D array to store beamforming values
	B = np.zeros((NuA, NThA, NuB, NThB, Nt)) 
	# Note: different order from Boue et al 2013 ordering of variables.
	# Order is velocity A, theta A, velocity B, theta B, start time

	# actually do the double beamforming on the cross-correlations
	for iA, stationA in enumerate(stationsA):
		print('station '+stationA) 
		for iUA in range(NuA): # for each velocity u A 
			print('\t iUA '+str(iUA))
			for iThA in range(NThA): # for each theta A angle
				print('\t \t iThA '+str(iThA))
				# calculate slowness vector of interest for array A
				thisUA = np.array([uA[iUA]*np.cos(ThA[iThA]), uA[iUA]*np.sin(ThA[iThA])])
				# calculate lags predicted for this slowness vector on A
				lagsASeconds = locationsA[:,0] * thisUA[0] + locationsA[:,1] * thisUA[1]
				lagsA = lagsASeconds / dtValue
				lagsA = lagsA.astype(int)

				for iUB in range(NuB): # for each velocity in B
					for iThB in range(NThB): # for each theta B angle
						# calculate slowness vector of interest for array B
						thisUB = np.array([uB[iUB]*np.cos(ThB[iThB]), uB[iUB]*np.sin(ThB[iThB])])
						# calculate lags predicted for this slowness vector on B
						lagsBSeconds = locationsB @ thisUB
						lagsB = lagsBSeconds / dtValue
						lagsB = lagsB.astype(int)

						for iT in range(Nt):
							# starting indices for all B sensors cross-correlations with this A sensor
							tIDs = np.mod(t[iT] - lagsA + lagsB, nTimesXcorrs) # mod in case you run off edge
							laggedXcorrA = xcorrs[iA,np.arange(nB),tIDs]# grabs one correlation value per sensor at proper lag
							B[iUA,iThA,iUB,iThB,iT] = np.sum(laggedXcorrA) # stack along given slant
		

	# normalize value by number of stations 
	B = B/(len(stationsA)*len(stationsB))

	return B