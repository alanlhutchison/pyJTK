#!/usr/bin/epython

import sys
import os.path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import numpy as np

import utility as u
from jtkcycle import JTKCycle
import statistic

from normal import NormalDistribution
from generated import GeneratedDistribution
from harding import HardingDistribution

class JTKCycleRun:
    """Class encapsulating the logic for running a JTK-CYCLE statistical
       test. Generates a statistical distribution and collection of
       reference cycles."""
    
    def __init__(self, reps, timepoints, periods, density, **kwargs):
        """Init w/: timepoint count, repetition spec, and search periods.
           Opt. timepoints specifies unevenly spaced time intervals."""
        self.reps = np.array(reps,dtype='float')
        self.timepoints = np.array(timepoints,dtype='float')
        self.periods = periods
        self.density = density

        self.__function__ = kwargs.get("function", np.cos)
        self.__symmetry__ = kwargs.get("symmetry", True)

        normal = kwargs.get("normal", True)
        if normal:
            self.distribution = NormalDistribution(self.reps)
        else:
            self.distribution = HardingDistribution(self.reps)

        # initialize empty lookup table for test cycles and results.
        self.cycles = {}
        self.results = {}
        self.best = None
    
    def __find_best__(self, series, cycles, best_p):
        results = self.__find_matches__(cycles, best_p)

        period = np.average([r[0] for r in results])
        offset = np.average([r[1] for r in results])
        k_score = np.amin([r[2] for r in results])
        p_value = np.amax([r[3] for r in results])
        est_amp = u.est_amp(series)

        return (est_amp, period, offset, k_score, p_value)
    
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

                    # a bit of modulo arithmetic to get lag.
                    if self.__symmetry__:
                        lag = (per + (1-s)*per/4 - off/2) % per
                    else:
                        lag = ((2 * per) - off) % per

                    results.append(
                        (cycle.period, lag, k_score, p_value)
                        )
        return results

    def run(self, series):
        """Input series is run through JTK-CYCLE."""
        self.results = {} # clear previous run.
        self.best = None
        best_cycles, best_p = [], 1.0

        q = statistic._tau_vector(series)

        for cycle in self.generate_jtk_cycles():
            period = cycle.period
            p = lambda k: self.bonferroni_adjust(
                self.distribution.p_value(k, period=period)
                )

            offset, k_score = cycle.run(q)
            p_value = p(k_score)

            if p_value < best_p:
                best_p = p_value
            self.results[period] = (offset, k_score, p_value)

        for cycle in self.generate_jtk_cycles():
            k_score = cycle.best[1]
            p_value = p(k_score)
            if p_value == best_p:
                best_cycles.append(cycle)

        self.best = self.__find_best__(series, best_cycles, best_p)
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
                    self.reps,
                    self.timepoints,
                    self.density,
                    function=self.__function__,
                    symmetry=self.__symmetry__
                    )
                self.cycles[period] = cycle
                yield self.cycles[period]

    def bonferroni_adjust(self, p_value):
        """Applies test-specific bonferroni correction to a p-value."""
        n = np.sum(self.periods)
        return min(1.0, n * p_value)

if __name__ == "__main__":
    print "Defines the main running class for jtk cycle statistical test."
