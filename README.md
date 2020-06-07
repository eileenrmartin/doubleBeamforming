# doubleBeamforming
code for traditional method and fast method for double beamforming of ambient seismic noise, with example workflow on US Array data. 

##To cite: 
Currently preprint is up at https://vtechworks.lib.vt.edu/handle/10919/96246


## Start with the Makefile as your guide
First, build/install the package using the first rule. 

Use the rules in the Makefile (in order) to run each part of the traditional and then the new workflow. This also includes scalability tests. Comments are added to guide you through, or you can use the last two commands to run from start (pulling data) to finish (scalability plots)

 The important part of the new algorithm is in DBFFuncs.py, and examples of its use are in newDBF.py

## These codes were written and tested using: 
* pip Python package manager
* Python 3.7.6
* Numpy version 1.18.1
* Scipy version 1.4.1 (used for fftpack, commands could easily be replaced)
* Obspy version 1.2.1
* Matplotlib version 3.1.3
* Numba version 0.48.0
