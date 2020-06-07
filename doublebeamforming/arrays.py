import numpy as np

class arrayPatch:
	"""A single array patch"""
	def __init__(self,stations,u,Th,dtValue,filenames,coordinatesFile):
		self.stations = stations # list of station names (list of strings)
		self.n = len(stations) # number of sensors (integer)
		self.u = u # slownesses of interest (numpy 1D array)
		self.Nu = u.size # number of slownesses of interest (integer)
		self.Th = Th # angles of interest (numpy 1D array)
		self.NTh = Th.size # number of angles of interest (integer)
		self.dtValue = dtValue # time between samples
		self.filenames = filenames # list of file names with input data in mseed format, one file per station
		self.coordinatesFile = coordinatesFile # string of a file name that contains the coordinates of each channel (one row per channel: station name \t latitude \t longitude \n)