#!/usr/bin/epython

import sys
import os.path

p = os.path.realpath(__file__)
q = os.path.split(os.path.dirname(p))
sys.path.append(os.path.join(q[0], "src"))
del p, q # keep globals clean

import unittest
import reference as R
import random
import numpy as np

class CustomFunctionSpec(unittest.TestCase):
    """Describe Reference instances with custom functions."""

    def setUp(self):
        angle_to_time = 24.0 / (2 * np.pi)
        self.reindex = lambda p: p * angle_to_time

    def test_constant(self):
        """It should make a series consisting of constant values."""
        cv = 10. * np.random.random()
        cf = lambda x: cv
        case = R.Reference(np.arange(0,24,2, dtype='float'), 24., 0., function=cf)
        for value in case.__values__:
            self.assertEqual(value, cv)

    def test_alternating(self):
        """It should generate a series with alternating +/- 1 values."""
        af = lambda p: -1 ** int(self.reindex(p))
        case = R.Reference(np.arange(0,24,2, dtype='float'), 24., 0., function=af)
        for i,value in enumerate(case.__values__):
            self.assertEqual(value, -1**i)

    def test_harmonic(self):
        """It should test against a descending harmonic series."""
        hf = lambda p: np.round(1.0 / (1.0 + self.reindex(p)), 2)
        case = R.Reference(np.arange(0,24,1, dtype='float'), 24., 0., function=hf)
        for i,value in enumerate(case.__values__):
            self.assertEqual(np.round(1./(i+1.0), 2), value)

class RankingSpec(unittest.TestCase):
    """Describe the rank-ordering functions in time series class."""

    def setUp(self):
        self.case = R.Reference(range(0,24,2),24,0)

    def test_rankings(self):
        """It correctly rank-orders elements in a time-series."""
        series = [5,3,2,1,4,6]
        ranked = self.case.__rank__(series)
        expect = [0.8, 0.4, 0.2, 0.0, 0.6, 1.0]
        for p in zip(ranked, expect):
            self.assertEqual(p[0], p[1])
    
    def test_fractional_rankings(self):
        """It correctly fractionally ranks elements."""
        series = [1,3,2,2,5,4]
        ranked = self.case.__rank__(series)
        expect = [0.0, 0.6, 0.3, 0.3, 1.0, 0.8]
        for p in zip(ranked, expect):
            self.assertEqual(p[0], p[1])

    def tearDown(self):
        pass

class ReferenceSpec(unittest.TestCase):
    """Describe the reference time series class."""
    
    def setUp(self):
        self.case = R.Reference(range(0,24,2),24,0)

    def test_initialization(self):
        """It returns an instance upon initialization."""
        self.assertTrue(isinstance(self.case, R.Reference))
        
        self.assertEqual(self.case.period, 24)
        self.assertEqual(self.case.offset, 0)
        
        self.assertTrue(isinstance(self.case.series, np.ndarray))
        self.assertTrue(isinstance(self.case.signs, np.ndarray))
    
    def test_data_series(self):
        """It builds a rank-valued periodic time series."""
        self.assertEqual(len(self.case.series), 12)
        for i,s, in enumerate(self.case.series):
            self.assertTrue(s >= 0 and s <= 1)
            if i == 0:
                continue
            elif i <= 6:
                # descending part of sinusoid
                self.assertTrue(s <= self.case.series[i-1])
            elif i > 6:
                # ascending part of sinusoid
                self.assertTrue(s >= self.case.series[i-1])
            else:
                pass
    
    def test_ranked_series(self):
        """It stores a sign-valued periodic time series."""
        self.assertEqual(len(self.case.signs), 12)
        for s in self.case.signs:
            self.assertTrue(s in (-1,0,1))
        
    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
