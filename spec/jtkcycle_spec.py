#!/usr/bin/epython

import sys
import os.path

p = os.path.realpath(__file__)
q = os.path.split(os.path.dirname(p))
sys.path.append(os.path.join(q[0], "src"))
del p, q # keep globals clean

import unittest
from jtkcycle import JTKCycle
import statistic
import random
import numpy as np

class JTKCycleSpec(unittest.TestCase):
    """Describe the complete reference collection class.
       It is a parent cache for individual reference time series."""
    
    def setUp(self):
        self.case = JTKCycle(24, 2*np.ones(12), np.arange(0,24,2), 2)
    
    def test_initialization(self):
        """It should appropriately initialize an instance."""
        self.assertTrue(isinstance(self.case, JTKCycle))
        self.assertEqual(self.case.period, 24)
        self.assertEqual(self.case.density, 2)
        
        self.assertEqual(len(self.case.timepoints), 12)
        self.assertEqual(len(self.case.reps), 12)
        
        self.assertEqual(self.case.best, None)
        
    def test_reference_generation(self):
        """It should generate appropriate reference instances."""
        N = 0
        offsets = []
        
        # check lazy instantiation.
        self.assertEqual(len(self.case.references), 0)
        
        for reference in self.case.generate_references():
            N += 1
            offsets.append(reference.offset)
        
        # check population and memoization.
        self.assertEqual(N, 12)
        self.assertEqual(offsets, range(0,24,2))
        self.assertEqual(len(self.case.references), 12)
    
    def test_run(self):
        """Top-level call iterates sequence through reference cycle."""
        series = np.zeros(24, dtype='float')
        q = statistic._tau_vector(series)
        
        (offset, k_score) = self.case.run(q)
        self.assertEqual(len(self.case.results), 12)
    
    def test_expansion(self):
        """It should appropriately expand a time series based on time_reps."""
        expect = np.array([ 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5,
                            6, 6, 7, 7, 8, 8, 9, 9,10,10,11,11],
                          dtype='float')
        actual = self.case.__expand__(np.arange(12, dtype='float'))
        for p in zip(expect, actual):
            self.assertEqual(p[0], p[1])
    
    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
