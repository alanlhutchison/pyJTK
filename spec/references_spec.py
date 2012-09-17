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

class SeriesMakerSpec(unittest.TestCase):
    """Describe reference series factory method."""
    
    def setUp(self):
        n = 12
        pers = [12]
        times = 2.0 * np.ones(n)
        inter = 2.0
        
        self.case = R.References(pers, times, inter)

    def _get_spec(self):
        per = random.randint(5,12)
        off = random.choice(range(per))
        return (per,off)
    
    def test_ranked_series(self):
        """It can be used to build rank-ordered series w. period/phase."""
        per,off = self._get_spec()
        series = self.case.make_series(per,off)
        for val in series:
            self.assertTrue(val >= 0.0 and val <= 1.0)
        
        self.assertEqual(len(series), 24)
        self._test_duplication(series)
    
    def test_signed_series(self):
        """It can be used to build sign-valued series with period/phase."""
        per,off = self._get_spec()
        series = self.case.make_series(per,off,signed=True)
        for idx,val in enumerate(series):
            self.assertTrue(val in (-1.0, 0.0, 1.0))
        
        self.assertEqual(len(series), 24)
        self._test_duplication(series)
    
    def test_truncated_series(self):
        """It can be used to generate shortened versions of time-series."""
        per,off = self._get_spec()
        aseries = self.case.make_series(per,off,signed=True,tlim=per)
        bseries = self.case.make_series(per,off,tlim=per)
        
        self.assertEqual(len(aseries), per*2)
        self.assertEqual(len(bseries), per*2)
        
        self._test_duplication(aseries)
        self._test_duplication(bseries)
        
    def _test_duplication(self, series):
        for i in range(len(series)/2):
            self.assertEqual(series[2*i],series[2*i+1])
        
    def tearDown(self):
        pass

class ReferencesSpec(unittest.TestCase):
    """Describe reference series generator class."""
    
    def setUp(self):
        n = 12
        pers = range(5,12)
        times = 2.0 * np.ones(n)
        inter = 1.0
        
        self.case = R.References(pers, times, inter)        
    
    def test_initialization(self):
        """It returns an instance upon initialization."""
        self.assertTrue(isinstance(self.case, R.References))
    
    def test_make_series(self):
        """It builds a time-series when needed."""
        period = random.choice(range(5,12))
        series = self.case.make_series(period,0.0)
        
        self.assertEqual(24, len(series))
        self.assertEqual(series[0.0], 1.0)

    def test_ranks(self):
        """It correctly rank-orders elements in a time-series."""
        series = [10.0*random.random() for i in range(20)]
        ranked = self.case.ranks(series)
        
        for rank in ranked:
            self.assertTrue(rank <= 1.0 and rank >= 0.0)
            self.assertEqual(ranked.count(rank), 1)
    
    def test_series(self):
        """It has a generator that iterates over period/phase combinations."""
        N = 0
        
        for ser in self.case.series():
            self.assertEqual(24, len(ser[2]))
            
            self.assertTrue(ser[0] in range(5,12))
            self.assertTrue(ser[1] <= ser[0])
            
            if ser[1] == 0.0:
                self.assertEqual(ser[2][0], 1.0)
            N += 1
        else:
            self.assertEqual(N, sum(range(5,12)))
        
    
    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
