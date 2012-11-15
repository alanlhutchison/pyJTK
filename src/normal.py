#!/usr/bin/epython

import sys
import os.path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import numpy as np
import utility as u

class NormalDistribution:
    """An normal approximation of the J-T Score distribution."""

    def __init__(self, times):
        """Init w. replicated times array (see utility.py)."""
        self.stdev = self._compute_stdev(times)
        self.max_score = self._compute_max_score(times)
        self.expected = self.max_score / 2.0
    
    def _compute_max_score(self, times):
        max_score = (sum(times)**2 - sum(times**2)) / 2.0
        return max_score
    
    def _compute_stdev(self, times):
        nn = sum(times)
        ns = times
        
        var = (nn**2 * (2*nn + 3) - np.sum(ns**2 * (2*ns + 3))) / 72.0
        sdv = np.sqrt(var)
        
        return sdv
    
    def p_value(self, S):
        """Public handle for generating a p-value from a tau score S."""
        if not S:
            return 1.0
        
        M = self.max_score
        score = (np.absolute(S) + M) / 2.0
        
        a = -1.0 * (score - 0.5)
        b = -1.0 * self.expected
        
        num = np.abs(a - b)
        den = self.stdev * np.sqrt(2)
        
        normal_cdf = lambda x: 1.0 - u.erf(x)
        p = normal_cdf(num / den)
        return p

if __name__ == "__main__":
    print "This is a jtk-cycle null distribution normal-approximation module."
