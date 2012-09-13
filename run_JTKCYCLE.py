#!/usr/bin/epython

import os.path
import sys
sys.path.append(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'src'
        )
    )
import argparse

def main(args):
    pass

def _create_parser():
    p = argparse.ArgumentParser(
        description="Python script runner for JTK_CYCLE statistical test.",
        epilog="..."
        )

    p.add_argument("dfile",
                   metavar="DATA_FILE",
                   default="-",
                   type=argparse.FileType('r'),
                   help="File from which to read data to run.")
    p.add_argument("-t", "--test",
                   action='store_true',
                   default=False,
                   help="Run the Python unittest testing suite.")
    
    analysis = p.add_argument_group(title="JTK_CYCLE analysis options")
    analysis.add_argument("--averaged",
                          action='store_true',
                          default=False,
                          help="Use averages to collapse replicate points.")
    analysis.add_argument("--min",
                          metavar="N",
                          type=int,
                          help="Set min period to N of intervals.")
    analysis.add_argument("--max",
                          metavar="N",
                          type=int,
                          help="Set max period to N of intervals.")
    
    bins = p.add_argument_group(title="low-pass frequency filters")
    bbins = bins.add_mutually_exclusive_group()
    bbins.add_argument("--gauss",
                       type=int,
                       metavar="STDEV",
                       help="Gaussian averages with standard deviation STDEV.")
    bbins.add_argument("--tricubic",
                       type=int,
                       metavar="WIDTH",
                       help="Tricubic averages with kernel width: 2*WIDTH.")
    bbins.add_argument("--step",
                       type=int,
                       metavar="SIZE",
                       help="Step-function moving average with width: SIZE.")
    
    files = p.add_argument_group(title="files & I/O management options")
    files.add_argument("-a", "--annotations",
                       dest="afile",
                       metavar="FILE",
                       type=argparse.FileType('r'),
                       help="Read annotations from file, not from data rows.")
    files.add_argument("-o", "--output",
                       dest="ofile",
                       metavar="FILE",
                       type=argparse.FileType('w'),
                       default="-",
                       help="Select a file to write results. Default: stdout.")
    
    printer = p.add_argument_group(title="result output preferences")
    printer.add_argument("-s", "--summarize",
                         action='store_true',
                         default=False,
                         help="Print a test summary after all cycles finish.")
    printer.add_argument("-u", "--unsorted",
                         action='store_true',
                         default=False,
                         help="Do not sort rows by P-values, print unsorted.")
    printer.add_argument("-m", "--multiplex",
                         action='store_true',
                         default=False,
                         help="Prints statistics for all considered periods.")
    printer.add_argument("-n",
                         dest="nlines",
                         metavar="N",
                         action='store',
                         help="Only write output for the first N count rows.")
    
    return p

if __name__ == "__main__":
    parser = _create_parser()
    args = parser.parse_args()
    main(args)
