# Written by Eileen R. Martin

# ------------------------------------------------------
# This is the rule to install the doublebeamforming package
installDBF:
	pip install .

# ---------------------------------------------------------
# These are rules to grab data from IRIS repository and 
# preprocess it according to the same process as Boue et al 2014.
# NOTE: This must be run before all other tests.

grabData:
	python dataPull.py

preprocessData:
	python dailyEnergy.py test-scripts/inter-results/dailyEnergy_
	python preprocessing.py 


# ---------------------------------------------------------
# Example of the full workflow for 
# NA = NB = 9 and NuA = NThA = NuB = NThB = 4

traditionalXcorrs9:
	python test-scripts/traditionalXcorrs.py test-scripts/inter-results/xcorrs9 test-scripts/inter-results/oldXcorrtiming_9.txt 9

traditionalDBFOnly9:
	python traditionalDBF.py test-scripts/inter-results/xcorrs9.npz test-scripts/inter-results/serialTraditionalResults4 4 4 4 4 9

traditionalDBFFull9:
	make traditionalXcorrs9
	make traditionalDBFOnly9


# ---------------------------------------------------------
# Scalability tests for the traditional cross-correlation
# algorithm in two parts: First, cross-correlations only, 
# second, double beamforming on the cross-correlations. 
# Note that the cross-correlations are written into 
# the inter-results folder as a single file (npz format). 

# Cross-correlations only test of scalability with number of sensors
# (only run after preprocessing the data)
traditionalXCorrsScalingSensors:
	python test-scripts/traditionalXcorrs.py test-scripts/inter-results/xcorrs9 test-scripts/timing-results/oldXcorrtiming_9.txt 9
	python test-scripts/traditionalXcorrs.py test-scripts/inter-results/xcorrs18 test-scripts/timing-results/oldXcorrtiming_18.txt 18
	python test-scripts/traditionalXcorrs.py test-scripts/inter-results/xcorrs36 test-scripts/timing-results/oldXcorrtiming_36.txt 36
	python test-scripts/traditionalXcorrs.py test-scripts/inter-results/xcorrs72 test-scripts/timing-results/oldXcorrtiming_72.txt 72

# Double beamforming only scalability as number of sensors grows
# (only run after calculating cross-correlations scalability with number of sensors)
traditionalDBFOnlyScalingSensors:
	python test-scripts/traditionalDBF.py test-scripts/inter-results/xcorrs9.npz test-scripts/inter-results/serialTraditionalResults4_9 4 4 4 4 test-scripts/timing-results/oldDBFtiming_9_4.txt 9
	python test-scripts/traditionalDBF.py test-scripts/inter-results/xcorrs18.npz test-scripts/inter-results/serialTraditionalResults4_18 4 4 4 4 test-scripts/timing-results/oldDBFtiming_18_4.txt 18
	python test-scripts/traditionalDBF.py test-scripts/inter-results/xcorrs36.npz test-scripts/inter-results/serialTraditionalResults4_36 4 4 4 4 test-scripts/timing-results/oldDBFtiming_36_4.txt 36
	python test-scripts/traditionalDBF.py test-scripts/inter-results/xcorrs72.npz test-scripts/inter-results/serialTraditionalResults4_72 4 4 4 4 test-scripts/timing-results/oldDBFtiming_72_4.txt 72

# Double beamforming only scalability as number of slownesses grows
# (only run after calculating cross-correlations between 9 sensors per patch) 
traditionalDBFOnlyScalingWithVelsAngles:
	python test-scripts/traditionalDBF.py test-scripts/inter-results/xcorrs9.npz test-scripts/inter-results/serialTraditionalResults2_9 2 2 2 2 test-scripts/timing-results/oldDBFtiming_9_2.txt 9
	python test-scripts/traditionalDBF.py test-scripts/inter-results/xcorrs9.npz test-scripts/inter-results/serialTraditionalResults4_9 4 4 4 4 test-scripts/timing-results/oldDBFtiming_9_4.txt 9
	python test-scripts/traditionalDBF.py test-scripts/inter-results/xcorrs9.npz test-scripts/inter-results/serialTraditionalResults8_9 8 8 8 8 test-scripts/timing-results/oldDBFtiming_9_8.txt 9
	python test-scripts/traditionalDBF.py test-scripts/inter-results/xcorrs.npz test-scripts/inter-results/serialTraditionalResults16_9 16 16 16 16 test-scripts/timing-results/oldDBFtiming_9_16.txt 9



