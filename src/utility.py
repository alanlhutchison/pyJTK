#!/usr/bin/epython

import sys
import os.path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import numpy as np
from scipy.stats import scoreatpercentile

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
    qlo = scoreatpercentile(series, 25)
    qhi = scoreatpercentile(series, 75)
    iqr = qhi - qlo
    return 1.5 * iqr
