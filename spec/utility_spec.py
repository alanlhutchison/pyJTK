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
