#!/usr/bin/epython

import sys
import os.path

p = os.path.realpath(__file__)
q = os.path.split(os.path.dirname(p))
sys.path.append(os.path.join(q[0], "src"))
del p, q # keep globals clean

import unittest
import harding as hd

class DistributionSpec(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
