#!/usr/bin/epython

import sys
import os.path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import numpy as np
import math

def make_times(timepoints, reps=1):
    """Generates an appropriately formatted timereps array.
       Times contains repeated indexes corresponding to replicates."""
    
    try:
        if len(reps) == timepoints:
            times = np.array(reps)
        else:
            times = reps[0] * np.ones(timepoints, dtype='float')
    
    except: # reps is not array-like
        times = reps * np.ones(timepoints, dtype='float')
    
    return times

def est_amp(series):
    """Uses interquartile range to estimate amplitude of a time series."""
    qlo = __score_at_percentile__(series, 25)
    qhi = __score_at_percentile__(series, 75)
    iqr = qhi - qlo
    return 1.5 * iqr

def __score_at_percentile__(ser, per):
    ser = np.sort(ser, axis=0)
    i = per/100. * (ser.shape[0] - 1)
    if (i % 1 == 0):
        score = ser[i]
    else:
        interpolate = lambda a,b,frac: a + (b - a)*frac
        score = interpolate(ser[int(i)], ser[int(i) + 1], i % 1)
    return score

def erf(x):
    """Dependency-free computation of error function. From Handbook of
       Mathematical Functions. (7.1.26)"""
    x = abs(x)

    a1 =  0.254829592
    a2 = -0.284496736
    a3 =  1.421413741
    a4 = -1.453152027
    a5 =  1.061405429
    p  =  0.3275911

    t = 1.0/(1.0 + p*x)
    y = 1.0 - (((((a5*t + a4)*t) + a3)*t + a2)*t + a1)*t*math.exp(-x*x)
    
    return y if x >= 0 else 2-y

if __name__ == "__main__":
    print "This module includes utility functions for JTK Cycle."
