#!/usr/bin/epython

import sys
import os.path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import numpy as np

import utility as u
from normal import NormalDistribution
from harding import HardingDistribution
from jtkcycle import JTKCycle
import statistic

class JTKCycleRun:
    """Class encapsulating the logic for running a JTK-CYCLE statistical
       test. Generates a statistical distribution and collection of
       reference cycles."""
    
    def __init__(self, n_times, reps, periods,
                 interval=1, timerange=None, normal=False):
        """Init w/: timepoint count, repetition spec, and search periods.
           Opt. interval specifies time-value intervalse between timepoints.
           Opt. timerange specifies unevenly spaced time intervals."""
        time_reps = u.make_times(n_times, reps)
        self.time_reps = time_reps
        self.timerange = timerange
        
        self.periods = periods
        self.interval = interval
        
        if normal:
            self.distribution = NormalDistribution(time_reps)
        else:
            self.distribution = HardingDistribution(time_reps)
        
        # initialize empty lookup table for test cycles and results.
        self.cycles = {}
        self.results = {}
        self.best = None
    
    def __find_best__(self, cycles, best_p):
        results = self.__find_matches__(cycles, best_p)
        
        period = self.interval * np.average([r[0] for r in results])
        offset = self.interval * np.average([r[1] for r in results])
        k_score = np.amin([r[2] for r in results])
        p_value = np.amax([r[3] for r in results])
        
        return (period, offset, k_score, p_value)
    
    def __find_matches__(self, cycles, best_p):
        """Searches child trees for equivalently high-scoring values."""
        p = lambda k: self.bonferroni_adjust(self.distribution.p_value(k))
        
        results = []
        for cycle in cycles:
            for offset in cycle.results.keys():
                k_score = cycle.results[offset]
                p_value = p(k_score)
                
                if p_value == best_p:
                    per,off = float(cycle.period),float(offset)
                    s = np.sign(k_score) or 1
                    lag = (per + (1-s)*per/4 - off/2) % per
                    results.append(
                        (cycle.period, lag, k_score, p_value)
                        )
        return results
    
    def run(self, series):
        """Input series is run through JTK-CYCLE."""
        self.results = {} # clear previous run.
        self.best = None
        best_cycles, best_p = [], 1.0
        
        for cycle in self.generate_jtk_cycles():
            period = cycle.period
            offset, k_score = cycle.run(series)
            p_value = self.bonferroni_adjust(
                self.distribution.p_value(k_score)
                )
            
            if p_value < best_p:
                best_p = p_value
            self.results[period] = (offset, k_score, p_value)
        
        for cycle in self.generate_jtk_cycles():
            k_score = cycle.best[1]
            p_value = self.bonferroni_adjust(
                self.distribution.p_value(k_score)
                )
            if p_value == best_p:
                best_cycles.append(cycle)
        
        self.best = self.__find_best__(best_cycles, best_p)
        return self.best
    
    def generate_jtk_cycles(self):
        """Lazy instantiation generator for building a memoized hash
           of reference cycle instances. One for each period to check."""
        for period in self.periods:
            try:
                yield self.cycles[period]
            except:
                cycle = JTKCycle(
                    period,
                    self.time_reps,
                    self.interval,
                    self.timerange
                    )
                self.cycles[period] = cycle
                yield self.cycles[period]
    
    def bonferroni_adjust(self, p_value):
        """Applies test-specific bonferroni correction to a p-value."""
        n = np.sum(self.periods)
        return min(1.0, n * p_value)
    
if __name__ == "__main__":
    print "Defines the main running class for jtk cycle statistical test."
