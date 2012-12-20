#!/usr/bin/epython

import sys
import os.path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import numpy as np
import statistic as s

class GeneratedDistribution:
    """Class represents a Monte-Carlo generated distribution for Kendall's Tau."""

    def __init__(self, reference, **kwargs):
        self.reference = reference
        self.N = 10000
        if "N" in kwargs.keys():
            self.N = kwargs["N"]
        self.scores = self.__make_scores__()
    
    def __make_scores__(self):
        series = self.__make_series__()
        scores = np.zeros(self.N)
        for i,test in enumerate(series):
            scores[i] = s.k_score(self.reference, test)
        return np.abs(scores)
    
    def __make_series__(self):
        n = self.reference.size
        return np.random.random((self.N, n))
    
    def p_value(self, S):
        leqs = np.sum(np.ones(self.N)[self.scores >= np.abs(S)])
        return leqs / float(self.N)
    
if __name__ == "__main__":
    print "This class encapsulates a Monte-Carlo null distribution."
