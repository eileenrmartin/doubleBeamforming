# Written by Eileen R. Martin

import obspy
from obspy.clients.fdsn import Client

client = Client("IRIS") # IRIS DMC
network = "TA" # US Array Transportable Array
stationsA = ['D27A', 'D28A', 'D29A', 'E27A', 'E28A', 'E29A', 'F27A', 'F28A', 'F29A']
stationsB = ['Y24A', 'Y25A', 'Y26A', 'Z24A', 'Z25A', 'Z26A', '124A', '125A', '126A']
channel = 'BHZ'


datapath = 'test-scripts/data/' # where data will be stored locally after pulling, relative to directory with Makefile

# able to pull a month of data
start = obspy.UTCDateTime("2009-11-01T00:00:00.000")
endTime = obspy.UTCDateTime("2009-11-30T23:59:59.000")
initWindowHrs = 24
initWindowSec = initWindowHrs*60*60 # for one channel on 18 stations, this means 6*39.6 MB data per window

windowHrs = 4 # to be used after dividing up into smaller windows
windowSec = windowHrs*60*60



Nt = 160
