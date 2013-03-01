"""An example program

This file contains an example program that demonstrates the use of
the functions provided by dual.py and triple.py to calculate the
dual and triple correlation of an image and write out the results.

This program is not meant as a basis on top of which to build
high level interfaces, but rather as an example of how to call
the functions in dual.py and triple.py.

Run with 'python example.py'.
Profile with 'python -m cProfile -s cum example.py >| pout';
the output will be in 'pout' sorted by cumulative time.

Copryight (c) 2013 Nick Klose, Richard Leung, Cameron Mann, Glen Nelson,
Omar Qadri, and James Wang under the 401 IP License (see LICENSE file)
"""

from __future__ import division
import numpy as np
import scipy.misc
import os
import dual
import triple
import backend_utils as butils

import warnings
warnings.simplefilter('ignore',np.ComplexWarning)

ALL_COLORS = str.split('r:g:b:rg:rb:gb:rgb',':')

def run(pdata,image_name,colors):
    if not os.path.exists(pdata):
        os.makedirs(pdata)
    image = scipy.misc.imread(image_name)
    r = image[:,:,0].astype('d')
    g = image[:,:,1].astype('d')
    b = image[:,:,2].astype('d')
    n = None
    p = [(r,n,n),(g,n,n),(b,n,n),(r,g,n),(r,b,n),(g,b,n),(r,g,b)]
    res = np.empty((7,4))
    np.ndarray.fill(res,np.nan)
    for color in colors:
        i = list.index(ALL_COLORS,color)
        (par,resnorm) = run_any(pdata,p[i][0],p[i][1],p[i][2],color)
        res[i,0:3] = par
        res[i,3] = resnorm
    header = str.format('{:>9s} {:>9s} {:>9s} {:>9s}',
                        'g(0)','w','ginf','norm')
    fpath = pdata + 'results.txt'
    with open(fpath,'w') as f:
        f.write(header+'\n')
        np.savetxt(f,res,fmt='%9.5f')
    print 'Done'

def run_any(pdata,a,b,c,color):
    if len(color) <= 2: return run_dual(pdata,a,b,c,color)
    if len(color) == 3: return run_trip(pdata,a,b,c,color)

def run_dual(pdata,a,b,c,color):
    range_val = 20
    initial_val = np.array([1,10,0],dtype=np.float64)
    (out,par) = dual.core(a,b,range_val,initial_val)
    fit = butils.gauss_2d(np.arange(range_val**2),*par)\
        .reshape(range_val,range_val)
    resnorm = np.sum((out-fit)**2)
    if len(color) == 1: code = 'AC'
    if len(color) == 2: code = 'XC'
    fname1 = code+color+'.txt'
    fname2 = code+color+'Fit.txt'
    np.savetxt(pdata+fname1,out,fmt='%9.5f')
    np.savetxt(pdata+fname2,fit,fmt='%9.5f')
    return (par,resnorm)

def run_trip(pdata,r,g,b,color):
    side = np.shape(r)[0]
    avg_r = np.average(r)
    avg_g = np.average(g)
    avg_b = np.average(b)
    avg_rgb = avg_r*avg_g*avg_b
    (sr,sg,sb) = triple.core_0(r,g,b)
    # over here in the UI, you would display surfc(abs(sr))
    # to allow the user to determine a suitable lim, rather
    # than hard coding it
    lim = 32
    part_rgb = triple.core_1(sr,sg,sb,avg_rgb,lim)
    # over here in the UI, you would display surfc(part_rgb[0,:,:])
    # to allow the user to determine a suitable range_val and
    # initial_val, rather than hard coding them
    range_val = 15
    initial_val = np.array([50,2,0],dtype=np.float64)
    (out,par) = triple.core_2(part_rgb,range_val,initial_val)
    fit = butils.gauss_1d(np.arange(range_val),*par)
    par[1] = int(par[1]*(side/lim)*10)/10
    resnorm = np.sum((out-fit)**2)
    fname1 = 'TripleCrgb.txt'
    fname2 = 'TripleCrgbFit.txt'
    np.savetxt(pdata+fname1,out,fmt='%9.5f',delimiter='\n')
    np.savetxt(pdata+fname2,fit,fmt='%9.5f',delimiter='\n')
    return (par,resnorm)
    
def main(): run('output/','../accTests/inputs/RGBtemp/rgb_001.bmp',ALL_COLORS)
if __name__ == "__main__": main()
