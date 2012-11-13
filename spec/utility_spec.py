#!/usr/bin/epython

import sys
import os.path

p = os.path.realpath(__file__)
q = os.path.split(os.path.dirname(p))
sys.path.append(os.path.join(q[0], "src"))
del p, q # keep globals clean

import unittest
import numpy as np
import utility as u
import random

class AmplitudeSpec(unittest.TestCase):
    """Describe amplitude estimation utility."""
    
    def test_trivial(self):
        """It should return 0 for a constant series."""
        vals = np.ones(12)
        expect = 0
        actual = u.est_amp(vals)
        self.assertEqual(expect, actual)
    
    def test_sinusoid(self):
        """It should return approximately the correct amplitude of a sine."""
        vals = np.sin(np.arange(100) / (10 * np.pi))
        expect = 2.0
        actual = u.est_amp(vals)
        self.assertTrue(actual < 2 * expect)
        self.assertTrue(actual > 0.5 * expect)
    
    def test_random(self):
        """It should return approximately the correct amplitude for noise."""
        vals = 10 * np.random.random(35)
        expect = 10
        actual = u.est_amp(vals)
        self.assertTrue(actual < 2 * expect)
        self.assertTrue(actual > 0.5 * expect)
        

class TimesSpec(unittest.TestCase):
    """Describe timereps array utility"""
    
    def test_integer(self):
        """It takes an integer to represent uniform replication."""
        points = np.arange(12,dtype='float')
        reps = random.randint(1,10)
        
        expect = reps * np.ones(12,dtype='float')
        actual = u.make_times(points,reps)
        
        for p in zip(expect,actual):
            self.assertEqual(p[0], p[1])
    
    def test_singleton(self):
        """It pulls zeroth from singleton array (less than N elem.)."""
        points = np.arange(12,dtype='float')
        reps = np.array([random.randint(1,10)],dtype='float')
        
        expect = reps[0] * np.ones(12,dtype='float')
        actual = u.make_times(points,reps)
        
        for p in zip(expect,actual):
            self.assertEqual(p[0], p[1])
    
    def test_full(self):
        """It uses provided replication array when lengths are matching."""
        points = 12
        reps = np.array([random.randint(1,10) for i in range(12)],dtype='float')
        
        expect = reps
        actual = u.make_times(points,reps)
        
        for p in zip(expect,actual):
            self.assertEqual(p[0],p[1])
        
if __name__ == "__main__":
    unittest.main()
