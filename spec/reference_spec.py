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
    
    def test_rankings(self):
        """It correctly rank-orders elements in a time-series."""
        series = [5,3,2,1,4,6]
        ranked = self.case.__rank__(series)
        expect = [0.8, 0.4, 0.2, 0.0, 0.6, 1.0]
        for p in zip(ranked, expect):
            self.assertEqual(p[0], p[1])
        
    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
