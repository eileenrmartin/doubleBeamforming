# Written by Eileen R. Martin

import obspy
from obspy.clients.fdsn import Client
from setupParams import *



## If you're trying to look up some new stations to use, 
## The following two lines can be helpful.
#inventory = client.get_stations(network=network, station="Z*A",starttime=start,endtime=end, level="channel")
#print(inventory)

fourFrqCorners = [0.001,1.0/150.0, 15, 20] # frquency filter
startWindow = start 
while startWindow < endTime:
	for station in stationsA:
		stZ = client.get_waveforms(network, station, "*", channel, startWindow, startWindow+initWindowSec, attach_response=True)
		print(stZ) # just so you know progress is being made
		stZ.remove_response(pre_filt=fourFrqCorners, output="VEL")
		stZ.write(datapath+station+'_'+channel+'_'+str(startWindow)+'.mseed',format='MSEED')
	for station in stationsB:
		stZ = client.get_waveforms(network, station, "*", channel, startWindow, startWindow+initWindowSec, attach_response=True)
		print(stZ) # just so you know progress is being made
		stZ.remove_response(pre_filt=fourFrqCorners, output="VEL")
		stZ.write(datapath+station+'_'+channel+'_'+str(startWindow)+'.mseed',format='MSEED')
	# move on to the next time window
	startWindow = startWindow+initWindowSec