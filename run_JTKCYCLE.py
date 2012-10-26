#!/usr/bin/epython

import os.path
import sys

FPATH = os.path.dirname(os.path.realpath(__file__)),[0]
sys.path.append(FPATH[0]+'/src')
VERSION = "2.3"

import json
import unittest
import string
import argparse

from main import JTKCycleRun
from parsed import DataParser

def main(args): # argument namespace
    if args.test:
        tests = unittest.defaultTestLoader.discover(FPATH[0]+"/spec",
                                                    pattern="*spec.py")
        test_runner = unittest.TextTestRunner(verbosity=1)
        test_runner.run(tests)
        return
    
    finput = args.ifile
    foutput = args.ofile
    fconfig = args.cfile
    
    parser = DataParser(finput, args.repattern)
    
    max_period = (args.max or 26/int(parser.interval)) + 1
    min_period = args.min or 20/int(parser.interval)
    step = args.step or 1
        
    config = {}
    if fconfig != None:
        config = json.load(fconfig)
        
    n_times   = __get_value__("n_times",   config) or parser.n_times
    reps      = __get_value__("reps",      config) or parser.reps
    interval  = __get_value__("interval",  config) or parser.interval
    timerange = __get_value__("timerange", config) or parser.timerange
    periods   = range(min_period, max_period, step)
    normal    = False
        
    test = JTKCycleRun(n_times, reps, periods,
                       interval, timerange, normal)
    
    foutput.write("probeset"+"\t"
                  +"p-value"+"\t"
                  +"period"+"\t"
                  +"lag"+"\t"
                  +"tau"+"\n")
    for name,series in parser.generate_series():
        period, offset, k_score, p_value = test.run(series)
        foutput.write(name+"\t"
                      +str(p_value)+"\t"
                      +str(period)+"\t"
                      +str(offset)+"\t"
                      +str(k_score)+"\n")
    
    # These are not currently used...
    p = args.pvalue
    summarize = args.summarize
    ndebug = args.ndebug
    
    finput.close()
    foutput.close()
    if fconfig != None:
        fconfig.close()
    
    return

def __get_value__(k,d):
    try:
        return d[k]
    except:
        return None

def __create_parser__():
    p = argparse.ArgumentParser(
        description="python script runner for JTK_CYCLE statistical test",
        epilog="...",
        version=VERSION
        )

    p.add_argument("-t", "--test",
                   action='store_true',
                   default=False,
                   help="run the Python unittest testing suite")
    p.add_argument("-p", "--pvalue",
                   metavar="P",
                   type=float,
                   default=0.01,
                   help="set p-value to define significance (dflt: 0.01)")

    analysis = p.add_argument_group(title="JTK_CYCLE analysis options")
    analysis.add_argument("--min",
                          metavar="N",
                          type=int,
                          help="set min period to N of intervals (dflt: 20/t)")
    analysis.add_argument("--max",
                          metavar="N",
                          type=int,
                          help="set max period to N of intervals (dflt: 26/t)")
    analysis.add_argument("--step",
                          metavar="N",
                          type=int,
                          help="determines range step in # intervals (dflt: 1)")
    
    parser = p.add_argument_group(title="parser option")
    parser.add_argument("-r", "--repattern",
                        action='store_true',
                        default=False,
                        help="use header line to re-order data series by ZT")
    
    files = p.add_argument_group(title="files & I/O management options")
    files.add_argument("-i", "--input",
                       dest="ifile",
                       metavar="FILENM",
                       default="-",
                       type=argparse.FileType('r'),
                       help="file from which to read data to run (dflt: stdin)")
    files.add_argument("-o", "--output",
                       dest="ofile",
                       metavar="FILENM",
                       type=argparse.FileType('w'),
                       default="-",
                       help="file to write results (dflt: stdout)")
    files.add_argument("-c", "--config",
                       dest="cfile",
                       metavar="FILENM",
                       type=argparse.FileType('r'),
                       help="read configuration from JSON, not from data header")

    printer = p.add_argument_group(title="result output preferences")
    printer.add_argument("-s", "--summarize",
                         action='store_true',
                         default=False,
                         help="print a test summary after all cycles finish")
    printer.add_argument("-n",
                         dest="ndebug",
                         metavar="N",
                         action='store',
                         help="wouldn't you love to know...")
    
    return p

if __name__ == "__main__":
    parser = __create_parser__()
    args = parser.parse_args()
    main(args)
