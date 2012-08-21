#!/usr/bin/epython

import sys
import os.path

p = os.path.realpath(__file__)
q = os.path.split(os.path.dirname(p))
sys.path.append(os.path.join(q[0], "src"))
del p, q # keep globals clean

import unittest
import normal_distribution as nd

class DistributionSpec(unittest.TestCase):
    pass

if __name__ == "__main__":
    unittest.main()
