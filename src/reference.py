#!/usr/bin/epython

import sys
import os.path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import numpy as np

class Reference:
    """Holding class for a reference time series given function, period,
       and offset.
       
       N.B. Replicates are not handled here! These are f(x) for all x in xs."""
    
    def __init__(self, xs, period, offset, **kwargs):
        """Initializes a reference time-series."""
        self.period = period
        self.offset = offset

        self.__xs__ = np.array(xs, dtype='float')
        self.__function__ = np.cos
        self.__symmetry__ = True

        if "function" in kwargs.keys():
            self.__function__ = np.frompyfunc(kwargs["function"],1,1)
            self.__symmetry__ = False
        if "symmetry" in kwargs.keys():
            self.__symmetry__ = kwargs["symmetry"]

        self.__values__ = self.__build_values__(period, offset)

        # Public data handles.
        self.series = self.__rank__(self.__values__)
        self.signs = np.sign(self.__values__)
        self.tau_vector = None
        
    def __build_values__(self, period, offset):
        """Evaluates the function f at argued xs."""
        f = self.__function__
        pi = round(np.pi,4)
        sf = 2. if self.__symmetry__ else 1.

        time_to_angle = 2 * pi / period
        dx = (offset * time_to_angle) / sf
        xs = self.__xs__ * time_to_angle

        values = np.array(f(xs + dx), dtype='float')
        return values
    
    def __rank__(self, data):
        """Fractional rank ordering of elements."""
        rank = lambda v: sorted(range(len(v)), key=v.__getitem__)

        n = len(data)
        idxs=rank(data)
        sorts=[data[idx] for idx in idxs]

        sum_ranks = 0
        n_ranked = 1
        f_ranks = [0]*n
        for i in xrange(n):
            sum_ranks += i
            n_ranked += 1
            if i==n-1 or sorts[i] != sorts[i+1]:
                avg_rank = sum_ranks / float(n_ranked)
                for j in xrange(i-n_ranked+1,i+1):
                    f_ranks[idxs[j]] = avg_rank
                sum_ranks = 0
                n_ranked = 0
        return np.array(f_ranks, dtype='float') / float(n - 1)
    
if __name__ == "__main__":
    print "Defines a class containing a reference series."
