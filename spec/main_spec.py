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

from main import JTKCycleRun

TEST_N = 12

class JTKCycleRun_Spec(unittest.TestCase):
    """Describe the JTK Cycle Runner class... """
    
    def setUp(self):
        self.case = JTKCycleRun(TEST_N,1,None,1.0)
    
    def test_initialization(self):
        """It should initialize correctly, and memoize appropriate
           initialization parameters."""
        self.assertTrue(isinstance(self.case, JTKCycleRun))
        self.assertEqual(self.case.periods, None)
        self.assertEqual(self.case.interval, 1.0)
    
    def tearDown(self):
        pass

class RunSeriesSpec(unittest.TestCase):
    """Describe the JTK Cycle Behaviour."""
    
    def setUp(self):
        self.case = JTKCycleRun(TEST_N,1,[4,6,8,10,12],2.0)
    
    def _generate_series(self, period):
        pihat = round(np.pi,4)
        factor = 2 * pihat / period
        times = 2.0 * np.array(range(TEST_N))
        times = times * factor
        series = np.cos(times)
        return series
    
    def test_run(self):
        """It should correctly estimate best periods of signal."""
        period = random.choice([8,12,16,20,24])
        series = self._generate_series(period)
        cperiod, coffset, k_score, p_value = self.case.run(series)
        self.assertEqual(period,cperiod)
    
    def tearDown(self):
        pass

class BonferroniSpec(unittest.TestCase):
    def setUp(self):
        periods = [random.randint(1,10) for i in range(5)]
        self.case = JTKCycleRun(12,1,periods)
        self.factor = sum(periods)
    
    def test_bonferroni(self):
        """It should apply a Bonferroni correction."""
        score = random.random() / self.factor
        expect = score * self.factor
        actual = self.case.bonferroni_adjust(score)
        self.assertEqual(expect, actual)

if __name__ == "__main__":
    unittest.main()
