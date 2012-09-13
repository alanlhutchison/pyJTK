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
        refs = refp[2]
        s_score = self.scorer.score(series, refs)
        p_score = self.distribution.p_value(s_score)
        return (refp[0], refp[1], p_score)
    
    def run_series(self, series):
        if len(series) != self.timepoints:
            raise Exception("poorly formatted series.")
        
        results = np.array(
            [self._run(series,ref) for ref in self.references.series()],
            dtype='float'
            )
        scores = self.bonferroni([r[2] for r in results])
        results = [(r[0],r[1],s) for r,s in zip(results,scores)]
        return min(results, key=lambda p:p[2])
    
    def bonferroni(self, scores):
        scores = np.array(scores, dtype='float')
        scores = scores / len(scores)
        return scores

if __name__ == "__main__":
    print "Defines the main running class for jtk cycle statistical test."
