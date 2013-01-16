#!/usr/bin/epython

import os.path
import sys

FPATH = os.path.dirname(os.path.realpath(__file__)),[0]
sys.path.append(FPATH[0]+'/src')
VERSION = "3.3"

import json
import unittest
import string
import argparse

from main import JTKCycleRun
from parsed import DataParser

import waveforms as w
import numpy as np

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

    reps       = config.get("reps",        None) or parser.reps
    timepoints = config.get("timepoints",  None) or parser.timepoints
    periods    = config.get("periods",     None) or periods
    density    = config.get("offset_step", None) or args.offset_step
    normal     = config.get("normal",      None) or args.normal

    function = __get_function__(args.function)
    symmetry = (args.function != "cosine") or args.symmetry
    test = JTKCycleRun(
        reps,
        timepoints,
        periods,
        density,
        normal=normal,
        function=function,
        symmetry=symmetry
        )

    summary = args.summary
    __write_header__(foutput, periods, summary)
    for name,series in parser.generate_series():
        _,_,_,_,_ = test.run(series)
        __write_data__(foutput, name, test, summary)

    # Variables are not currently used...
    p = args.pvalue

    finput.close()
    foutput.close()
    if fconfig != None:
        fconfig.close()

    return

def __get_function__(astr):
    f = np.cos
    if astr == "cosine":
        f = np.cos
    elif astr == "rampup":
        f = np.frompyfunc(w.ramp_up, 1, 1)
    elif astr == "rampdown":
        f = np.frompyfunc(w.ramp_down, 1, 1)
    elif astr == "impulse":
        f = np.frompyfunc(w.impulse, 1, 1)
    elif astr == "step":
        f = np.frompyfunc(w.step, 1, 1)
    else:
        f = np.cos
    return f

#
# printer utilities
#

def __write_header__(foutput, periods, summary=False):
    if summary:
        foutput.write("#")
        for period in sorted(periods):
            foutput.write("\t" + str(period) + "-HR")
        else:
            foutput.write("\n")
    else:
        foutput.write("#"+"\t"
                      +"p-value"+"\t"
                      +"amp"+"\t"
                      +"period"+"\t"
                      +"lag"+"\t"
                      +"tau"+"\n")
    return

def __write_data__(foutput, name, test, summary=False):
    if summary:
        foutput.write(name)
        est_amp,_,_,_,_ = test.best
        for period in sorted(test.results.keys()):
            offset, k_score, p_value = test.results[period]
            outstr = str(p_value)+";"+str(period)+";"+str(offset)+";"+str(est_amp)
            foutput.write("\t" + outstr)
        else:
            foutput.write("\n")
    else:
        est_amp, period, offset, k_score, p_value = test.best
        foutput.write(name+"\t"
                      +str(p_value)+"\t"
                      +str(est_amp)+"\t"
                      +str(period)+"\t"
                      +str(offset)+"\t"
                      +str(k_score)+"\n")
    return



#
# runner script utilities
#

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
    analysis.add_argument("--function",
                          dest="function",
                          type=str,
                          metavar="$FUNC_STR",
                          action='store',
                          default="cosine",
                          choices=["cosine","rampup","rampdown","step","impulse"],
                          help="cosine (dflt), rampup, rampdown, impulse, step")
    analysis.add_argument("--assymetric",
                          dest="symmetry",
                          action="store_false",
                          default=True,
                          help="flag for half-density lags")
    
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
                        help="use header to re-order data series by ZT")
    
    files = p.add_argument_group(title="files & I/O management options")
    files.add_argument("-i", "--input",
                       dest="ifile",
                       metavar="FILENM",
                       default="-",
                       type=argparse.FileType('r'),
                       help="file from which to read data (dflt: stdin)")
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
                       help="read {reps,times,periods,normal} from JSON")

    printer = p.add_argument_group(title="result output preferences")
    printer.add_argument("-s", "--summary",
                         action='store_true',
                         default=False,
                         help="print summary over all searched periods")
    
    return p

if __name__ == "__main__":
    parser = __create_parser__()
    args = parser.parse_args()
    main(args)
