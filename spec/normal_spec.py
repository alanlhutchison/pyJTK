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
    def setUp(self):
        pass
    
    def test_score_bounds(self):
        times = u.make_times(10,1.0)
        case = nd.NormalDistribution(times)
        
        c_maximum = 45.0
        c_expected = 22.5
        
        self.assertEqual(case.max_score, c_maximum)
        self.assertEqual(case.expected, c_expected)
    
    def test_standard_deviations(self):
        times = u.make_times(5,2)
        case = nd.NormalDistribution(times)
        
        c_stdev = sqrt((2300. - 5.*28.) / 72.0)
        
        self.assertEqual(case.stdev, c_stdev)
    
    def test_p_values(self):
        times = u.make_times(10,1.0)
        case = nd.NormalDistribution(times)
        
        self.assertEqual(case.p_value(None), 1.0)
        # need to test the right cases here...
    
    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
