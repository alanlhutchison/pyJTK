#!/usr/bin/epython

import os.path
import sys

FPATH = os.path.dirname(os.path.realpath(__file__)),[0]
sys.path.append(FPATH[0]+'/src')
VERSION = "2.3.1"

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
    
    max_period = (args.max or 26) + 1
    min_period = args.min or 20
    period_step = args.period_step or 2
    
    try:
        periods = json.loads(args.periods)
    except:
        periods = range(min_period, max_period, period_step)
    
    config = {}
    if fconfig != None:
        config = json.load(fconfig)
    
    reps       = __get_value__("reps",       config) or parser.reps
    timepoints = __get_value__("timepoints", config) or parser.timepoints
    periods    = __get_value__("periods",    config) or periods
    normal     = __get_value__("normal",     config) or args.normal
    
    test = JTKCycleRun(reps, timepoints, periods, normal)
    
    summarize = args.summarize
    __write_header__(foutput, periods, summarize)
    for name,series in parser.generate_series():
        _,_,_,_ = test.run(series)
        __write_data__(foutput, name, test, summarize)
    
    # Variables are not currently used...
    p = args.pvalue
    offset_step = args.offset_step
    
    finput.close()
    foutput.close()
    if fconfig != None:
        fconfig.close()
    
    return


#
# printer utilities
#

def __write_header__(foutput, periods, summarize=False):
    if summarize:
        foutput.write("probeset")
        for period in sorted(periods):
            foutput.write("\t" + str(period) + "-HR")
        else:
            foutput.write("\n")
    else:
        foutput.write("probeset"+"\t"
                      +"p-value"+"\t"
                      +"period"+"\t"
                      +"lag"+"\t"
                      +"tau"+"\n")
    return

def __write_data__(foutput, name, test, summarize=False):
    if summarize:
        foutput.write(name)
        for period in sorted(test.results.keys()):
            offset, k_score, p_value = test.results[period]
            foutput.write("\t" + str(p_value))
        else:
            foutput.write("\n")
    else:
        period, offset, k_score, p_value = test.best
        foutput.write(name+"\t"
                      +str(p_value)+"\t"
                      +str(period)+"\t"
                      +str(offset)+"\t"
                      +str(k_score)+"\n")
    return



#
# runner script utilities
#

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

    analysis = p.add_argument_group(title="JTK_CYCLE analysis options")
    analysis.add_argument("-p", "--pvalue",
                          metavar="P",
                          type=float,
                          default=0.01,
                          help="set p-value to define significance (dflt: 0.01)")
    analysis.add_argument("-n", "--normal",
                          dest="normal",
                          action='store_true',
                          default=False,
                          help="use normal approximation to null distribution")
    
    periods = p.add_argument_group(title="JTK_CYCLE custom search periods")
    periods.add_argument("--periods",
                         metavar="$JSON_ARR",
                         type=str,
                         action='store',
                         help="JSON array specifies periods i.e. [1,3,5,7]")
    periods.add_argument("--min",
                         metavar="N",
                         type=int,
                         help="set min period to number N hours (dflt: 20)")
    periods.add_argument("--max",
                         metavar="N",
                         type=int,
                         help="set max period to number N hours (dflt: 26)")
    periods.add_argument("--period-step",
                         metavar="N",
                         type=int,
                         help="determines range step N in hours (dflt: 2)")
    periods.add_argument("--offset-step",
                         metavar="N",
                         type=float,
                         action='store',
                         help="offset step size N of half-hours (dflt: 2)")
    
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
                       help="configure {reps, times, periods, normal} from JSON")

    printer = p.add_argument_group(title="result output preferences")
    printer.add_argument("-s", "--summarize",
                         action='store_true',
                         default=False,
                         help="print a test summary after all cycles finish")
    
    return p

if __name__ == "__main__":
    parser = __create_parser__()
    args = parser.parse_args()
    main(args)
