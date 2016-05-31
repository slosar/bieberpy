#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
from optparse import OptionParser
import sys
sys.path.append('py')
from bieberpy import SHTrace

parser = OptionParser(usage="""Specify .bbr file on command line. 

Note that mostly min and max trace contain the same numbers, so by default
we output the min_trace, but not the max_trace field
""")


parser.add_option("-o", "--output", dest="output", default=None,
                  help="output file, otherwise rename .bbr into .txt", metavar="filename")
parser.add_option("-H", "--noheader", dest="header", default=True,
                  action="store_false", help="do not write header")
parser.add_option( "--notime", dest="time", default=True,
                   action="store_false", help="do not write time column")
parser.add_option( "--nomintrace", dest="mintrace", default=True,
                   action="store_false", help="don't write min trace record")
parser.add_option( "--maxtrace", dest="maxtrace", default=False,
                   action="store_true", help="write max trace record")


(o, args) = parser.parse_args()

if len(args)>0:
    fname=args[0]
else:
    parser.print_help()
    sys.exit(0)
    
print "Reading ",fname
da=SHTrace(fname)
if (o.output is None):
    ofname=fname.replace('.bbr','')
    ofname+='.txt'
else:
    ofname=o.output
header=""

if (o.header):
    print "Writing header..."
    for n in da.header_arr.dtype.names:
        val=da.header_arr[n][0]
        header+="# %s : %s \n"%(n,str(val))
    header+="#\n#"
    if (o.time):
        header+=" time "
    if (o.mintrace):
        header+=" min_trace "
    if (o.maxtrace):
        header+=" max_trace "

    header+="\n"

ocols=[]
fmt=''
if (o.time):
    ocols.append('time')
    fmt+='u8 '
if (o.mintrace):
    ocols.append('min_trace')
    fmt+="%g "#*da.trace_len
if (o.maxtrace): ocols.append('max_trace')

print "Writing to ", ofname#, fmt
# Doesn't fucking work
#np.savetxt(ofname,da.data[ocols],fmt=fmt, header=header)
f=open(ofname,'w')
f.write(header)
for line in da.data[ocols]:
    for v in line:
        try:
            for vx in v:
                f.write (str(vx)+" ")
        except:
            f.write(str(v)+" ")
    f.write("\n")
            
f.close()

        
        
            

