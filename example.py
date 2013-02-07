"""An example program

This file contains an example program that demonstrates the use of
the functions provided by dual.py and triple.py to calculate the
dual and triple correlation of an image and write out the results.

This program is not meant as a basis on top of which to build
high level interfaces, but rather as an example of how to call
the functions in dual.py and triple.py; moreover, along with
the check.py file, it can be used for basic testing.

Type 'python example.py' to run this program -- note that it expects
its input to come from an RGB file called 'RGBtemp.bmp' in the current
directory. Type 'python -m cProfile -s time example.py > prof.txt' to
profile this program -- the profiling results will be in a 'prof.txt'
file and sorted by total time taken.
"""

from __future__ import division
import numpy as np
import scipy.misc
import os
import dual
import triple
import warnings
warnings.simplefilter('ignore',np.ComplexWarning)

ALL_COLORS = str.split('r:g:b:rg:rb:gb:rgb',':')

def run(pdata,image_name,colors):
    image = scipy.misc.imread(image_name)
    r = image[:,:,0].astype('d')
    g = image[:,:,1].astype('d')
    b = image[:,:,2].astype('d')
    n = None
    p = [(r,n,n),(g,n,n),(b,n,n),(r,g,n),(r,b,n),(g,b,n),(r,g,b)]
    res = np.empty((7,3))
    np.ndarray.fill(res,np.nan)
    for color in colors:
        i = list.index(ALL_COLORS,color)
        res[i] = run_any(pdata,p[i][0],p[i][1],p[i][2],color)
    np.savetxt(path(pdata,'RGBtemp','txt'),res,fmt='%9.5f')

def run_any(pdata,a,b,c,color):
    if len(color) <= 2: return run_dual(pdata,a,b,c,color)
    if len(color) == 3: return run_trip(pdata,a,b,c,color)

def run_dual(pdata,a,b,c,color):
    range_val = 20
    initial_val = np.array([1,10,0],dtype=np.float64)
    (gnew,gs,gcov) = dual.core(a,b,range_val,initial_val)
    gfit = gauss_2d(range_val,gs)
    if len(color) == 1: code = 'AC'
    if len(color) == 2: code = 'XC'
    fname1 = code+color
    fname2 = code+color+'Fit'
    np.savetxt(path(pdata,fname1,'txt'),gnew,fmt='%9.5f')
    np.savetxt(path(pdata,fname2,'txt'),gfit,fmt='%9.5f')
    return gs

def run_trip(pdata,r,g,b,color):
    (sr,sg,sb,avg_rgb) = triple.core_0(r,g,b)
    lowlim = 48
    (bsdisp,tcmat,lim,side) = triple.core_1(sr,sg,sb,avg_rgb,lowlim)
    range_val = 15
    initial_val = np.array([50,2,0],dtype=np.float64)
    (gnew,gs,gcov) = triple.core_2(tcmat,lim,side,range_val,initial_val)
    gfit = gauss_1d(range_val,gs)
    gs[1] = int(gs[1]*(side/lim)*10)/10
    fname1 = 'TripleCrgb'
    fname2 = 'TripleCrgbFit'
    np.savetxt(path(pdata,fname1,'txt'),gnew,fmt='%9.5f',delimiter='\n')
    np.savetxt(path(pdata,fname2,'txt'),gfit,fmt='%9.5f',delimiter='\n')
    return gs
    
def gauss_2d(range_val,gs):
    g1_sq = gs[1]**2
    gmn = np.empty((range_val,range_val))
    for a in xrange(range_val):
        for b in xrange(a+1):
            gmn[a,b] = gs[0]*np.exp((-(a**2+b**2))/g1_sq)+gs[2]
    for a in xrange(range_val):
        for b in xrange(a+1,range_val):
            gmn[a,b] = gmn[b,a]
    return gmn

def gauss_1d(range_val,gs):
    g1_sq = gs[1]**2
    delta_sq = np.arange(range_val)**2
    return gs[0]*np.exp(-delta_sq/g1_sq)+gs[2]
    
def path(dir,fname,ext):
    return str.format('{}{}{}.{}',dir,os.sep,fname,ext)
    
def main(): run('pdata','RGBtemp.bmp',ALL_COLORS)  
if __name__ == "__main__": main()
