import obspy
import numpy as np
import scipy.fftpack as ft
from setupParams9 import *



channel = channels[0] # just 'BHZ' for now

startWindow = start
nRejected = 0
while startWindow < endTime: # breaks this into 24 hour windows
	print(startWindow) # so you know progress is being made
	endWindow = startWindow + initWindowSec
	for station in stationsA+stationsB:
		filename = datapath+station+'_'+channel+'_'+str(startWindow)+'.mseed'
		st = obspy.read(filename) # read 24 hours of data

		# response is already removed in data-pull.py

		# calculate the average daily energy 			
		dataAllDay = st[0].data
		nSamplesAllDay = dataAllDay.size
		avgDailyEnergy = np.sum(np.power(dataAllDay,2))/float(nSamplesAllDay)

		# break into 4 hour windows (defined in setupParams.py)
		startSmallWindow = startWindow
		while startSmallWindow < endWindow:

			# grab just this 4 hours of data
			windowSt = st.slice(startSmallWindow,startSmallWindow+windowSec)
			if len(windowSt):
				nSamplesWindow = (windowSt[0].data).size


				# reject if more than 10% of samples are zero
				epsilon = 1e-12
				fracZero = (np.where(np.absolute(windowSt[0].data) < epsilon)[0]).size/float(nSamplesWindow)
				if fracZero > 0.1:
					print('rejecting window '+str(startSmallWindow)+' for sensor '+station+' too many zeros')
					nRejected = nRejected + 1
					windowSt[0].data.fill(0)
				else: # keep otherwise

					# average energy within this window
					avgWindowEnergy = np.sum(np.power(windowSt[0].data,2))/float(nSamplesWindow)
					# compare this window's energy to daily average, reject if energy more than 1.5 times
					if(avgWindowEnergy > 1.5*avgDailyEnergy):
						print('rejecting window '+str(startSmallWindow)+' for sensor '+station+' too high energy')
						nRejected = nRejected + 1
						windowSt[0].data.fill(0)
					else:
						# taper edges
						windowSt[0].taper(0.02,type='cosine',max_length=30.0)

						# whiten from period T = 5 to 150 seconds (1/150 to 1/5 Hz) 
						windowSt[0].filter('bandpass',freqmin=1.0/150.0, freqmax=1.0/5.0) 
						data = windowSt[0].data
						n = int(np.power(2,np.ceil(np.log2(nSamplesWindow))))
						dataSpec = ft.fft(data, n)
						powerSpec = np.sqrt(np.absolute(np.multiply(dataSpec,np.conjugate(dataSpec))))
						smallest = np.percentile(powerSpec,10)
						powerSpec = np.maximum(powerSpec,smallest)
						dataSpec = dataSpec/powerSpec
						windowSt[0].data = np.real(ft.ifft(dataSpec,n)[:nSamplesWindow])


						# clip to remove any remaining peaks bigger than 3.8 times the standard deviation of the window
						std = np.std(windowSt[0].data)
						std38 = 3.8*std
						windowSt[0].data[windowSt[0].data > std38] = std38
						windowSt[0].data[windowSt[0].data < -std38] = -std38	



			outfile = datapath+station+'_'+channel+'_'+str(startSmallWindow)+'_preproc.mseed'
			windowSt.write(outfile)

			# move onto next 4 hour window within this day
			startSmallWindow = startSmallWindow + windowSec

	# move on to next file of data (next day)
	startWindow = startWindow + initWindowSec

print("Total number of windows rejected: "+str(nRejected))
