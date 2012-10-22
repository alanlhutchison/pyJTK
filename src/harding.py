#!/usr/bin/epython

import sys
import os.path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import numpy as np

class HardingDistribution:
    
    def __init__(self, times):
        self.max_score = self._compute_max_score(times)
        self.cdf = self._build_cdf()
        
        self.times = times
        
    def _compute_max_score(self, times):
        max_score = (sum(times)**2 - sum(times**2)) / 2.0
        return max_score
    
    def _build_cdf(self):
        # mode = np.floor(self.max_score)
        # cf = np.ones(mode + 1, dtype='float')
        
        # size = np.sort(self.times)
        # k = len(self.times)
        
        # N = size[-1]
        # if k > 2:
        #     pass

        #
        #
        #
        
        # np.sum(cf, axis=1, dtype='float')
        
        return None
    
    def p_value(self, S):
        if not S:
            p = 1.0
        else:
            M = self.max_score
            score = (abs(S) + M) / 2.0
            idx = 2 * score
            p = self.cdf[idx]
        return p

if __name__ == "__main__":
    print "This is a jtk-cycle exact null distribution module."
