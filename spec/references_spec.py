#!/usr/bin/epython

import sys
import os.path

p = os.path.realpath(__file__)
q = os.path.split(os.path.dirname(p))
sys.path.append(os.path.join(q[0], "src"))
del p, q # keep globals clean

import unittest
import references as R
import random
import numpy as np

class ReferencesSpec(unittest.TestCase):
    
    def setUp(self):
        n = 12
        pers = range(5,12)
        times = 2.0 * np.ones(n)
        inter = 1.0
        
        self.case = R.References(pers, times, inter)        
    
    def test_initialization(self):
        self.assertTrue(isinstance(self.case, R.References))
    
    def test_series(self):
        for ser in self.case.series():
            self.assertEqual(24, len(ser[2]))
            self.assertTrue(ser[0] in range(5,12))
            self.assertTrue(ser[1] <= ser[0])
            if ser[1] == 0.0:
                self.assertEqual(ser[2][0], 1.0)
    
    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
