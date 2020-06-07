# Written by Eileen R. Martin
#from arrays import *
import numpy as np
import obspy
#from distFromAvg import calcDistFromAvg


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
	# arrayPatchA, the first arrayPatch
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
	stationsA = arrayPatchA.stations
	stationsB = arrayPatchB.stations
	for iA, stationA in enumerate(stationsA):
		print('at station '+stationA) # help keep track of how far you've made it
		filenameA = arrayPatchA.filenames[iA]
		stA = obspy.read(filenameA)
		stASubset = stA[0].data[maxTauID+1:-maxTauID-1]
		nSamp = stA[0].data.size
		nSamplesUsed = stASubset.size

		for iB, stationB in enumerate(stationsB):
			print('\t with station '+stationB)
			filenameB = arrayPatchB.filenames[iB]
			stB = obspy.read(filenameB)

			# do cross-correlation 
			for tau in range(-maxTauID,maxTauID+1):
				stBSubset = stB[0].data[maxTauID+tau:maxTauID+nSamplesUsed+tau]
				xcorrs[iA,iB,tau+maxTauID] = np.inner(stASubset,stBSubset)
	
	return xcorrs


def DBFAfterXcorrs(arrayPatchA, arrayPatchB, xcorrs, Nt):
	# PURPOSE:
	# Calculate the double beamforming transform between array patch A and array patch B based
	# on the cross correlations in xcorrs.
	#
	# INPUTS: 
	# arrayPatchA, the first arrayPatch
	# arrayPatchB, the second arrayPatch (should have same dtValue as A)
	# maxTau, a float representing max time lag of cross-correlations in seconds
	# xcorrs, a numpy array with (num. stations A) x (num. stations B) x (# of time lags including negative, 0 and positive) representing all cross-correlations
	# Nt, an int representing number of starting time lags to consider
	# 
	# OUTPUTS:
	# B, a numpy array with (num. slowness A) x (num. angles A) x (num. slowness B) x (num. angles B) x (num. start times) representing the double beamforming transform

	# get slowness and angle parameters from both array patches
	NuA = arrayPatchA.Nu
	uA = arrayPatchA.u
	NThA = arrayPatchA.NTh
	ThA = arrayPatchA.Th
	NuB = arrayPatchB.Nu
	uB = arrayPatchB.u
	NThB = arrayPatchB.NTh
	ThB = arrayPatchB.Th
	# get stations and filenames from both array patches
	stationsA = arrayPatchA.stations
	stationsB = arrayPatchB.stations
	listOfFilenamesA = arrayPatchA.filenames
	listOfFilenamesB = arrayPatchB.filenames
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

	return B