#!/usr/bin/epython

import sys
import os.path

p = os.path.realpath(__file__)
q = os.path.split(os.path.dirname(p))
sys.path.append(os.path.join(q[0], "src"))
del p, q # keep globals clean

import unittest
import numpy as np
import waveforms as w

class ProperDomainSpec(unittest.TestCase):
    """Describe re-domaining function to normalize argument x to [0,2*pi]."""

    def test_left_boundary(self):
        """It should return zero for zero."""
        self.assertEqual(w.__make_proper__(0), 0)

    def test_right_boundary(self):
        """It should wrap two pi in the domain to zero."""
        self.assertEqual(w.__make_proper__(2*np.pi), 0.0)

    def test_intermediate_value(self):
        """It should leave intermediate values unchanged."""
        test = np.random.random() * (2*np.pi - 0.0001)
        self.assertEqual(test, w.__make_proper__(test))

    def test_under_bounds(self):
        """It should return the elements as properly domained."""
        test = -4 * np.pi + np.pi + np.pi / 8
        expect = 9 * np.pi / 8
        self.assertEqual(round(w.__make_proper__(test),4), round(expect,4))

    def test_over_bounds(self):
        """It should return the element as properly domained."""
        test = 4 * np.pi - np.pi / 8
        expect = 15 * np.pi / 8
        self.assertEqual(round(w.__make_proper__(test),4), round(expect,4))

    def test_series(self):
        """It should preserver sequence properties but redomain."""
        make = np.frompyfunc(w.__make_proper__,1,1)
        test = np.linspace(-4 * np.pi, 4 * np.pi, 100)
        result = make(test)
        self.assertEqual(len(result), len(test))
        for v in result:
            self.assertTrue(v >= 0 and v <= 2*np.pi)

class RampDownSpec(unittest.TestCase):
    """Describe the ramping down function."""

    def test_initial_value(self):
        """It should begin at a peak."""
        self.assertEqual(w.ramp_down(0.0), 1.0)

    def test_baseline(self):
        """It should have a trailing baseline."""
        ramp_down = np.frompyfunc(w.ramp_down,1,1)
        xs = np.linspace(3*np.pi/2, 2*np.pi, 100)
        ys = ramp_down(xs)
        for y in ys[:-1]:
            self.assertEqual(y, 0.0)

    def test_decreasing(self):
        """It should decrease monotonically during the ramp duration."""
        ramp_down = np.frompyfunc(w.ramp_down,1,1)
        xs = np.linspace(0.0, 3*np.pi/2, 100)
        ys = ramp_down(xs)
        for i,y in enumerate(ys[:-1]):
            self.assertTrue(y > ys[i+1])

class RampUpSpec(unittest.TestCase):
    """Describe the ramping up function."""

    def test_initial_value(self):
        """It should begin at the foot of a ramp up."""
        self.assertEqual(w.ramp_up(0.0), 0.0)

    def test_peak_value(self):
         """It should peak at the specified ramp length."""
         self.assertEqual(w.ramp_up(3*np.pi/2), 1.0)

    def test_baseline(self):
        """It should have a trailing baseline."""
        ramp_up = np.frompyfunc(w.ramp_up,1,1)
        xs = np.linspace(3*np.pi/2, 2*np.pi, 100)
        ys = ramp_up(xs)
        for y in ys[1:]:
            self.assertEqual(y, 0.0)

    def test_increasing(self):
        """It should increase monotonically during the ramp duration."""
        ramp_up = np.frompyfunc(w.ramp_up,1,1)
        xs = np.linspace(0.0, 3*np.pi/2, 100)
        ys = ramp_up(xs)
        for i,y in enumerate(ys[:-1]):
            self.assertTrue(y < ys[i+1])
    
class ImpulseSpec(unittest.TestCase):
    """Describe the impulse function."""

    def test_initial_value(self):
        """It should begin at a peak."""
        self.assertEqual(w.impulse(0.0), 1.0)

    def test_baseline(self):
        """It should be zero-valued midphase."""
        impulse = np.frompyfunc(w.impulse,1,1)
        xs = np.linspace(np.pi/4, 7*np.pi/4, 100)
        ys = impulse(xs)
        for y in ys:
            self.assertEqual(y, 0.0)

    def test_decreasing(self):
        """It should decrease monotonically following peak."""
        impulse = np.frompyfunc(w.impulse,1,1)
        xs = np.linspace(0.0, np.pi/8, 100)
        ys = impulse(xs)
        for i,y in enumerate(ys[:-1]):
            self.assertTrue(y > ys[i+1])

    def test_increasing(self):
        """It should increase monotonically before a peak."""
        impulse = np.frompyfunc(w.impulse,1,1)
        xs = np.linspace(15 * np.pi / 8, 2*np.pi, 100)
        ys = impulse(xs)
        for i,y in enumerate(ys[:-1]):
            self.assertTrue(y < ys[i+1])

class StepSpec(unittest.TestCase):
    """Describe the step function waveform."""

    def test_initial_value(self):
        """It should initialize on a peak."""
        self.assertEqual(w.step(0.0), 1.0)

    def test_step_function(self):
        """It should spend half of the phase cycle valued 1.0 and half of
           the phase cycle valued 0.0."""
        step = np.frompyfunc(w.step,1,1)
        xs = np.linspace(0,2*np.pi,100)
        ys = step(xs)
        for y in ys[:50]:
            self.assertEqual(y, 1.0)
        for y in ys[51:-1]:
            self.assertEqual(y, 0.0)
        
if __name__ == "__main__":
    unittest.main()
