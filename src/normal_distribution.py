#!/usr/bin/epython

import sys
import os.path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import numpy as np
from scipy.stats import norm
from math import sqrt

class NormalDistribution:

    def __init__(self, timepoints, reps=1):
        try:
            if len(reps) == timepoints:
                times = np.array(reps)
            else:
                times = reps[0] * np.ones(timepoints, dtype='float')
            
        except: # reps is not array-like
            times = reps * np.ones(timepoints, dtype='float')
        
        self.stdev = self._compute_stdev(times)
        self.max_score = self._compute_max_score(times)
        self.expected = self.max_score / 2.0
    
    def _compute_max_score(self, times):
        max_score = (sum(times)**2 - sum(times**2)) / 2.0
        return max_score
    
    def _compute_stdev(self, times):
        nn = sum(times)
        ns = times
        
        var = (nn**2 * (2*nn + 3) - sum(ns**2 * (2*ns + 3))) / 72.0
        sdv = sqrt(var)
        return sdv
    
    def p_value(self, S):
        if not S:
            p = 1.0
        else:
            M = self.max_score
            score = (abs(S) + M) / 2.0
            p = 2 * norm.sf(-(score-0.5),
                            loc=self.expected,
                            scale=self.stdev)
            p = 0.0
        return p

if __name__ == "__main__":
    print "This is a jtk-cycle null distribution normal-approximation module."
