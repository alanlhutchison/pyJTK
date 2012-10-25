#!/usr/bin/epython

import sys
import os.path

p = os.path.realpath(__file__)
q = os.path.split(os.path.dirname(p))
sys.path.append(os.path.join(q[0], "src"))
r = os.path.dirname(os.path.realpath(__file__))
del p, q # keep globals clean

import numpy as np
import random
import unittest

import parsed as p

class AcceptanceSpec(unittest.TestCase):
    """Describe correct use of the metadataset header."""
    
    def setUp(self):
        f = open(r + "/header.ldz", "r")
        self.case = p.DataParser(f)
    
    def test_times(self):
        self.assertEqual(self.case.n_times, 12)
    
    def test_reps(self):
        self.assertEqual(self.case.reps, [8,2,8,2,8,2,6,2,7,2,8,2])
    
    def test_interval(self):
        self.assertEqual(self.case.interval, 1)
    
    def test_timerange(self):
        self.assertEqual(self.case.timerange, [0,1,4,5,8,9,12,13,16,17,20,21])
        
    def tearDown(self):
        pass


class ArgumentsSpec(unittest.TestCase):
    """Describe the parser's ability to correctly determine initialization
       arguments for JTKCycleRun class."""
    
    def setUp(self):
        f = open(r + "/header.mock", "r")
        self.case = p.DataParser(f)
    
    def test_times(self):
        self.assertEqual(self.case.n_times, 4)
    
    def test_reps(self):
        self.assertEqual(self.case.reps, [2,2,3,3])
    
    def test_interval(self):
        self.assertEqual(self.case.interval, 2)
    
    def test_timerange(self):
        self.assertEqual(self.case.timerange, None)
    
    def tearDown(self):
        pass

class UtilitiesSpec(unittest.TestCase):
    """Describe some parsing utility methods."""
    
    def setUp(self):
        f = open(r + "/header.mock", "r")
        self.case = p.DataParser(f)
    
    def test_get_ZT_time(self):
        """It should correctly find the ZT times or return None."""
        self.assertEqual(self.case.get_ZT_time("GiulianiZT16"), 16)
        self.assertEqual(self.case.get_ZT_time("NA"), None)
    
    def test_uniques(self):
        """It should correctly identify the unique elements of iterable."""
        self.assertEqual(self.case.__uniques__("ABBA"), ["A", "B"])
        self.assertEqual(self.case.__uniques__([1,2,3,4,4,3,2,1]), [1,2,3,4])
    
    def test_intervals(self):
        """It should correctly compute the intervals between elements."""
        data = [2,3,5,7,11,13]
        expect = [1,2,2,4,2]
        actual = self.case.__intervals__(data).tolist()
        self.assertEqual(expect, actual)
    
    def tearDown(self):
        pass

class PatterningSpec(unittest.TestCase):
    """Describe active repatterning feature of the parser."""
    
    def setUp(self):
        f = open(r + "/header.mock", "r")
        self.case = p.DataParser(f)
    
    def test_pattern(self):
        """It should correctly assign indices to the corresponding times."""
        expect = [
            (0, [0, 6]),
            (2, [2, 5]),
            (4, [1, 4, 9]),
            (6, [3, 7, 8])
            ]
        actual = self.case.pattern
        self.assertEqual(expect, actual)

    def test_repattern(self):
        """It should appropriately repattern input series."""
        data = "AECHFDBIJG"
        expect = "ABCDEFGHIJ"
        actual = "".join(self.case.repattern(data))
        self.assertEqual(expect, actual)
    
    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
