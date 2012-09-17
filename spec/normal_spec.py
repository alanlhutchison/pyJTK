#!/usr/bin/epython

import sys
import os.path

p = os.path.realpath(__file__)
q = os.path.split(os.path.dirname(p))
sys.path.append(os.path.join(q[0], "src"))
del p, q # keep globals clean

import unittest
import numpy as np
import normal as nd
import utility as u
from math import sqrt

class DistributionSpec(unittest.TestCase):
    """describe normal distribution approximation"""
    
    def setUp(self):
        pass
    
    def test_score_bounds(self):
        """it calculates the correct maximum and expected scores"""
        times = u.make_times(10,1.0)
        case = nd.NormalDistribution(times)
        
        c_maximum = 45.0
        c_expected = 22.5
        
        self.assertEqual(case.max_score, c_maximum)
        self.assertEqual(case.expected, c_expected)
    
    def test_standard_deviations(self):
        """it computes a reasonable approximation of the standard dev."""
        times = u.make_times(5,2)
        case = nd.NormalDistribution(times)
        
        c_stdev = sqrt((2300. - 5.*28.) / 72.0)
        
        self.assertEqual(case.stdev, c_stdev)
    
    def test_p_values(self):
        """it computes appropriate p-values for elements in distribution"""
        times = u.make_times(10,1.0)
        case = nd.NormalDistribution(times)
        
        self.assertEqual(case.p_value(None), 1.0)
        
        # TODO: ANDY! YOU NEED TO TEST THE RIGHT CASES HERE.
        #       TAKE SOME TIME TO CHOOSE THE RIGHT TESTS.
    
    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
