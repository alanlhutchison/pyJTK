#!/usr/bin/epython

import sys
import os.path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import numpy as np

def k_score(data, ref):
    """Determines concordant / discordant pairwise relationships."""
    q = _tau_vector(data)
    r = _tau_vector(ref)
    s = np.sum(q * r)
    return s
        
def _tau_vector(series):
    """Internal comparison vector that gives pairwise relationships."""
    z = np.array(series, dtype='float')
    n = len(series)
    
    idxs = _tril_indices(n)
    signs = np.sign(np.subtract.outer(z,z))
        
    return signs[idxs]
    
def _tril_indices(n):
    """Trivial retrieval of indices."""
    xs,ys = np.tril_indices(n,k=-1)
    
    #
    # N.B. Previously reindexed to retrieve values column-wise down.
    #
    # ps = zip(xs,ys)
    # ps.sort(key=lambda p:p[1])
    #
    # xs = np.array([p[0] for p in ps])
    # ys = np.array([p[1] for p in ps])
    #
    
    return (xs,ys)
    
if __name__ == "__main__":
    print "This is a jtk-cycle statistic calculation module."
