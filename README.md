# doubleBeamforming
code for traditional method and fast method for double beamforming of ambient seismic noise, with example workflow on US Array data. 

##To cite: 
Currently preprint is up at https://vtechworks.lib.vt.edu/handle/10919/96246


## Start with the Makefile as your guide
First, build/install the package using the first rule. 

Use the rules in the Makefile (in order) to run each part of the traditional and then the new workflow. This also includes scalability tests. Comments are added to guide you through, or you can use the last two commands to run from start (pulling data) to finish (scalability plots)

 The important part of the new algorithm is in doublebeamforming/DBFFuncs.py, and examples of its use are in doublebeamforming/newDBF.py

## These codes were written and tested using: 
* pip Python package manager
* Python 3.7.6
* Numpy version 1.18.1
* Scipy version 1.4.1 (used for fftpack, commands could easily be replaced)
* Obspy version 1.2.1 (installation instructions at https://github.com/obspy/obspy/wiki#installation)
* Matplotlib version 3.1.3
* Numba version 0.48.0

## Directory structure:
* LICENSE, MIT license text file
* Makefile, rules to run all tests provided
* README.md, this
* requirements.txt, lists the dependencies needed to run this code
* setup.py, script to build the double beamforming package out of the contents of the doublebeamforming subdirectory
* /docs, documentation to use the code
* /doublebeamforming, the important functions (all the reusable stuff that's not specific to this test case) for traditional and new double beamforming algorithms
* /test-scripts, where the python scripts are to test out the double beamforming package, as well as subdirectories to pull data, write intermediate results, and write output figures


