#!/usr/bin/epython

import sys
import os.path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import numpy as np

class References:
    """Class that provides a series of reference time series
    for a given JTKCYCLE run. Builds time series over periods / phases."""
    
    def __init__(self, periods, times, interval=1):
        """Init w/: search periods, timereps array, and opt. interval."""
        self.periods = periods
        self.interval = interval
        self.times = times
        
        n = len(times)
        self.timerange = np.array(range(n),dtype='float')
        
    def _expand(self, values, tlim=None):
        """Provides replication of time-series based on timereps array."""
        if len(values) != len(self.times):
            raise Exception("unexpected elem count in expansion")
        pairs = zip(values[:tlim], self.times[:tlim])
        comps = tuple([value * np.ones(times) for value,times in pairs])
        return np.concatenate(comps)

    def ranks(self, series):
        """Rank-ordering of series."""
        n = float(len(series)) - 1.0
        
        ix = range(len(series))
        ix.sort(key=lambda j: series[j])
        ranks = [ix.index(i) / n for i in range(len(series))]
        
        return ranks

    def make_series(self, period, offset, **kwargs):
        """Builds a time-series for a given period and offset.
        Keyword arguments: bool signed, function func, int tlim."""
        
        signed = False
        if "signed" in kwargs.keys() and kwargs["signed"]:
            signed = True
        
        func = np.cos
        if "func" in kwargs.keys():
            func = kwargs["func"]
        
        tlim = None
        if "tlim" in kwargs.keys():
            tlim = kwargs["tlim"]
        
        pihat = round(np.pi,4)
        
        time_to_angle = 2 * pihat / period
        dtheta = (offset * time_to_angle) / 2.0
        thetas = self.timerange * time_to_angle
        
        vals = np.array(func(thetas + dtheta),dtype='float')
        ranks = self.ranks(vals)
        signs = np.sign(vals)
        
        if signed:
            series = self._expand(signs, tlim)
        else:
            series = self._expand(ranks, tlim)
        
        return np.array(series,dtype='float')
    
    def series(self, func=None):
        """Generates the entire reference library.
        Opt. func argument can specify non-sinusoid functions."""
        if not func:
            func = np.cos
        
        for period in self.periods:
            for offset in range(period):
                yield (period, offset, self.make_series(period, offset, func=func))
        
if __name__ == "__main__":
    print "This is a module for generating reference series."
