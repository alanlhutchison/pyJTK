#!/usr/bin/epython

import sys
import os.path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import numpy as np

def make_times(timepoints, reps=1):
    try:
        if len(reps) == timepoints:
            times = np.array(reps)
        else:
            times = reps[0] * np.ones(timepoints, dtype='float')
            
    except: # reps is not array-like
        times = reps * np.ones(timepoints, dtype='float')
    
    return times
