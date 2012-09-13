3#!/usr/bin/epython

import sys
import os.path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import numpy as np

class ScoreFactory:
    
    def __init__(self):
        pass
    
    def score(self, data, ref):
        q = self.tau_vector(data)
        r = self.tau_vector(ref)
        s = sum(q * r)
        return s
        
    def tau_vector(self, series):
        z = np.array(series)
        n = len(series)
        
        idxs = self._tril_indices(n)
        signs = np.sign(np.subtract.outer(z,z))
        
        return signs[idxs]
    
    def _tril_indices(self, n):
        """reindex to retrieve values column-wise down"""
        xs,ys = np.tril_indices(n,k=-1)
        
        ps = zip(xs,ys)
        ps.sort(key=lambda p:p[1])
        
        xs = np.array([p[0] for p in ps])
        ys = np.array([p[1] for p in ps])
        
        return (xs,ys)
    
if __name__ == "__main__":
    print "This is a jtk-cycle statistic calculation module."
