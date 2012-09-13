#!/usr/bin/epython

import sys
import os.path

p = os.path.realpath(__file__)
q = os.path.split(os.path.dirname(p))
sys.path.append(os.path.join(q[0], "src"))
del p, q # keep globals clean

import numpy as np
import random
import unittest

from main import JTKCYCLE

TEST_N = 12
# write some test cases here.

class JTKCYCLE_Spec(unittest.TestCase):
    def setUp(self):
        self.case = JTKCYCLE(TEST_N,1,None,1.0)
    
    def test_initialization(self):
        self.assertTrue(isinstance(self.case,JTKCYCLE))
        
        self.assertEqual(self.case.timepoints, TEST_N)
        self.assertEqual(self.case.periods, None)
        self.assertEqual(self.case.interval, 1.0)
    
    def tearDown(self):
        pass

class RunSeriesSpec(unittest.TestCase):
    def setUp(self):
        self.case = JTKCYCLE(TEST_N,1,range(6,13),2.0)
    
    def _generate_series(self, period):
        pihat = round(np.pi,4)
        times = np.array(range(TEST_N), dtype='float')
        times = times * 2 * pihat / period
        
        series = np.cos(times)
        return series
    
    def test_run(self):
        for per in range(6,13):
            ser = self._generate_series(per)
            cper,coff,camp,ctau = self.case.run_series(ser)
            self.assertEqual(per,cper)
    
    def tearDown(self):
        pass

class BonferroniSpec(unittest.TestCase):
    def setUp(self):
        self.case = JTKCYCLE(12,1,None)
    
    def test_bonferroni(self):
        n = random.randint(10,50)
        ser = [10 * random.random() for i in range(n)]
        
        expect = np.array([s/float(n) for s in ser],dtype='float')
        actual = self.case._bonferroni(ser)
        
        for p in zip(expect,actual):
            self.assertEqual(p[0], p[1])
    
    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
