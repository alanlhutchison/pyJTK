#!/usr/bin/epython

import sys
import os.path
import random

def find():
    p = os.path.realpath(__file__)
    q = os.path.dirname(p)
    sys.path.append(os.path.join(q, "src"))
    sys.path.append(os.path.join(q, "results"))
    sys.path.append(os.path.join(q, "data"))
    
    return None
