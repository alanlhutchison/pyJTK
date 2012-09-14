#!/usr/bin/epython

import sys
import os.path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import numpy as np

import utility as u
import normal as t
import statistic as s
import references as r

class JTKCYCLE:
    
    def __init__(self, timepoints, reps, periods, interval=1):
        times = u.make_times(timepoints, reps)
        
        self.timepoints = timepoints
        self.times = times
        
        self.periods = periods
        self.interval = interval
        
        self.scorer = s.ScoreFactory()
        self.distribution = t.NormalDistribution(times)
        self.references = r.References(periods, times, interval)
    
    def _run(self, series, refp):
        per,off,ser = refp
        
        s_score = self.scorer.score(series, ser)
        p_score = self.distribution.p_value(s_score)
        
        amp = self.est_amp(ser, per, off, s_score)
        
        return (per, off, amp, p_score)
    
    def run_series(self, series):
        if len(series) != self.timepoints:
            raise Exception("poorly formatted series.")
        
        results = np.array(
            [self._run(series,ref) for ref in self.references.series()],
            dtype='float'
            )
        results = self.do_bonferroni(results)
        best = self.best(results)
        
        return best
    
    def best(self, results):
        scores = [r[3] for r in results]
        
        min_score = min(scores)
        results = filter(lambda r: r[3] == min_score, results)
        
        per = np.average([r[0] for r in results])
        lag = np.average([r[1] for r in results])
        amp = max(0.0, np.average([r[2] for r in results]))
        tau = abs(min_score) / self.distribution.max_score
        
        return (per, lag, amp, tau)
    
    def est_amp(self, series, period, offset, S):
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
        scores = self._bonferroni([u[3] for u in uncorrected])
        corrected = [(u[0],u[1],u[2],s) for u,s in zip(uncorrected,scores)]
        return corrected
    
    def _bonferroni(self, scores):
        scores = np.array(scores, dtype='float')
        scores = scores / len(scores)
        return scores

if __name__ == "__main__":
    print "Defines the main running class for jtk cycle statistical test."
