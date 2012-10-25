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
        if "function" in kwargs.keys():
            self.__function__ = kwargs["function"]
        
        self.__values__ = self.__build_values__(period, offset)
        
        # Public data handles.
        self.series = self.__rank__(self.__values__)
        self.signs = np.sign(self.__values__)
        self.tau_vector = None
        
    def __build_values__(self, period, offset):
        """Evaluates the function f at argued xs."""
        f = self.__function__
        pi = round(np.pi,4)
        
        time_to_angle = 2 * pi / period
        dx = (offset * time_to_angle) / 2.0
        xs = self.__xs__ * time_to_angle
        
        values = np.array(f(xs + dx), dtype='float')
        return values
    
    def __rank__(self, values):
        """Rank-ordering of series."""
        n = float(len(values)) - 1.0
        
        ix = range(len(values))
        ix.sort(key=lambda j: values[j])
        ranks = [ix.index(i) / n for i in range(len(values))]
        
        return np.array(ranks, dtype='float')
    
if __name__ == "__main__":
    print "Defines a class containing a reference series."
