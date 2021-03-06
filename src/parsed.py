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
    
    def __init__(self, f, should_repattern=False):
        self.file = f
        header = f.readline()
        times = self.parse_header(header)
        
        # These are arguments to JTKCycleRun initialization...
        self.reps       = self.get_reps(times)
        self.timepoints = self.get_timepoints(times)
        
        # This enables correct concatenation.
        self.should_repattern = should_repattern
        self.pattern = self.build_pattern(times)
    
    def parse_header(self, header):
        words = string.split(header)
        del words[0]
        
        times = map(self.get_ZT_time, words)
        return times
    
    def get_ZT_time(self, astring):
        m = re.search(r"ZT[\d.]+$", astring)
        if not m:
            return None
        return float(m.group()[2:])
    
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
    
    def get_timepoints(self, times):
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
            values = map(self.floatify, words[1:])
            if self.should_repattern:
                values = self.repattern(values)
            yield (name, values)
    
    def floatify(self, astring):
        try:
            return float(astring)
        except:
            return None
    
if __name__ == "__main__":
    print "This is a parser for handling microarray data."
