# ---------------------------------------------------------
# These are rules to grab data from IRIS repository and 
# preprocess it according to the same process as Boue et al 2014.
# NOTE: This must be run before all other tests.

grabData:
	python dataPull.py

preprocessData:
	python dailyEnergy.py inter-resuts/dailyEnergy_
	python preprocessing.py 


# ---------------------------------------------------------
# Example of the full workflow for 
# NA = NB = 9 and NuA = NThA = NuB = NThB = 4

traditionalXcorrs9:
	python traditionalXcorrs9.py inter-results/xcorrs9 inter-results/oldXcorrtiming_9.txt

traditionalDBFOnly9:
	python traditionalDBF9.py inter-results/xcorrs9.npz inter-results/serialTraditionalResults4 4 4 4 4

traditionalDBFFull9:
	make traditionalXcorrs9
	make traditionalDBFOnly9


# ---------------------------------------------------------
# Scalability tests for the traditional 

traditionalXCorrsScalingSensors:
	python traditionalXcorrs9.py inter-results/xcorrs9 timingResults/oldXcorrtiming_9.txt
	python traditionalXcorrs18.py inter-results/xcorrs18 timingResults/oldXcorrtiming_18.txt
	python traditionalXcorrs36.py inter-results/xcorrs36 timingResults/oldXcorrtiming_36.txt
	python traditionalXcorrs72.py inter-results/xcorrs72 timingResults/oldXcorrtiming_72.txt

traditionalDBFOnlyScalingSensors:
	python traditionalDBF9.py inter-results/xcorrs9.npz inter-results/serialTraditionalResults4_9 4 4 4 4 timingResults/oldDBFtiming_9_4.txt
	python traditionalDBF18.py inter-results/xcorrs18.npz inter-results/serialTraditionalResults4_18 4 4 4 4 timingResults/oldDBFtiming_18_4.txt
	python traditionalDBF36.py inter-results/xcorrs36.npz inter-results/serialTraditionalResults4_36 4 4 4 4 timingResults/oldDBFtiming_36_4.txt
	python traditionalDBF72.py inter-results/xcorrs72.npz inter-results/serialTraditionalResults4_72 4 4 4 4 timingResults/oldDBFtiming_72_4.txt

traditionalDBFOnlyScalingWithVelsAngles:
	python traditionalDBF9.py inter-results/xcorrs9.npz inter-results/serialTraditionalResults2_9 2 2 2 2 timingResults/oldDBFtiming_9_2.txt
	python traditionalDBF9.py inter-results/xcorrs9.npz inter-results/serialTraditionalResults4_9 4 4 4 4 timingResults/oldDBFtiming_9_4.txt
	python traditionalDBF9.py inter-results/xcorrs9.npz inter-results/serialTraditionalResults8_9 8 8 8 8 timingResults/oldDBFtiming_9_8.txt
	python traditionalDBF9.py inter-results/xcorrs.npz inter-results/serialTraditionalResults16_9 16 16 16 16 timingResults/oldDBFtiming_9_16.txt


newDBFScalingSensors:
	python newDBF9.py inter-results/serialNewResults9 4 4 4 4 timingResults/newtiming_9_4.txt
	python newDBF18.py inter-results/serialNewResults18 4 4 4 4 timingResults/newtiming_18_4.txt
	python newDBF36.py inter-results/serialNewResults36 4 4 4 4 timingResults/newtiming_36_4.txt
	python newDBF72.py inter-results/serialNewResults72 4 4 4 4 timingResults/newtiming_72_4.txt
	python newDBF144.py inter-results/serialNewResults144 4 4 4 4 timingResults/newtiming_144_4.txt
	python newDBF288.py inter-results/serialNewResults288 4 4 4 4 timingResults/newtiming_288_4.txt
	python newDBF576.py inter-results/serialNewResults576 4 4 4 4 timingResults/newtiming_576_4.txt

newDBFScalingWithVelsAngles:
	python newDBF9.py inter-results/serialNewResults2_9 2 2 2 2 timingResults/newtiming_9_2.txt
	python newDBF9.py inter-results/serialNewResults4_9 4 4 4 4 timingResults/newtiming_9_4.txt
	python newDBF9.py inter-results/serialNewResults8_9 8 8 8 8 timingResults/newtiming_9_8.txt
	python newDBF9.py inter-results/serialNewResults16_9 16 16 16 16 timingResults/newtiming_9_16.txt


nVelsAngles = 4
nSensors = 9
plotComparison:
	python plotScalingWithSensors.py timingResults/oldXcorrTiming_ timingResults/oldDBFtiming_ timingResults/newtiming_ ${nVelsAngles} 9 18 36 72 144 288 576
	python plotScalingWithVelsAngles.py timingResults/oldXcorrTiming_ timingResults/oldDBFtiming_ timingResults/newtiming_ ${nSensors} 2 4 8 16