#!/usr/bin/epython

import sys
import os.path

p = os.path.realpath(__file__)
q = os.path.split(os.path.dirname(p))
sys.path.append(os.path.join(q[0], "src"))
del p, q # keep globals clean

import unittest
import shewchuk
import random

class TwoSumSpec(unittest.TestCase):
    def test_integer(self):
        n = random.randint(1,10)
        m = random.randint(1,10)
        expect = n+m
        self.assertEqual(shewchuk.two_sum(n,m), expect)
    
    def test_truncated_float(self):
        n = random.randint(1,10)
        m = random.randint(1,10)
        expect = n+m
        self.assertEqual(shewchuk.two_sum(float(n),float(m)), float(expect))
    
    def test_float(self):
        n = round(10*random.random(),1)
        m = round(10*random.random(),1)
        expect = n+m
        actual = shewchuk.two_sum(n,m)
        if isinstance(actual,tuple):
            self.assertEqual(actual[0],expect)
        else:
            self.assertEqual(actual,expect)

class FastTwoSumSpec(unittest.TestCase):
    def test_float(self):
        n = round(10*random.random(),1)
        m = round(10*random.random(),1)
        expect = n+m
        actual = shewchuk.two_sum(n,m)
        if isinstance(actual, tuple):
            self.assertEqual(actual[0],expect)
        else:
            self.assertEqual(actual,expect)

class ExpansionSum(unittest.TestCase):
    def test_empty(self):
        self.assertEqual((None, 0.0), shewchuk.expansion_sum([]))
    
    def test_singleton(self):
        n = 10*random.random()
        self.assertEqual((None, n), shewchuk.expansion_sum([n]))
    
    def test_integers(self):
        l = [random.randint(1,10) for i in range(10)]
        self.assertEqual(sum(l), shewchuk.expansion_sum(l)[1])
    
    def test_truncated_float(self):
        l = [random.randint(1,10) for i in range(10)]
        self.assertEqual(float(sum(l)), shewchuk.expansion_sum(map(float,l))[1])
    
    def test_float(self):
        l = [round(10*random.random(),1) for i in range(10)]
        expect = sum(l)
        actual = shewchuk.expansion_sum(l)
        if isinstance(actual, tuple):
            self.assertEqual(round(actual[1],1),round(expect,1))
        else:
            self.assertEqual(actual,expect)

if __name__ == "__main__":
    unittest.main()
