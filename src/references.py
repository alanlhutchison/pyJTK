#!/usr/bin/epython

import sys
import os.path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import numpy as np
from math import pi

class References:
    
    def __init__(self, periods, times, interval=1):
        self.periods = periods
        self.interval = interval
        self.times = times
        
    def _expand(self, values):
        if len(values) != len(self.times):
            raise Exception("unexpected elem count in expansion")
        pairs = zip(values, self.times)
        comps = [p[0] * np.ones(p[1]) for p in pairs]
        return np.concatenate(comps)
        
    def series(self, gen_f=None):
        if not gen_f:
            gen_f = np.cos
        
        pihat = round(pi,4)
        n = len(self.times)
        timerange = np.array(range(n),dtype='float')
        
        for period in self.periods:
            time_to_angle = 2 * pihat / period
            for offset in range(period):
                dtheta = (offset * time_to_angle) / 2.0
                
                thetas = timerange * time_to_angle
                vals = gen_f(thetas + dtheta)
                series = self._expand(vals)
                
                yield (period, offset, series)

if __name__ == "__main__":
    print "This is a module for generating reference series."
