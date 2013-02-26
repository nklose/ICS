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

Copryight (c) 2013 Nick Klose, Richard Leung, Cameron Mann, Glen Nelson, Omar
Qadri, and James Wang under the 401 IP License.

This Agreement, effective the 1st day of April 2013, is entered into by and
between Dr. Nils Petersen (hereinafter "client") and the students of the
Biomembrane team (hereinafter "the development team"), in order to establish
terms and conditions concerning the completion of the Image Correlation
Spectroscopy application (hereinafter "The Application") which is limited to the
application domain of application-domain (hereinafter "the domain of use for the
application").  It is agreed by the client and the development team that all
domain specific knowledge and compiled research is the intellectual property of
the client, regarded as a copyrighted collection. The framework and code base
created by the development team is their own intellectual property, and may only
be used for the purposes outlined in the documentation of the application, which
has been provided to the client. The development team agrees not to use their
framework for, or take part in the development of, anything that falls within
the domain of use for the application, for a period of 6 (six) months after the
signing of this agreement.
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
