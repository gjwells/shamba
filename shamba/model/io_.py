#!/usr/bin/python

"""Module for io related functions in the SHAMBA program."""

import sys
import os
import logging as log
import argparse
import csv

import numpy as np
from shamba.model import cfg
from shamba import default_input

class FileOpenError(Exception):
    
    """
    Exception to be called when a file can't be opened.
    Prints error message and closes program with exit code 2.
    
    """

    def __init__(self, filename):
        """Initialise FileOpenError.

        Args:
            filename: name of file which couldn't be opened
        
        """
        super(FileOpenError, self).__init__()
        log.exception("Could not open %s" % filename)


def print_csv(fileOut, array, col_names=[], 
        print_years=False, print_total=False, print_column=False):
    """Custom method for printing an array or list to a csv file.
    Uses numpy.savetxt. 

    Args
        arrayName: array to be printed
        fileOut: where to print (put in output unless path specified)
        col_names: list of column names to put at top of csv
        print_years: whether to print the years (index of array) in
                     left-most column
        print_total: whether to print the total of each row in last column
        print_column: whether to print a 1d array to a column instead of row
    """
    def round_(x):
        try:
            x = "%.5f" % x
        except TypeError:
            pass
        return x
    
    # See if existing path was given, put file in OUT_DIR if not
    if not os.path.isdir(os.path.dirname(fileOut)):
        fileOut = os.path.join(cfg.OUT_DIR, fileOut)
        
    
    # See if the array given is actually a list (because it has strings)
    if isinstance(array, list):
        isList = True

        # WARNIN - broken if data is 3d (list is doubly nested)
            # but not sure how you'd print that to csv anyway
        if not isinstance(array[0], list):
            array = [array, []]     # to make sure it's at least 2d
    else:
        isList = False

    if print_total and not isList:
        #Add total as last column
        total = np.sum(array, axis=1)
        col_names.append('total')
        array = np.column_stack((array,total))

    if print_years and not isList:
        # Add years as first column
        years = np.array(range(array.shape[0]))
        col_names.insert(0, 'year')
        array = np.column_stack((years,array))
        
    # manually do header since numpy 1.6 doesn't
    # support header argument to savetxt - FFS
    try:
        with open(fileOut, 'w') as outcsv:
            writer = csv.writer(outcsv,lineterminator='\n')
            writer.writerow(col_names)
            if isList:
                for row in array:
                    if row:
                        writer.writerow(map(lambda x: round_(x), row))
            else:
                if array.ndim == 1 and print_column:
                    np.savetxt(
                            outcsv, np.atleast_2d(array).T, 
                            delimiter=',', fmt="%.5f")
                else:
                    # 2d
                    np.savetxt(
                            outcsv, np.atleast_2d(array), 
                            delimiter=',', fmt='%.5f')

    except IOError:
        log.exception("Cannot print to file %s", fileOut)

def read_csv(fileIn, cols=None):
    """Read data from a .csv file. Usees numpy.loadtxt. 
    
    Args: 
        fileIn: name of file to read
        cols: tuple of columns to read (read all if cols==None)
    Returns:
        array: numpy array with data from fileIn
    Raises:
        IOError: if file can't be found/opened

    """
        
    # if full path not specified, search through the files in the 
    # project data folder /input, then in the 'defaults' folder
    default_path = os.path.dirname(os.path.abspath(default_input.__file__))

    if not os.path.isfile(fileIn):
        if os.path.isfile(os.path.join(cfg.INP_DIR, fileIn)):
            fileIn = os.path.join(cfg.INP_DIR, fileIn)
        elif os.path.isfile(os.path.join(default_path, fileIn)):
            fileIn = os.path.join(default_path, fileIn)
        else:
            # not in either folder, and not in full path
            raise FileOpenError(fileIn)
    
    array = np.genfromtxt(
            fileIn,
            skip_header=1,
            usecols=cols,
            comments='#',
            delimiter=','
    )

    return array

def read_mixed_csv(fileIn, cols=None, types=None):
    """Read data from a mixed csv (strings and numbers). 
    Uses numpy.loadfromtxt 

    NOTE: when used to read HWSD stuff (probably the primary
    use of this method), make sure to use usecols=(0,1,2,3..12)
    since genfromtxt seems to think there's 15 cols and gives an error
    
    Args:
        fileIn: name of file to be read
        cols: tuple of columns to read (read all if cols==None) 
        types: tuple of the expected types (e.g. int, float, "|S25", etc.)
    Returns:
        array: ndarray of data from fileIn
    Raises:
        IOError: if file can't be read/opened or if types don't work
        
    """

    try:
        if not os.path.isfile(fileIn):
            if os.path.isfile(os.path.join(cfg.INP_DIR, fileIn)):
                fileIn = os.path.join(cfg.INP_DIR, fileIn)
            elif os.path.isfile(os.path.join(cfg.DEF_DIR, fileIn)):
                fileIn = os.path.join(cfg.DEF_DIR, fileIn)
            else:
                # not in either folder, and not in full path
                raise IOError 

        array = np.genfromtxt(
                fileIn,
                usecols=cols,
                dtype=types,
                delimiter=',',
                skip_header=1
        )
    except IOError:
        raise FileOpenError(fileIn)

    return array

def get_cl_args():
    """
    Parse the command line arguments for graph and report generation 
    (-g, -r) and verbosity of output (-v=info,-vv=debug) and project name 
    and input filename. 
    Return args.
    """

    parser = argparse.ArgumentParser()
    verboseMsg = "Set verbosity level (e.g. -v -v or vv more verbose than -v)"
    parser.add_argument(
            "-v", "--verbose", action="count", dest="verbose",
            default=0, help=verboseMsg
    )
    parser.add_argument(
            "-p", "--param", action="store", dest="param")
    parser.add_argument(
            "-r", "--report", action="store_true", dest="report",
            default=False, help="Print report to stdout"
    )
    parser.add_argument(
            "-g", "--graph", action="store_true", dest="graph",
            default=False, help="Show plots"
    )

    parser.add_argument(
            "-prj", "--project", action="store", dest="project",
            default=False, help="project name"
    )

    parser.add_argument(
            "-in", "--input", action="store", dest="project_input",
            default=False, help="CSV project input file"
    )

    args = parser.parse_args()

    # Set up logging level based on v arguments
    if args.verbose == 2:
        log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
    elif args.verbose == 1:
        log.basicConfig(format="%(levelname)s: %(message)s", level=log.INFO)
    elif args.verbose == 0:
        log.basicConfig(format="%(levelname)s: %(message)s")

    return args

def print_metadata():
    """
    Print the project metadata (timestamp and unique hex ID)
    calculated in the cfg module.
    
    """
    filepath = os.path.join(cfg.SAV_DIR, '.info')
    with open(filepath, 'w') as f:
        f.write(cfg.ID+"\n"+cfg.TIME+"\n"+cfg.PROJ_NAME+"\n\n")

