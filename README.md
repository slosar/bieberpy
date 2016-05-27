# bieberpy
Python Interface to Signal Hound bbr files

A very simple class that will load Signal Hound bbr files as produced by their spike software.
Using plott_trace.py one can plot a very simple waterfall plots.
Do something like:

```
~/work/BMX/bieberpy $ ./plot_trace.py 
Usage: Specify .bbr file on command line

Options:
  -h, --help            show this help message and exit
  -s, --show            call show at the end
  -p filename, --pdf=filename
                        save to pdf
  --fmin=value          min freqency [MHz]
  --fmax=value          max freqency [MHz]
  --tmin=value          min time [ms timestamp]
  --tmax=value          max time [ms timestamp]
  --favg=value          frequency averaging
  --tavg=value          time averaging
  --pmin=value          min power [dB]
  --pmax=value          max power [dB]
~/work/BMX/bieberpy $ ./plot_trace.py  ../bbrpy/2016-05-26\ 17h21m39s.bbr --favg=100 --pmax=-60 -s
Reading  ../bbrpy/2016-05-26 17h21m39s.bbr
Frequencies span: 500.014138735 1499.98527332 # samples: 35000
Timestamps span: 1464297703150 1464324152240 # samples: 3572
```
