## Subdirectory structure:
* __init__.py, used to build the double beamforming package by describing contents of this directory
* README.md, this
* arrays.py, definition of arrayPatch class (describes a collection of nearby sensors in a single patch, and 2 arrayPatch objects are used in double beamforming)
* distFromAvg.py, function to calculate each sensor's distance in two dimensions from the center of an array (like x-distance, y-distance)
* traditionalXcorrsDBF.py, functions to calculate all time-domain cross-correlations between sensors in two array patches, then do double beamforming on the cross-correlations
* newDBFFuncs.py, functions to calculate double beamforming transform between two array patches using algorithm 1 from "A Linear Algorithm for Ambient Seismic Noise Double Beamforming Without Explicit Crosscorrelations"
