#
# Python Interface to Signal Hound .bbr files
#
import numpy as np


class SHTrace(object):

    """
    From https://github.com/SignalHound/BBApp/blob/master/BBApp/src/model/playback_toolbar.h:

       struct playback_header {
        unsigned short signature;
        unsigned short version;

        int sweep_count;

        ushort title[MAX_TITLE_LEN + 1];
        double center_freq; // Sweep settings
        double span;
        double rbw;
        double vbw;
        double ref_level;
        double div;
        int atten;
        int gain;
        int detector;

        int trace_len;
        double trace_start_freq;
        double bin_size;
    };
    """
    _head_desc=[('signature','u2'),('version','u2'),('count','i4'),
                ('title','S256'),('center_freq','f8'),('span','f8'),
                ('rbw','f8'),('vbw','f8'), ('ref_level','f8'),('div','f8'),
                ('atten','i4'), ('gain','i4'),('detector','i4'),('trace_len','i4'),
                ('trace_start_freq','f8'),('bin_size','f8')]
    _head_dt=np.dtype(_head_desc,align=False)

    def __init__ (self,filename):
        """
        Given filename, read the file and initialize the object
        """
        f=open(filename)
        self.header_arr=np.fromfile(f,self._head_dt,count=1)
        for n in self.header_arr.dtype.names:
            self.__dict__.update({n:self.header_arr[n][0]})
        self.Ns=self.count
        # now read the rest of the data
        rec_desc=[('time','u8'),('min_trace','f4',self.trace_len),('max_trace','f4',self.trace_len)]
        rec_dt=np.dtype(rec_desc,align=False)
        self.data=np.fromfile(f,rec_dt)
        if not (len(self.data)==self.count):
            print "Warning, number of records in header (%i) doesn't match number read (%i) " %(
                self.count, len(self.data))
        # we work in MHz
        self.freq = self.trace_start_freq/1e6+self.bin_size*np.arange(self.trace_len)/1e6
        self.timestamps=self.data['time']
    
    def getDataCube (self,min_freq=None, max_freq=None, min_time=None, max_time=None,
                     freq_avg=1, time_avg=1):
        """
        Returns the data appropriate cuts and averages
        """
        if min_freq==None:
            imin=0
        else:
            imin=np.argmax(self.freq>min_freq)
        if max_freq==None:
            imax=len(self.freq)
        else:
            imax=np.argmin(self.freq<max_freq)

        if min_time==None:
            jmin=0
        else:
            jmin=np.argmax(self.timestamps>min_time)
        if max_time==None:
            jmax=len(self.timestamps)
        else:
            jmax=np.argmin(self.timestamps<max_time)

        freqs=self.freq[imin:imax]
        tstamps=self.timestamps[jmin:jmax]
        #print imin,imax,jmin,jmax
        data=self.data["min_trace"][jmin:jmax,imin:imax]
        if (freq_avg>1) or (time_avg>1):
            ## funnily enough, there doesn't seem to be a better way
            ## of boxcar average than this
            Nf=len(freqs)/freq_avg
            Nt=len(tstamps)/time_avg
            if (Nf*freq_avg<len(freqs)):
                Nf+=1
            if (Nt*time_avg<len(tstamps)):
                Nt+=1
            nfreqs=np.array([freqs[i*freq_avg:(i+1)*freq_avg].mean() for i in range(Nf)])
            ntstamps=np.array([tstamps[i*time_avg:(i+1)*time_avg].mean() for i in range(Nt)])
            ndata=np.array([[ data[i*time_avg:(i+1)*time_avg,j*freq_avg:(j+1)*freq_avg].mean() for j in range(Nf)]
                                              for i in range(Nt)])
            freqs=nfreqs
            tstamps=ntstamps
            data=ndata
        return freqs,tstamps,data
    
        
