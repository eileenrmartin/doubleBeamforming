## Subdirectory structure:
* /data, a subdirectory where all data that's pulled, and all data after preprocessing go for this example
* /fig, a subdirectory where figures produced by the tests go
* /inter-results, a subdirectory where intermediate energy and beamforming results are written
* /timing-results, a subdirectory where all timing results are written
* setupParams.py, script specifying which US Array data to pull
* dataPull.py, script to pull that data to your local computer
* dailyEnergy.py, script to calculate energy in windows of time (so you can go back and check which windows were rejected)
* preprocessing.py, script to preprocess the data that were pulled 
* traditionalXcorrs.py, script to perform the cross-correlations on this test example (1st part of old double beamforming algorithm)
* traditionalDBF.py, script to perform double beamforming transform on cross-correlations (2nd part of old double beamforming algorithm)
* newDBF.py, script to run the new double beamforming algorithm on this test example
* plotScalingWithSensors.py, script to read timing results and plot scalability with many sensors
* plotScalingWithVelsAngles.py, script to read 