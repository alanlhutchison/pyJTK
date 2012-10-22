#!/usr/bin/epython

import sys
import os.path

p = os.path.realpath(__file__)
q = os.path.split(os.path.dirname(p))
sys.path.append(os.path.join(q[0], "src"))
del p, q # keep globals clean

import unittest
import numpy as np

import statistic

class StatisticSpec(unittest.TestCase):
    """Describe score factory."""
    
    def setUp(self):
        pass
    
    def test_score_trivial_a(self):
        """It should generate a zero score for flatline reference."""
        data = np.arange(12)
        ref = np.ones(12)
        expect = 0.0
        actual = statistic.k_score(data,ref)
        self.assertEqual(expect, actual)

    def test_score_trivial_b(self):
        """It should generate a zero score for flatline test series."""
        data = np.ones(12)
        ref = np.arange(12)
        expect = 0.0
        actual = statistic.k_score(data,ref)
        self.assertEqual(expect, actual)
    
    def test_score_a(self):
        """It should generate a correct score for test series A."""
        data = np.array([1,3,2,4],dtype='float')
        ref = np.arange(4)
        expect = 4.0
        actual = statistic.k_score(data,ref)
        self.assertEqual(expect, actual)
    
    def test_score_b(self):
        """It should generate a correct score for test series B."""
        data = np.array([4,3,2,1],dtype='float')
        ref = np.arange(4)
        expect = -6.0
        actual = statistic.k_score(data,ref)
        self.assertEqual(expect, actual)
    
    def test_score_c(self):
        """It should generate a correct score for test series C."""
        data = np.array([1,2,4,3],dtype='float')
        ref = np.array([3,2,1,4],dtype='float')
        expect = -2.0
        actual = statistic.k_score(data,ref)
        self.assertEqual(expect, actual)    
    
    def test_tau_vector(self):
        """It should generate appropriate pairwise relationships."""
        data = np.array([1,3,5,7,9,2,4,6,8,10],dtype='float')
        expect = np.array(
            [  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
               1, -1, -1, -1, -1,  1,  1, -1, -1, -1,
               1,  1,  1,  1, -1, -1,  1,  1,  1,  1,
               1,  1, -1,  1,  1,  1,  1,  1,  1,  1,
               1,  1,  1,  1,  1],
            dtype='float'
            )
        actual = statistic._tau_vector(data)
        for p in zip(expect, actual):
            self.assertEqual(p[0],p[1])
    
    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
