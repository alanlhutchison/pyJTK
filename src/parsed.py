#!/usr/bin/epython

import sys
import os.path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import string
import re
import numpy as np

class DataParser:
    """A parser class for reading microarray data and generating
       relevant specification."""
    
    def __init__(self, f):
        self.file = f
        header = f.readline()
        times = self.parse_header(header)
        
        # These are arguments to JTKCycleRun initialization...
        self.n_times   = self.count_times(times)
        self.reps      = self.get_reps(times)
        self.interval  = self.get_min_interval(times)
        self.timerange = self.get_timerange(times)
        
        # This enables correct concatenation.
        self.pattern = self.build_pattern(times)
    
    def parse_header(self, header):
        words = string.split(header)
        del words[0]
        
        times = map(self.get_ZT_time, words)
        return times
    
    def get_ZT_time(self, astring):
        m = re.search(r"ZT[\d]{1,2}$", astring)
        if not m:
            return None
        return int(m.group()[2:])
    
    def count_times(self, times):
        return len(set(times))
    
    def get_reps(self, times):
        uniques = self.__uniques__(times)
        times = [times.count(u) for u in uniques]
        return times
    
    def __uniques__(self, seq):
        seen = set()
        seen_add = seen.add
        uniques = [x for x in seq if x not in seen and not seen_add(x)]
        
        uniques.sort()
        return uniques
    
    def get_min_interval(self, times):
        intervals = self.__intervals__(times)
        return np.amin(intervals)
    
    def __intervals__(self, times):
        uniques = np.array(self.__uniques__(times), dtype='float')
        intervals = uniques[1:] - uniques[:-1]
        return intervals
    
    def get_timerange(self, times):
        intervals = self.__intervals__(times)
        if len(set(intervals)) == 1:
            return None
        else:
            return self.__uniques__(times)
    
    def build_pattern(self, times):
        uniques = self.__uniques__(times)
        
        get_indices = lambda m: [i for i,t in enumerate(times) if t == m]
        patternify = lambda t: (t, get_indices(t))
        
        pattern = map(patternify, uniques)        
        return pattern
    
    def repattern(self, series):
        repatterned = []
        for t,indices in self.pattern:
            for i in indices:
                repatterned.append(series[i])
        return repatterned
    
    def generate_series(self):
        for line in self.file:
            words = string.split(line)
            
            name = words[0]
            values = self.repattern(
                map(self.floatify, words[1:])
                )
            yield (name, values)
    
    def floatify(self, astring):
        try:
            return float(string)
        except ValueError:
            return None
    
if __name__ == "__main__":
    print "This is a parser for handling microarray data."
