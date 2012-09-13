#!/usr/bin/epython

import sys
import os.path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import numpy as np

class References:
    
    def __init__(self, periods, times, interval=1):
        self.periods = periods
        self.interval = interval
        self.times = times
        
        n = len(times)
        self.timerange = np.array(range(n),dtype='float')
        
    def _expand(self, values):
        if len(values) != len(self.times):
            raise Exception("unexpected elem count in expansion")
        pairs = zip(values, self.times)
        comps = tuple([p[0] * np.ones(p[1]) for p in pairs])
        return np.concatenate(comps)

    def ranks(self, series):
        n = float(len(series)) - 1.0
        
        ix = range(len(series))
        ix.sort(key=lambda j: series[j])
        ranks = [ix.index(i) / n for i in range(len(series))]
        
        return ranks

    def make_series(self, period, offset, func=None):
        if not func:
            func = np.cos
        pihat = round(np.pi,4)
        
        time_to_angle = 2 * pihat / period
        dtheta = (offset * time_to_angle) / 2.0
        thetas = self.timerange * time_to_angle
        
        vals = func(thetas + dtheta)
        ranks = self.ranks(vals)
        series = self._expand(ranks)
        
        return series
    
    def series(self, func=None):
        if not func:
            func = np.cos
        
        for period in self.periods:
            for offset in range(period):
                yield (period, offset, self.make_series(period, offset, func))
        
if __name__ == "__main__":
    print "This is a module for generating reference series."
