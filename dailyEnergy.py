# Written by Eileen R. Martin

import obspy
import numpy as np
from setupParams import *
import sys


outpath = sys.argv[1]

startWindow = start 
while startWindow < endTime:
	energy = {}
	for station in stationsA+stationsB:

			filename = datapath+station+'_'+channel+'_'+str(startWindow)+'.mseed'
			# read the data for this sensor on this day
			st = obspy.read(filename)
			data = st[0].data
			nSamples = data.size
			## If you're wanting to check out the preprocessing, uncomment these two lines below
			#plt.plot(np.power(data,2))
			#plt.show()

			# calculate the average energy for this sensor on this day
			energy[station] = np.sum(np.power(data,2))/float(nSamples)

	outfileName = outpath+str(startWindow)+".txt"
	outfile = open(outfileName,"w+")
	for station in stationsA+stationsB:
		outfile.write(station+'\t'+str(energy[station])+'\n')
	outfile.close()


	# move on to the next day
	startWindow = startWindow + initWindowSec