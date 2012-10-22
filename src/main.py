#!/usr/bin/epython

import sys
import os.path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import numpy as np

import utility as u
import normal as t
import statistic
import references as r

class JTKCYCLE:
    """Class encapsulating the logic for running a JTK-CYCLE statistical
       test. Components are a score factory, a statistical distribution,
       and a reference library."""
    
    def __init__(self, timepoints, reps, periods, interval=1):
        """Init w/: timepoint count, repetition count, and search periods.
        Opt. interval specifies time-unit distance between timepoints."""
        
        times = u.make_times(timepoints, reps)
        
        self.timepoints = timepoints
        self.times = times
        
        self.periods = periods
        self.interval = interval
        
        # score factory, distribution, and reference series generator
        self.distribution = t.NormalDistribution(times)
        self.references = r.References(periods, times, interval)
    
    def _run(self, series, refp):
        per,off,ser = refp
        
        s_score = statistic.k_score(series, ser)
        p_score = self.distribution.p_value(s_score)
        
        amp = self.est_amp(ser, per, off, s_score)
        
        return (per, off, amp, s_score, p_score)
    
    def run_series(self, series):
        """Input series is run through JTK-CYCLE."""
        results = [self._run(series,ref) for ref in self.references.series()]
        results = self.do_bonferroni(results)
        best = self.find_best(results)
        
        return best
    
    def find_best(self, results):
        """From a series of results vs. reference library,
        extracts characterization of best fitting reference."""
        p_vals = [r[4] for r in results]
        
        min_p = min(p_vals)
        fresults = filter(lambda r: r[4] == min_p, results)
        
        per = np.average([r[0] for r in fresults])
        lag = np.average([r[1] for r in fresults])
        amp = max(0.0, np.average([r[2] for r in fresults]))
        
        scores = [r[3] for r in fresults]
        tau = abs(np.average(scores)) / self.distribution.max_score
        
        return (min_p, per, lag, amp, tau)
    
    def est_amp(self, series, period, offset, S):
        """Estimates amplitude based on best fit reference series."""
        sref = self.references.make_series(period,
                                           offset,
                                           signed=True,
                                           tlim=period)
        s = np.sign(S) or 1.0
        
        ser = np.array(series[:len(sref)], dtype='float')
        w = (ser - np.median(ser))
        
        amps = s * sref * w
        amps = filter(lambda a: a != 0.0, amps)
        amp = np.median(amps)
        
        factor = np.sqrt(2.0)
        return amp * factor
    
    def do_bonferroni(self, uncorrected):
        """Applies bonferroni correction to a series of results."""
        scores = self._bonferroni([u[4] for u in uncorrected])
        corrected = [(u[0],u[1],u[2],u[3],s) for u,s in zip(uncorrected,scores)]
        return corrected
    
    def _bonferroni(self, scores):
        """Arithmetic helper function for bonferroni correction."""
        scores = np.array(scores, dtype='float')
        scores = scores * len(scores)
        return scores

if __name__ == "__main__":
    print "Defines the main running class for jtk cycle statistical test."
