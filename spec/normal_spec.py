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
        
    def tearDown(self):
        pass

class SmallUnequalSpec(unittest.TestCase):
    """Generated test from R-script, compares expected p-values."""
    
    def setUp(self):
        self.case = nd.NormalDistribution(
            u.make_times(4, [2,3,5,4])
            )
    
    def test_initialization(self):
        """It should provide the correct parameters for the distribution."""
        self.assertEqual(round(self.case.stdev, 2), 8.71)
        self.assertEqual(round(self.case.max_score), 71.)
        self.assertEqual(round(self.case.expected, 1), 35.5)
    
    def test_p_values(self):
        """It should compute appropriate p-values given a set of scores."""
        # 6.055271e-01 1.045762e+00 6.461744e-01 1.684351e-01 2.013015e-17
        self.assertEqual(round(self.case.p_value(-10),2), 0.61)
        self.assertEqual(round(self.case.p_value(0),2), 1.0)
        self.assertEqual(round(self.case.p_value(9),2), 0.65)
        self.assertEqual(round(self.case.p_value(25),2), 0.17)
        self.assertEqual(round(self.case.p_value(149),2), 0.00)
    
    def tearDown(self):
        pass

class LargeUnequalSpec(unittest.TestCase):
    """Generated test from R-script, compares expected p-values."""
    
    def setUp(self):
        self.case = nd.NormalDistribution(
            u.make_times(12, [8,2,8,2,8,2,6,2,7,2,8,2])
            )
    
    def test_initialization(self):
        """It should provide the correct parameters for the distribution."""
        self.assertEqual(round(self.case.stdev), 72.)
        self.assertEqual(round(self.case.max_score), 1442.)
        self.assertEqual(round(self.case.expected), 721.)
    
    def test_p_values(self):
        """It should compute appropriate p-values given a set of scores."""
        # 4.920460e-01 1.005537e+00 4.964295e-01 8.397821e-02 4.294873e-25
        self.assertEqual(round(self.case.p_value(-100),2), 0.49)
        self.assertEqual(round(self.case.p_value(0),2), 1.0)
        self.assertEqual(round(self.case.p_value(99),2), 0.50)
        self.assertEqual(round(self.case.p_value(250),2), 0.08)
        self.assertEqual(round(self.case.p_value(1492),2), 0.00)
    
    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
