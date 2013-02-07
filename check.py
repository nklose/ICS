"""A checking program

This file contains a simple program that compares the numerical
values contained in certain files in one directory to values in
files with the same name in another directory, and checks whether
these values agree within a certain epsilon. If all the values
agree, the program prints no output; if there are values that
do not agree, the program prints out the names of the files
containing these values to stdout.

By default the two directories used are 'accTests/mdata'
and 'pdata', and the default value for epsilon is 0.0005; 
under these settings, everything passes the test.
"""

from __future__ import division
import numpy as np
import os

def run(mdata,pdata,epsilon):
    opts = ['ACb','ACg','ACr','XCrg','XCrb','XCrg','TripleCrgb']
    fits = [opt+'Fit' for opt in opts]
    names = opts+fits
    olds = [path(mdata,name,'txt') for name in names]
    news = [path(pdata,name,'txt') for name in names]
    for (old,new) in zip(olds,news):
        a = np.loadtxt(old)
        b = np.loadtxt(new)
        if not np.all(np.abs(a-b)<epsilon):
            print old

def path(dir,fname,ext):
    return str.format('{}{}{}.{}',dir,os.sep,fname,ext)

def main(): run(os.path.join('accTests','mdata'),'pdata',0.0005)  
if __name__ == "__main__": main()
