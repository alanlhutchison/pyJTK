#!/usr/bin/epython

import sys
import os.path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import numpy as np

def __make_proper__(x):
    d = np.floor(x / (2. * np.pi))
    return x - d*2.*np.pi

def ramp_down(x, w=None):
    if w == None:
        w = 3*np.pi/2
    x = __make_proper__(x)
    y = max(-1.*x/w + 1.0, 0.0)
    return y

def ramp_up(x, w=None):
    if w == None:
        w = 3*np.pi/2
    x = __make_proper__(x)
    y = x/w if x <= w else 0.0
    return y

def impulse(x, w=None):
    if w == None:
        w = 3*np.pi/4
    x = __make_proper__(x)
    d = min(x, np.abs(np.pi*2 - x))
    y = max(-2.*d/w + 1.0, 0.0)
    return y

def step(x, w=None):
    if w == None:
        w = np.pi
    x = __make_proper__(x)
    y = 1.0 if x < w else 0.0
    return y

if __name__ == "__main__":
    print "This module holds custom waveforms for JTK Cycle analysis."
