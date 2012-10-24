#!/usr/bin/epython

import sys
import os.path

p = os.path.realpath(__file__)
q = os.path.split(os.path.dirname(p))
sys.path.append(os.path.join(q[0], "src"))
del p, q # keep globals clean

import unittest
from jtkcycle import JTKCycle
import random
import numpy as np

class JTKCycleSpec(unittest.TestCase):
    """Describe the complete reference collection class.
       It is a parent cache for individual reference time series."""
    
    def setUp(self):
        self.case = JTKCycle(24, 2*np.ones(12), 2, None)
    
    def test_initialization(self):
        """It should appropriately initialize an instance."""
        self.assertTrue(isinstance(self.case, JTKCycle))
        self.assertEqual(self.case.period, 24)
        self.assertEqual(self.case.interval, 2)
        
        self.assertEqual(len(self.case.timerange), 12)
        self.assertEqual(len(self.case.time_reps), 12)
        
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
        self.assertEqual(N, 24)
        self.assertEqual(offsets, range(24))
        self.assertEqual(len(self.case.references), 24)
    
    def test_run(self):
        """Top-level call iterates sequence through reference cycle."""
        series = np.zeros(24, dtype='float')
        (offset, k_score) = self.case.run(series)
        self.assertEqual(len(self.case.results), 24)
    
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
