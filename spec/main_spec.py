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
        """It should initialize correctly, and memoize initialization values."""
        self.assertTrue(isinstance(self.case,JTKCYCLE))
        
        self.assertEqual(self.case.timepoints, TEST_N)
        self.assertEqual(self.case.periods, None)
        self.assertEqual(self.case.interval, 1.0)
    
    def tearDown(self):
        pass

class EstAmpSpec(unittest.TestCase):
    def setUp(self):
        self.case = JTKCYCLE(TEST_N,1,None,1.0)
    
    def _generate_series(self, amp, per):
        pihat = round(np.pi,4)
        times = np.array(range(TEST_N), dtype='float')
        times = np.array(times * 2 * pihat / per, dtype='float')
        
        series = amp * np.cos(times)
        return series
    
    def test_estimation(self):
        """It should correctly estimate amplitudes of the signal."""
        for amp in map(float, range(1,15)):
            per = 12
            ser = self._generate_series(amp,per)
            
            camp = self.case.est_amp(ser, per, 0.0, 1.0)
            self.assertEqual(round(camp),amp)
    
    def tearDown(self):
        pass

class RunSeriesSpec(unittest.TestCase):
    def setUp(self):
        self.case = JTKCYCLE(TEST_N,1,range(6,13),2.0)
    
    def _generate_series(self, period, offset):
        pihat = round(np.pi,4)
        factor = 2 * pihat / period
        
        times = np.array(range(TEST_N))
        times = times * factor
        
        times = times + (0.5 * offset * factor)
        
        series = np.cos(times)
        return series
    
    def test_run(self):
        """It should correctly estimate best periods and offsets of signal."""
        for per in range(6,13):
            off = random.choice(range(per))
            
            ser = self._generate_series(per,off)
            cper,coff,camp,ctau = self.case.run_series(ser)
            
            self.assertEqual(per,cper)
            self.assertEqual(off,coff)
    
    def tearDown(self):
        pass

class BonferroniSpec(unittest.TestCase):
    def setUp(self):
        self.case = JTKCYCLE(12,1,None)
    
    def test_bonferroni(self):
        """It should apply a Bonferroni correction."""
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
