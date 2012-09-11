#!/usr/bin/epython

import sys
import os.path

p = os.path.realpath(__file__)
q = os.path.split(os.path.dirname(p))
sys.path.append(os.path.join(q[0], "src"))
del p, q # keep globals clean

import unittest
import numpy as np
import normal_distribution as nd
from math import sqrt

class DistributionSpec(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_initialization_with_int(self):
        case = nd.NormalDistribution(6,1)
        self.assertTrue(isinstance(case,nd.NormalDistribution))
    
    def test_initialization_with_array(self):
        case = nd.NormalDistribution(6,np.array([1.0]))
        self.assertTrue(isinstance(case,nd.NormalDistribution))
    
    def test_score_bounds(self):
        case = nd.NormalDistribution(10,1.0)
        
        c_maximum = 45.0
        c_expected = 22.5
        
        self.assertEqual(case.max_score, c_maximum)
        self.assertEqual(case.expected, c_expected)
    
    def test_standard_deviations(self):
        case = nd.NormalDistribution(5,2)
        
        c_stdev = sqrt((2300. - 5.*28.) / 72.0)
        
        self.assertEqual(case.stdev, c_stdev)
    
    def test_p_values(self):
        case = nd.NormalDistribution(10,1.0)
        
        self.assertEqual(case.p_value(None), 1.0)
        # need to test the right cases here...
    
    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
