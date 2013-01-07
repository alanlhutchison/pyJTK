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
from harding import HardingDistribution
from normal import NormalDistribution

TEST_N = 12

class JTKCycleRun_Spec(unittest.TestCase):
    """Describe the JTK Cycle Runner class... """
    
    def setUp(self):
        self.case = JTKCycleRun(np.ones(TEST_N),
                                2*np.arange(TEST_N),
                                None,
                                2)
    
    def test_initialization(self):
        """It should initialize correctly, and memoize appropriate
           initialization parameters."""
        self.assertTrue(isinstance(self.case, JTKCycleRun))
        self.assertEqual(self.case.periods, None)
        self.assertEqual(self.case.density, 2)
    
    def tearDown(self):
        pass

class DistributionSelectionSepc(unittest.TestCase):
    """Describe the Null Distribution boolean selector."""
    
    def test_gaussian_distribution(self):
        case = JTKCycleRun(np.ones(TEST_N),
                           2*np.arange(TEST_N),
                           None,
                           2,
                           normal=True)
        self.assertTrue(isinstance(case.distribution, NormalDistribution))
    
    def test_exact_distribution(self):
        case = JTKCycleRun(np.ones(TEST_N),
                           2*np.arange(TEST_N),
                           None,
                           2,
                           normal=False)
        self.assertTrue(isinstance(case.distribution, HardingDistribution))
    
    

class RunSeriesSpec(unittest.TestCase):
    """Describe the JTK Cycle Behaviour."""
    
    def setUp(self):
        self.case = JTKCycleRun(np.ones(TEST_N),
                                2 * np.arange(TEST_N),
                                [8,12,16,20,24],
                                2,
                                normal=False)
    
    def _generate_series(self, period):
        pihat = round(np.pi,4)
        factor = 2 * pihat / period
        times = 2 * np.arange(TEST_N)
        times = times * factor
        series = np.cos(times)
        return series
    
    def test_run(self):
        """It should correctly estimate best periods of signal."""
        period = random.choice([8,12,16,20,24])
        series = self._generate_series(period)
        camp, cperiod, coffset, k_score, p_value = self.case.run(series)
        self.assertEqual(period,cperiod)
    
    def tearDown(self):
        pass

class BonferroniSpec(unittest.TestCase):
    def setUp(self):
        periods = [random.randint(1,10) for i in range(5)]
        self.case = JTKCycleRun(np.ones(TEST_N),2*np.arange(TEST_N),periods,2)
        self.factor = sum(periods)
    
    def test_bonferroni(self):
        """It should apply a Bonferroni correction."""
        score = random.random() / self.factor
        expect = score * self.factor
        actual = self.case.bonferroni_adjust(score)
        self.assertEqual(expect, actual)

if __name__ == "__main__":
    unittest.main()
