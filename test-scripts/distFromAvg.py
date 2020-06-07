# Written by Eileen R. Martin

import math
import numpy as np
import obspy

def calcDistFromAvg(listOfFilenames, fileWithCoords=''):
	# Input: list of files, each containing data for one seismic sensor in a patch. 
	# If stats.coordinates is mising from files, then read lat and long from
	# a text file (0th column name, first column latitude, 2nd column longitude).
	# Note: this just does distance conversion alng the surface, and is an approximation. 
	# Return: 2D numpy array storing distance in meters of each sensor from centroid of array of sensors.

	distFromAvg = np.zeros((len(listOfFilenames),2)) # will be returned with distances in meters
	latLong = np.zeros((len(listOfFilenames),2)) # will store latitudes and longitudes of each sensor in radians (intermediate need)

	# read the latitude and longitude coordinates for each sensor
	if fileWithCoords: # read from a file with coordinates (seems necessary with the test dataset)
		infile = open(fileWithCoords,"r")
		allLines = infile.readlines()
		for id,line in enumerate(allLines):
			nameLatLong = line.split()
			latString = (nameLatLong[1]).strip()
			latLong[id,0] = math.radians(float(latString))
			longString = (nameLatLong[2]).strip()
			latLong[id,1] = math.radians(float(longString))
	else: # read from the data file (preferred)
		for id,filename in enumerate(listOfFilenames):
			st = obspy.read(filename) 
			latLong[id,0] = math.radians(st[0].stats.coordinates.latitude)
			latLong[id,1] = math.radians(st[0].stats.coordinates.longitude)
	
	avgLatLong = np.mean(latLong,axis=0) # [avg latitude, avg longitude]
	earthRadiusInMeters = 6371000
	avgLatCircumference = np.absolute(earthRadiusInMeters*2*np.pi*np.cos(avgLatLong[0]))# circumference of straight across circle on earth

	for id in range(len(listOfFilenames)):
		# apply Haversine distance formula https://en.wikipedia.org/wiki/Haversine_formula
		latDiff = latLong[id,0] - avgLatLong[0]
		distFromAvg[id,0] = earthRadiusInMeters*latDiff
		longDiff = latLong[id,1] - avgLatLong[1]
		distFromAvg[id,1] = avgLatCircumference*longDiff/(2*np.pi)

	# distFromAvg is numpy array that is (# of sensors, 2) 
	# 0th column is latitude, 1st column is longitude
	return distFromAvg