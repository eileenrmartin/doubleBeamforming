# doubleBeamforming
code for traditional method and fast method for double beamforming of ambient seismic noise, with example workflow on US Array data. 

##To cite: 
**preprint to be posted soon**, until the preprint is up: E.R. Martin, "Scalable Seismic Acquisition and Algorithms" abstract from the 2019 International Conference for Engineering Geophysics. 

## Start with the Makefile as your guide
Use the rules in the Makefile (in order) to run each part of the traditional and then the new workflow. This also includes scalability tests. Comments are added to guide you through, or you can use the last two commands to run from start (pulling data) to finish (scalability plots)

 The important part of the new algorithm is in DBFFuncs.py, and examples of its use are in newDBF.py

## These codes were written and tested using: 
* Python 3.7.3
* Numpy version 1.16.2
* Scipy version 1.2.1 (used for fftpack, commands could easily be replaced)
* Obspy version 1.1.0
* Matplotlib version 3.0.3
* Numba version 0.43.1
