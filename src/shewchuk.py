#!/usr/bin/epython

import sys
import os.path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# http://www.cs.cmu.edu/afs/cs/project/quake/public/papers/robust-arithmetic.ps

def fast_two_sum(a,b):
    """Assumes abs(a) >= abs(b), otherwise use two_sum."""
    x = a + b
    b_virtual = x - a
    y = b - b_virtual
    if y == 0:
        return x
    else:
        return (x,y)

def two_sum(a,b):
    """Evaluates adaptive precision summation for a,b in unknown order"""
    x = a + b
    
    b_virtual = x - a
    a_virtual = x - b_virtual
    
    b_roundoff = b - b_virtual
    a_roundoff = a - a_virtual
    
    y = a_roundoff + b_roundoff
    
    if y == 0:
        return x
    else:
        return (x,y)

def expansion_sum(series):
    if len(series) == 0:
        return (None, 0.0)
    elif len(series) == 1:
        return (None, series[0])
    
    series = sorted(series, key=lambda v: abs(v))
    z = fast_two_sum(series[1], series[0])
    h = None
    
    try:
        q = z[0]
        h = z[1]
    except: # not a tuple
        q = z
    
    if len(series) == 2:
        return (h,q)
    
    for v in series[2:]:
        z = two_sum(q,v)
        try:
            q = z[0]
            h = z[1]
        except: # not a tuple
            q = z
    
    return (h,q)

if __name__ == "__main__":
    print "Adaptive precision summation algorithms."
