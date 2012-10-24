#!/usr/bin/epython

import sys
import os.path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import numpy as np

class HardingDistribution:
    """Class representing an exact statistic distribution for Kendall's
       Tau. Builds cumulative distribution function on initializations
       for reference when method p-value invoked."""
    
    def __init__(self, times):
        """Initialize with time-point replication array."""
        self.max_score = self._compute_max_score(times)
        self.cdf = self._build_cdf(times)
        
    def _compute_max_score(self, times):
        """Maximum score possible for total concordance."""
        max_score = (sum(times)**2 - sum(times**2)) / 2.0
        return max_score
    
    def _build_cdf(self, times):
        """Top-level private method for generating cumulative distribution."""
        lcdf = self._build_lcdf(times)
        ucdf = self._build_ucdf(lcdf)
        
        cdf = np.concatenate((lcdf, ucdf))
        
        icf = np.array(cdf[::-1], dtype='float')
        hcf = (icf[:-1] + icf[1:]) / 2
        
        cf = np.zeros(1 + 2*self.max_score, dtype='float')
        cf[0::2] = icf
        cf[1::2] = hcf
        
        cp = cf / cf[0]
        return cp
    
    def _build_lcdf(self, times):
        """Harding algorithm to produce lower half of score distribution."""
        mode = int(self.max_score / 2)
        cf = np.ones(mode + 1, dtype='float')
        
        size = map(int,sorted(times))
        k = len(times)
        
        N = [size[-1]]
        if k > 2:
            for i in range(k-2,0,-1):
                N.append(size[i] + N[-1])
        N.reverse()
        
        for i in range(k-1):
            m = size[i]
            n = N[i]
            
            if n < mode:
                p = min(m + n, mode)
                
                if p > n+1:
                    ts = range(n+1, p+1)
                else:
                    ts = range(n+1, p-1, -1)
                
                for t in ts:
                    for u in range(mode, t-1, -1):
                        cf[u] = cf[u] - cf[u-t]
            
            q = int(min(m, mode))
            for s in range(1,q+1):
                for u in range(s, mode+1):
                    cf[u] = cf[u] + cf[u-s]
        
        lcdf = cf
        return lcdf
    
    def _build_ucdf(self, lcdf):
        """Builds symmetric upper-half cumulative distribution to c.f."""
        midx = int(self.max_score / 2)
        if self.max_score % 2 == 1:
            # odd-case: duplicate mode
            total = 2 * lcdf[midx]
            ucdf = np.zeros(midx + 1, dtype='float')
            ucdf[:midx] = lcdf[:midx][::-1]
        else:
            # even-case
            total = lcdf[midx-1] + lcdf[midx]
            ucdf = np.zeros(midx, dtype='float')
            ucdf[:midx-1] = lcdf[:midx-1][::-1]
        
        ucdf = total - ucdf
        return ucdf
    
    def p_value(self, S):
        """Publically invoked method, returns a p-value for a given Score."""
        if not S:
            p = 1.0
        else:
            M = self.max_score
            score = (np.absolute(S) + M) / 2.0
            
            # score based index in upper-half of cdf array.
            idx = int(2 * score)
            p = 2 * self.cdf[idx]
        return p

if __name__ == "__main__":
    print "This is a jtk-cycle exact null distribution module."