# ---------------------------------------------------------
# Scalability tests for the new double beamforming algorithm
# as the number of sensors grows (only run after preprocessing)
newDBFScalingSensors:
	python test-scripts/newDBF.py test-scripts/inter-results/serialNewResults9 4 4 4 4 test-scripts/timing-results/newtiming_9_4.txt 9
	python test-scripts/newDBF.py test-scripts/inter-results/serialNewResults18 4 4 4 4 test-scripts/timing-results/newtiming_18_4.txt 18
	python test-scripts/newDBF.py test-scripts/inter-results/serialNewResults36 4 4 4 4 test-scripts/timing-results/newtiming_36_4.txt 36
	python test-scripts/newDBF.py test-scripts/inter-results/serialNewResults72 4 4 4 4 test-scripts/timing-results/newtiming_72_4.txt 72
	python test-scripts/newDBF.py test-scripts/inter-results/serialNewResults144 4 4 4 4 test-scripts/timing-results/newtiming_144_4.txt 144
	python test-scripts/newDBF.py test-scripts/inter-results/serialNewResults288 4 4 4 4 test-scripts/timing-results/newtiming_288_4.txt 288
	python test-scripts/newDBF.py test-scripts/inter-results/serialNewResults576 4 4 4 4 test-scripts/timing-results/newtiming_576_4.txt 576

# ---------------------------------------------------------
# Scalability tests for the new double beamforming algorithm
# as the number of slownesses grows (only run after preprocessing)
newDBFScalingWithVelsAngles:
	python test-scripts/newDBF.py test-scripts/inter-results/serialNewResults2_9 2 2 2 2 test-scripts/timing-results/newtiming_9_2.txt 9
	python test-scripts/newDBF.py test-scripts/inter-results/serialNewResults4_9 4 4 4 4 test-scripts/timing-results/newtiming_9_4.txt 9
	python test-scripts/newDBF.py test-scripts/inter-results/serialNewResults8_9 8 8 8 8 test-scripts/timing-results/newtiming_9_8.txt 9
	python test-scripts/newDBF.py test-scripts/inter-results/serialNewResults16_9 16 16 16 16 test-scripts/timing-results/newtiming_9_16.txt 9


# ---------------------------------------------------------
# Rules to make scalability plots.

# Make plots of timing as number of sensors per patch grows.
# (only run after all scalability tests as number of sensors grows)
nVelsAngles = 4 # Hold the number of velocities/angles constant as number of sensors grows.
plotComparisonSensors:
	python test-scripts/plotScalingWithSensors.py test-scripts/timing-results/oldXcorrTiming_ test-scripts/timing-results/oldDBFtiming_ test-scripts/timing-results/newtiming_ ${nVelsAngles} 9 18 36 72 144 288 576

# Make plots of timing as number of 
# (only run after scalability tests as number of slownesses grows)
nSensors = 9 # Hold the number of sensors constant as slownesses grows.
plotComparisonsAngleVels:
	python test-scripts/plotScalingWithVelsAngles.py test-scripts/timing-results/oldXcorrTiming_ test-scripts/timing-results/oldDBFtiming_ test-scripts/timing-results/newtiming_ ${nSensors} 2 4 8 16


# -----------------------------------------------------------
# Full workflow to make sensor scaling plots from start to finish
fullSensorScaling:
	make grabData
	make preprocessData
	make traditionalXCorrsScalingSensors
	make traditionalDBFOnlyScalingSensors
	make newDBFScalingSensors
	make plotComparisonSensors

# Full workflow to make slowness scaling plots from start to finish
# (note the grabData and preprocessData steps are redundant if you 
# already ran the full workflow for sensor scaling)
fullSlownessScaling:
	make grabData
	make preprocessData
	make traditionalXCorrs9
	make traditionalDBFOnlyScalingWithVelsAngles
	make newDBFScalingWithVelsAngles
	make plotComparisonsAngleVels


# ----------------------------------------------------------
# cleanup intermediate and final results
clean:
	rm -f inter-results/*.txt
	rm -f inter-results/*.npz
	rm -f timing-results/*.txt
	rm -f fig/*.pdf

# cleanup all pulled data, intermediate and final results
burn:
	rm -f data/*.mseed
	make clean