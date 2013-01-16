#!/usr/bin/epython

import sys
import os.path

p = os.path.realpath(__file__)
q = os.path.split(os.path.dirname(p))
sys.path.append(os.path.join(q[0], "src"))
del p, q # keep globals clean

import unittest
import generated as g
import numpy as np

TEST_N = 12
MAX_S = 0.5 * TEST_N * (TEST_N - 1.0)

class DistributionSpec(unittest.TestCase):
    """Describe the Distribution class."""
    def setUp(self):
        self.series = series = np.random.random(TEST_N)
        self.case = g.GeneratedDistribution(N=10)
        self.period = period = len(series)
        self.case.add_reference(period, series)
    
    def test_initialization(self):
        """It should correctly generate an instance of the class."""
        self.assertTrue(isinstance(self.case, g.GeneratedDistribution))
    
    def test_series_memoization(self):
        """It should correctly recall the series initially used to generate."""
        self.assertTrue(np.all(self.series == self.case.references[self.period]))

class ScoresSpec(unittest.TestCase):
    """Describe the Monte-Carlo generation of scores."""
    
    def test_default_size(self):
        """It defaults to a distribution size of 25000."""
        series = np.random.random(TEST_N)
        case = g.GeneratedDistribution()
        period = len(series)
        case.add_reference(period, series)
        
        self.assertEqual(25000, case.scores[period].size)
        self.assertTrue(np.all(np.abs(case.scores[period]) <= MAX_S))
        
    def test_argued_size(self):
        """It accepts an argued distribution size and build accordingly."""
        distribution_size = 25
        series = np.random.random(TEST_N)
        period = len(series)
        case = g.GeneratedDistribution(N=distribution_size)
        case.add_reference(len(series), series)
        
        self.assertEqual(distribution_size, case.scores[period].size)
        self.assertTrue(np.all(np.abs(case.scores[period]) <= MAX_S))

class SeriesSpec(unittest.TestCase):
    """Describe the generation of test series."""
    def setUp(self):
        self.distribution_size = ds = 10
        self.series = series = np.random.random(TEST_N)
        self.case = g.GeneratedDistribution(N=ds)
        self.case.add_reference(len(series), series)
    
    def test_series_shape(self):
        """It generates a test series of appropriate shape."""
        series = self.case.__make_series__(TEST_N)
        self.assertEqual(self.distribution_size, series.shape[0])
        self.assertEqual(TEST_N, series.shape[1])
    
    def test_series_values(self):
        """It should generate values with appropriate bounds."""
        series = self.case.__make_series__(TEST_N)
        shape = (self.distribution_size, TEST_N)
        self.assertTrue(np.all(series <= np.ones(shape)))
        self.assertTrue(np.all(series >= np.zeros(shape)))
    
class PValueSpec(unittest.TestCase):
    """Describe the computation of p-values."""
    def setUp(self):
        series = np.random.random(TEST_N)
        self.period = period = len(series)
        self.case = g.GeneratedDistribution(N=2500)
        self.case.add_reference(period, series)
    
    def test_minimum(self):
        """It should report 1.0 for a zero score."""
        expect = 1.0
        actual = self.case.p_value(0, period=self.period)
        self.assertEqual(expect, actual)
    
    def test_maximum(self):
        """It should report significant values for a high score."""
        actual = self.case.p_value(MAX_S, period=self.period)
        significant = 0.01
        self.assertTrue(actual <= significant)
    
if __name__ == "__main__":
    unittest.main()
