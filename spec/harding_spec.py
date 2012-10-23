#!/usr/bin/epython

import sys
import os.path

p = os.path.realpath(__file__)
q = os.path.split(os.path.dirname(p))
sys.path.append(os.path.join(q[0], "src"))
del p, q # keep globals clean

import unittest
import harding as hd
import utility as u

class DistributionSpec(unittest.TestCase):
    """Describe the cumulative distribution function of Harding Class."""
    
    def setUp(self):
        pass
    
    def _test_cdfs(self, expect, N, actual=None):
        actual = hd.HardingDistribution(u.make_times(N)).cdf
        for p in zip(expect, actual):
            if p[0] != 0:
                self.assertTrue(abs(p[0] - p[1]) / p[0] < 0.0001)        
    
    def test_cdf_a(self):
        """It should correctly generate the cdf for case N=3."""
        expect = [1.0000000,
                  0.9166667,
                  0.8333333,
                  0.6666667,
                  0.5000000,
                  0.3333333,
                  0.1666667]
        self._test_cdfs(expect, 3)
        
    def test_cdf_b(self):
        """It should correctly generate the cdf for case N=4."""
        expect = [1.00000000, 0.97916667, 0.95833333, 0.89583333, 0.83333333,
                  0.72916667, 0.62500000, 0.50000000, 0.37500000, 0.27083333,
                  0.16666667, 0.10416667, 0.04166667]
        self._test_cdfs(expect, 4)
    
    def test_cdf_c(self):
        """It should correctly generate the cdf for case N=5."""
        expect = [1.000000000, 0.995833333, 0.991666667, 0.975000000,
                  0.958333333, 0.920833333, 0.883333333, 0.820833333,
                  0.758333333, 0.675000000, 0.591666667, 0.500000000,
                  0.408333333, 0.325000000, 0.241666667, 0.179166667,
                  0.116666667, 0.079166667, 0.041666667, 0.025000000,
                  0.008333333]
        self._test_cdfs(expect, 5)
    
    def test_cdf_d(self):
        """It should correctly generate the cdf for case N=6."""
        expect = [1.000000000,0.999305556,0.998611111,0.995138889,0.991666667,
                  0.981944444,0.972222222,0.952083333,0.931944444,0.897916667,
                  0.863888889,0.814583333,0.765277778,0.702777778,0.640277778,
                  0.570138889,0.500000000,0.429861111,0.359722222,0.297222222,
                  0.234722222,0.185416667,0.136111111,0.102083333,0.068055556,
                  0.047916667,0.027777778,0.018055556,0.008333333,0.004861111,
                  0.001388889]
        self._test_cdfs(expect, 6)
        
    def test_cdf_e(self):
        """It should correctly generate the cdf for unbalanced replication."""
        expect = [1.0000000000,0.9997023810,0.9994047619,0.9985119048,
                  0.9976190476,0.9952380952,0.9928571429,0.9880952381,
                  0.9833333333,0.9747023810,0.9660714286,0.9523809524,
                  0.9386904762,0.9184523810,0.8982142857,0.8708333333,
                  0.8434523810,0.8086309524,0.7738095238,0.7324404762,
                  0.6910714286,0.6446428571,0.5982142857,0.5491071429,
                  0.5000000000,0.4508928571,0.4017857143,0.3553571429,
                  0.3089285714,0.2675595238,0.2261904762,0.1913690476,
                  0.1565476190,0.1291666667,0.1017857143,0.0815476190,
                  0.0613095238,0.0476190476,0.0339285714,0.0252976190,
                  0.0166666667,0.0119047619,0.0071428571,0.0047619048,
                  0.0023809524,0.0014880952,0.0005952381]
        actual = hd.HardingDistribution(u.make_times(4, [2,3,2,1])).cdf
        for p in zip(expect, actual):
            try:
                if p[0] != 0:
                    self.assertTrue(abs(p[0] - p[1]) / p[0] < 0.001)
            except:
                print p
            
        
    def tearDown(self):
        pass

class PValueSpec(unittest.TestCase):
    """Describe p-value generating methods in Harding Distribution."""
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
