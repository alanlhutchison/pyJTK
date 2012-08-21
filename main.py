#!/usr/bin/epython

import os.path
import sys
sys.path.append(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'src'
        )
    )

def main(filenm):
    pass

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print "Please argue a filename when running main.py !"
