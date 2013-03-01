"""A checking program

This file contains functions to ensure that valeues in sets of files
agree within a certain tolerance, and prints out the names of files
containing disagreeing values to stdout.

Copryight (c) 2013 Nick Klose, Richard Leung, Cameron Mann, Glen Nelson, 
Omar Qadri, and James Wang under the 401 IP License (see LICENSE file)
"""

from __future__ import division
import numpy as np
import os

def run(mdata,pdata,epsilon):
    opts = ['ACb','ACg','ACr','XCrg','XCrb','XCrg','TripleCrgb']
    fits = [opt+'Fit' for opt in opts]
    names = opts+fits
    olds = [mdata+name+'.txt' for name in names]
    news = [pdata+name+'.txt' for name in names]
    num_wrong = 0
    for (old,new) in zip(olds,news):
        a = np.loadtxt(old)
        b = np.loadtxt(new)
        if not np.all(np.abs(a-b)<epsilon):
            num_wrong += 1
            print old
    if num_wrong == 0:
        print 'All correct'
    else:
        print str.format('Total {:d} incorrect files',num_wrong)

def path(dir,fname,ext):
    return str.format('{}{}{}.{}',dir,os.sep,fname,ext)

def main(): run('../accTests/outputs/RGBtemp/','output/',0.0005)
if __name__ == "__main__": main()
