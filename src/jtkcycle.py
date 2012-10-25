#!/usr/bin/epython

import sys
import os.path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import numpy as np
from reference import Reference
import statistic

class JTKCycle:
    """Class that executes a series of cached JTK tests vs. cached reference
       series in a JTKCYCLE run. Builds periodic time series over offsets."""
    
    def __init__(self, period, time_reps, interval=1, timerange=None):
        """Init w/: search periods, timereps array, and opt. interval."""
        self.period = period
        self.interval = interval
        self.time_reps = time_reps
        
        n = len(time_reps)
        self.timerange = timerange
        if self.timerange == None:
            self.timerange = np.arange(n,dtype='float')
        
        # initialize empty memoization caches
        self.references = {}
        self.results = {}
        self.best = None # (offset, k_score)
        
    def __expand__(self, values, limit=None):
        """Provides replication of time-series based on time-reps."""
        pairs = zip(values[:limit], self.time_reps[:limit])
        comps = tuple([value * np.ones(times) for value,times in pairs])
        return np.concatenate(comps)
    
    def __run__(self, tseries, reference):
        """Tests a single series against a child reference."""
        if reference.tau_vector == None:
            reference.tau_vector = statistic._tau_vector(
                self.__expand__(reference.series)
                )
        r_tau_vector = reference.tau_vector
        return statistic.fast_k_score(tseries, r_tau_vector)
    
    def run(self, series):
        """Populates the results dictionary. Returns the best-result."""
        self.results = {} # clear previous run.
        self.best = None
        
        for reference in self.generate_references():
            k_score = self.__run__(series, reference)
            offset = reference.offset
            
            if self.best == None or abs(k_score) >= abs(self.best[1]):
                self.best = (offset, k_score)
            self.results[offset] = k_score
        
        return self.best
    
    def generate_references(self):
        """Generates the entire reference library."""
        for offset in range(self.period):
            try:
                yield self.references[offset]
            except:
                self.references[offset] = Reference(self.timerange,
                                                    self.period,
                                                    offset)
                yield self.references[offset]
    
if __name__ == "__main__":
    print "This is a module for generating reference series."
