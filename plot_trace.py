#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
from optparse import OptionParser
import sys
sys.path.append('py')
from bieberpy import SHTrace

parser = OptionParser(usage="Specify .bbr file on command line")
parser.add_option("-s", "--show", dest="show", default=False,
                  action="store_true", help="call show at the end")
parser.add_option("-p", "--pdf", dest="pdf", default=None,
                  help="save to pdf", metavar="filename")
parser.add_option("--fmin", dest="fmin", default=None,
                  help="min freqency [MHz]", metavar="value", type="float")
parser.add_option("--fmax", dest="fmax", default=None,
                  help="max freqency [MHz]", metavar="value", type="float")
parser.add_option("--tmin", dest="tmin", default=None,
                  help="min time [ms timestamp]", metavar="value", type="float")
parser.add_option("--tmax", dest="tmax", default=None,
                  help="max time [ms timestamp]", metavar="value", type="float")
parser.add_option("--favg", dest="favg", default=1,
                  help="frequency averaging", metavar="value", type="int")
parser.add_option("--tavg", dest="tavg", default=1,
                  help="time averaging", metavar="value", type="int")
parser.add_option("--pmin", dest="pmin", default=None,
                  help="min power [dB]", metavar="value", type="float")
parser.add_option("--pmax", dest="pmax", default=None,
                  help="max power [dB]", metavar="value", type="float")

(o, args) = parser.parse_args()

if len(args)>0:
    fname=args[0]
else:
    parser.print_help()
    sys.exit(0)
    
print "Reading ",fname
da=SHTrace(fname)
print "Frequencies span:",da.freq[0], da.freq[-1], "# samples:",len(da.freq)
print "Timestamps span:",da.timestamps[0], da.timestamps[-1], "# samples:", len(da.timestamps)

faxis,taxis,pdata=da.getDataCube(o.fmin,o.fmax,o.tmin,o.tmax,o.favg,o.tavg)
fmin,fmax=faxis[0],faxis[-1]
tmin,tmax=taxis[0], taxis[-1]
print tmax-tmin
print o.pmin, o.pmax
plt.figure(figsize=(20,20))
plt.imshow(pdata,interpolation='nearest',extent=(fmin,fmax,0,(tmax-tmin)/1e3),
           vmin=o.pmin, vmax=o.pmax,aspect='auto')
plt.ylabel('t[s]')
plt.xlabel('f[MHz]')
plt.colorbar()

if o.pdf:
    plt.savefig(o.pdf)

if o.show:
    plt.show()

