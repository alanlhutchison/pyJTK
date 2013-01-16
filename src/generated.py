#!/usr/bin/epython

import sys
import os.path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import numpy as np
import statistic as s

class GeneratedDistribution:
    """Class represents a Monte-Carlo generated distribution for Kendall's Tau."""

    def __init__(self, **kwargs):
        self.N = 25000
        if "N" in kwargs.keys():
            self.N = kwargs["N"]

        self.references = {}
        self.scores = {}

    def add_reference(self, period, series):
        self.references[period] = series
        self.scores[period] = self.__make_scores__(period)

    def __make_scores__(self, period):
        series = self.__make_series__(period)
        scores = np.zeros(self.N)

        reference = self.references[period]
        for i in xrange(series.shape[0]):
            test = series[i,:]
            scores[i] = s.k_score(reference, test)

        return np.abs(scores)

    def __make_series__(self, period):
        n = self.references[period].size
        return np.random.random((self.N, n))

    def p_value(self, S, **kwargs):
        try:
            period = kwargs["period"]
        except:
            raise Exception("Must specify period for Monte Carlo distributions.")
        leqs = np.sum(np.ones(self.N)[self.scores[period] >= np.abs(S)])
        return leqs / float(self.N)
    
if __name__ == "__main__":
    print "This class encapsulates a Monte-Carlo null distribution."
