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
import os
import dual
import triple

import warnings
warnings.simplefilter('ignore',np.ComplexWarning)

import backend_utils as butils
import bimloader

ALL_COLORS = str.split('r:g:b:rg:rb:gb:rgb',':')

def run_seperate(pdata, rfile, gfile, bfile, colors, d_range=20, t_range=15):
    """Added for integration tests"""
    if not os.path.exists(pdata):
        os.makedirs(pdata)
    r = bimloader.load_image_split(rfile)
    g = bimloader.load_image_split(gfile)
    b = bimloader.load_image_split(bfile)
    n = None
    p = [(r,n,n),(g,n,n),(b,n,n),(r,g,n),(r,b,n),(g,b,n),(r,g,b)]
    res = np.empty((7,7))
    np.ndarray.fill(res,np.nan)
    for color in colors:
        i = list.index(ALL_COLORS,color)
        res[i,:] = run_any(pdata,p[i][0],p[i][1],p[i][2],color,d_range,t_range)
    header = str.format('{:>9s} {:>9s} {:>9s} {:>9s} {:>9s} {:>9s} {:>9s}',
                        'g(0)','w','ginf','dx','dy','used','norm')
    fpath = get_filename(pdata, 'results.txt')
    with open(fpath,'w') as f:
        f.write(header+'\n')
        np.savetxt(f,res,fmt='%9.5f')
    print 'Done'

def run(pdata,image_name,colors,d_range=20,t_range=15):
    if not os.path.exists(pdata):
        os.makedirs(pdata)
    (r,g,b) = bimloader.load_image_mixed(image_name)
    n = None
    p = [(r,n,n),(g,n,n),(b,n,n),(r,g,n),(r,b,n),(g,b,n),(r,g,b)]
    res = np.empty((7,7))
    np.ndarray.fill(res,np.nan)
    for color in colors:
        i = list.index(ALL_COLORS,color)
        res[i,:] = run_any(pdata,p[i][0],p[i][1],p[i][2],color,d_range,t_range)
    header = str.format('{:>9s} {:>9s} {:>9s} {:>9s} {:>9s} {:>9s} {:>9s}',
                        'g(0)','w','ginf','dx','dy','used','norm')
    fpath = get_filename(pdata, 'results.txt')
    with open(fpath,'w') as f:
        f.write(header+'\n')
        np.savetxt(f,res,fmt='%9.5f')
    print 'Done'

def run_any(pdata,a,b,c,color,d_range,t_range):
    if len(color) <= 2: return run_dual(pdata,a,b,c,color,d_range)
    if len(color) == 3: return run_trip(pdata,a,b,c,color,t_range)

def run_dual(pdata,a,b,c,color,d_range):
    range_val = d_range
    #g0, w, ginf, deltaX?, deltaY?
    initial_val = np.array([1,10,0,0,0],dtype=np.float64)
    consider_deltas = False
    (out,par,used_deltas) = dual.core(a,b,range_val,initial_val,consider_deltas)
    fit = butils.gauss_2d_deltas(np.arange(range_val**2),*par)\
        .reshape(range_val,range_val)
    resnorm = np.sum((out-fit)**2)
    if len(color) == 1: code = 'AC'
    if len(color) == 2: code = 'XC'
    fname1 = code+color+'.txt'
    fname2 = code+color+'Fit.txt'
    np.savetxt(get_filename(pdata, fname1),out,fmt='%9.5f')
    np.savetxt(get_filename(pdata, fname2),fit,fmt='%9.5f')
    full_par = np.zeros(7)
    full_par[0:5] = par
    full_par[5] = used_deltas
    full_par[6] = resnorm
    return full_par

def run_trip(pdata,r,g,b,color,t_range):
    side = np.shape(r)[0]
    (avg_r,sr) = triple.core_0(r)
    (avg_g,sg) = triple.core_0(g)
    (avg_b,sb) = triple.core_0(b)
    # over here in the UI, you would display surfc(abs(sr))
    # to allow the user to determine a suitable lim, rather
    # than hard coding it
    lim = 32
    avg_rgb = avg_r*avg_g*avg_b
    part_rgb = triple.core_1(sr,sg,sb,avg_rgb,lim)
    # over here in the UI, you would display surfc(part_rgb[0,:,:])
    # to allow the user to determine a suitable range_val and
    # initial_val, rather than hard coding them
    range_val = t_range
    initial_val = np.array([50,2,0],dtype=np.float64)
    (out,par) = triple.core_2(part_rgb,range_val,initial_val)
    fit = butils.gauss_1d(np.arange(range_val),*par)
    par[1] = int(par[1]*(side/lim)*10)/10
    resnorm = np.sum((out-fit)**2)
    fname1 = 'TripleCrgb.txt'
    fname2 = 'TripleCrgbFit.txt'
    np.savetxt(get_filename(pdata, fname1),out,fmt='%9.5f',delimiter='\n')
    np.savetxt(get_filename(pdata, fname2),fit,fmt='%9.5f',delimiter='\n')
    full_par = np.zeros(7)
    full_par[0:3] = par
    full_par[6] = resnorm
    return full_par

def get_filename(pdata, fname):
    return os.path.join(pdata, fname)

def main(): run('output/','../accTests/inputs/RGBtemp/rgb_001.bmp',ALL_COLORS)
if __name__ == "__main__": main()
