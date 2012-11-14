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
    
    def __init__(self, period, reps, timepoints, density):
        """Init w/: search period, repetitions, timepoints, and density."""
        self.period = period
        self.reps = reps
        self.density = density
        self.timepoints = np.array(timepoints,dtype='float')
        
        # initialize empty memoization caches
        self.references = {}
        self.results = {}
        self.best = None # (offset, k_score)
        
    def __expand__(self, values):
        """Provides replication of time-series based on repetitions array."""
        pairs = zip(values, self.reps)
        comps = tuple([value * np.ones(times) for value,times in pairs])
        return np.concatenate(comps)
    
    def __run__(self, q, reference):
        """Tests a single series against a child reference."""
        if reference.tau_vector == None:
            reference.tau_vector = statistic._tau_vector(
                self.__expand__(reference.series)
                )
        r = reference.tau_vector
        
        k_score = np.sum(q * r)
        return k_score
    
    def run(self, q):
        """Populates the results dictionary. Returns the best-result."""
        self.results = {} # clear previous run.
        self.best = None
        
        for reference in self.generate_references():
            k_score = self.__run__(q, reference)
            offset = reference.offset
            
            if self.best == None or abs(k_score) >= abs(self.best[1]):
                self.best = (offset, k_score)
            self.results[offset] = k_score
        
        return self.best
    
    def generate_references(self):
        """Generates the entire reference library."""
        for offset in np.arange(0, self.period, self.density):
            try:
                yield self.references[offset]
            except:
                self.references[offset] = Reference(self.timepoints,
                                                    self.period,
                                                    offset)
                yield self.references[offset]
    
if __name__ == "__main__":
    print "This is a module for generating reference series."
