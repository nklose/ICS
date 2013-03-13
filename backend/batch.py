"""Runs a batch job

This file contains functions that run a batch job with a given
configuration. Three sample configurations are given below.
Run with 'python batch.py'

Copryight (c) 2013 Nick Klose, Richard Leung, Cameron Mann, Glen Nelson,
Omar Qadri, and James Wang under the 401 IP License (see LICENSE file)
"""

from __future__ import division
import numpy as np
import scipy.optimize

import os
import sys
import ctypes
from ctypes import c_int
from ctypes import c_void_p

import warnings
warnings.simplefilter('ignore',np.ComplexWarning)

import configs
import backend_utils as butils
import bimloader

raw_image = None
ALL_COLORS = str.split('r:g:b:rg:rb:gb:rgb',':')
DUAL_COMBINATIONS = [(0,0),(1,1),(2,2),(0,1),(0,2),(1,2)]

class Info:

    lib = None              # handle to backend C library
    avg = None              # average of r,g,b channels
    image = None            # image in three channels
    
    fft = None              # ffts
    shifted = None          # shifted ffts
    conj_fft = None         # conjugate ffts
    part_rgb = None         # slice of data_rgb
    
    raw_data_rgb = None     # unaligned data_rgb buffer
    raw_dual_tmp = None     # unaligned dual_tmp buffer
    data_rgb = None         # triple correlation data
    dual_tmp = None         # dual correlation data
    
    grid = None             # 2d grid used to initialize flip
    flip = None             # 2d array of alternating signs
    dual_xdata = None       # x-axis values for dual curve fitting
    triple_xdata = None     # x-axis values for triple curve fitting
    
    dual_out = None         # dual correlation output array
    dual_fit = None         # dual correlation fitting array
    dual_par = None         # dual correlation parameters
    dual_used = None        # whether deltas were used in fitting 
    
    triple_out = None       # triple correlation output array
    triple_fit = None       # triple correlation fitting array
    triple_par = None       # triple correlation parameters
    
    cur_files = None        # the current file
    num_files = None        # the number of files
    
    results = None          # summary results
    
    isr = None              # shifted r-channel as a C pointer
    isg = None              # shifted g-channel as a C pointer
    isb = None              # shifted b-channel as a C pointer    
    ilim = None             # lim as a C int
    iside = None            # side as a C int
    idata = None            # data_rgb as a C pointer
    
def setup(info,config):

    if not os.path.exists(config.output_directory):
        os.makedirs(config.output_directory)
    
    side = config.side
    lim = config.triple_lim
    
    info.lib = butils.backend_lib
    info.avg = np.empty(3)
    info.image = np.empty((3,side,side))
    info.max_pixel = None
    
    info.fft = np.empty((3,side,side), dtype=np.complex)
    info.shifted = np.empty((3,side,side), dtype=np.complex)
    info.conj_fft = np.empty((3,side,side), dtype=np.complex)
    info.part_rgb = np.empty((6,lim,lim))
    
    nbytes = lim**4*16
    info.raw_data_rgb = np.empty(nbytes+16,dtype=np.uint8)
    start_idx = -info.raw_data_rgb.ctypes.data % 16
    info.data_rgb = info.raw_data_rgb[start_idx:start_idx+nbytes]\
        .view(dtype=np.complex).reshape(lim,lim,lim,lim)
    
    nbytes = side**2*16
    info.raw_dual_tmp = np.empty(nbytes+16,dtype=np.uint8)
    start_idx = -info.raw_dual_tmp.ctypes.data % 16
    info.dual_tmp = info.raw_dual_tmp[start_idx:start_idx+nbytes]\
        .view(dtype=np.complex).reshape(side,side)
    
    info.grid = np.ogrid[:lim,:lim]
    info.flip = 1-2*((info.grid[0]+info.grid[1])%2==1)
    info.dual_xdata = np.arange(config.dual_range**2)
    info.triple_xdata = np.arange(config.triple_range)
    
    info.dual_out = np.empty((6,config.dual_range,config.dual_range))
    info.dual_fit = np.empty((6,config.dual_range,config.dual_range))
    info.dual_par = np.empty((6,5))
    info.dual_used = np.empty(6)
    
    info.triple_out = np.empty(config.triple_range)
    info.triple_fit = np.empty(config.triple_range)
    info.triple_par = np.empty(3)
    
    info.cur_files = 0
    info.num_files = config.name_max-config.name_min+1
    
    info.results = np.empty((info.num_files,53))

    info.isr = info.shifted[0,:,:].ctypes.data_as(c_void_p)
    info.isg = info.shifted[1,:,:].ctypes.data_as(c_void_p)
    info.isb = info.shifted[2,:,:].ctypes.data_as(c_void_p)
    info.ilim = c_int(config.triple_lim)
    info.iside = c_int(config.side)
    info.idata = info.data_rgb.ctypes.data_as(c_void_p);    
    info.lib.init(info.ilim,info.idata)

def run_0(info,config):
    # read image
    fnum = info.cur_files
    if config.input_type == 'mixed':
        fname = str.format(config.name_format,config.name_min+fnum)
        fpath = config.input_directory + fname
        bimloader.load_image_mixed_batch(info.image,fpath)
    elif config.input_type == 'split':
        for i in range(3):
            fname = str.format(config.name_format,'rgb'[i],config.name_min+fnum)
            fpath = config.input_directory + fname
            bimloader.load_image_split_batch(info.image[i,:,:],fpath)
    else:
        sys.exit('Input type must be mixed or split')
    
    # perform some preprocessing
    for i in range(3):
        info.avg[i] = np.average(info.image[i,:,:])
        info.fft[i,:,:] = np.fft.fft2(info.image[i,:,:])
        info.conj_fft[i,:,:] = np.conj(info.fft[i,:,:])
        info.shifted[i,:,:] = np.fft.fft2(info.image[i,:,:]-info.avg[i])
        info.shifted[i,:,:] = np.fft.fftshift(info.shifted[i,:,:])
    info.shifted[2,:,:] = np.conj(info.shifted[2,:,:])/(config.side**2)

def run_1(info,config):
    # perform dual correlation
    for i, comb in enumerate(DUAL_COMBINATIONS):
        rval = config.dual_range
        denom = info.avg[comb[0]]*info.avg[comb[1]]*config.side**2
        info.dual_tmp = np.fft.ifft2(info.fft[comb[0],:,:]*\
            info.conj_fft[comb[1],:,:])
        info.dual_out[i,:,:] = np.float64(info.dual_tmp[0:rval,0:rval])/denom-1
        first_entry = info.dual_out[i,0,0]
        info.dual_out[i,0,0] = info.dual_out[i,0,1]
        
        # dual curve fitting
        if i<3: using_deltas = config.auto_consider_deltas
        if i>=3: using_deltas = config.cross_consider_deltas
        if using_deltas:
            (info.dual_par[i,:],_) = \
                scipy.optimize.curve_fit(butils.gauss_2d_deltas,info.dual_xdata,
                np.reshape(info.dual_out[i,:,:],rval**2),config.dual_initial)
            if (info.dual_par[i,3]>config.dual_initial[1] or \
                info.dual_par[i,4]>config.dual_initial[1]): 
                using_deltas = False
        if not using_deltas:
            (info.dual_par[i,0:3],_) = \
                scipy.optimize.curve_fit(butils.gauss_2d,info.dual_xdata,
                np.reshape(info.dual_out[i,:,:],rval**2),
                config.dual_initial[0:3])
            info.dual_par[i,3] = 0
            info.dual_par[i,4] = 0
        info.dual_par[i,1] = abs(info.dual_par[i,1])
        info.dual_fit[i,:,:] = butils.gauss_2d_deltas(info.dual_xdata,\
            *info.dual_par[i,:]).reshape(rval,rval)
        info.dual_used[i] = float(using_deltas)
        info.dual_out[i,0,0] = first_entry

def run_2(info,config):
    # perform triple correlation
    info.lib.core(info.idata,info.isr,info.isg,info.isb,info.iside,info.ilim)
    info.lib.execute()
    
    info.part_rgb[0,:,:] = np.float64(info.data_rgb[:,:,0,0])
    info.part_rgb[1,:,:] = np.float64(info.data_rgb[0,:,:,0])
    info.part_rgb[2,:,:] = np.float64(info.data_rgb[0,0,:,:])
    info.part_rgb[3,:,:] = np.float64(info.data_rgb[0,:,0,:])
    info.part_rgb[4,:,:] = np.float64(info.data_rgb[:,0,:,0])
    info.part_rgb[5,:,:] = np.float64(info.data_rgb[:,0,0,:])
    info.part_rgb *= info.flip/(config.side**4*np.prod(info.avg))
    
    np.ndarray.fill(info.triple_out,0)
    for i in range(6):
        info.triple_out += info.part_rgb[i,0,0:config.triple_range]
        info.triple_out += info.part_rgb[i,0:config.triple_range,0]
    info.triple_out /= 12
    
    # triple curve fitting
    (info.triple_par[:],_) = \
        scipy.optimize.curve_fit(butils.gauss_1d,info.triple_xdata,
        info.triple_out,config.triple_initial)
    info.triple_par[1] = abs(info.triple_par[1])
    info.triple_fit = butils.gauss_1d(info.triple_xdata,*info.triple_par)
    temp = config.side/config.triple_lim
    info.triple_par[1] = int(info.triple_par[1]*temp*10)/10

def run_3(info,config):
    # assign results for a single row
    fnum = info.cur_files
    info.results[fnum,0] = config.name_min+fnum
    info.results[fnum,1:4] = info.avg[:]
    
    # assign dual results for a single row
    for i in range(6):
        info.results[fnum,4+(i*7):4+(i*7)+5] = info.dual_par[i,:]
        info.results[fnum,4+(i*7)+5] = info.dual_used[i]
        info.results[fnum,4+(i*7)+6] = \
            np.sum((info.dual_out[i,:,:]-info.dual_fit[i,:,:])**2)
    
    # assign triple results for a single row
    info.results[fnum,4+(6*7):4+(6*7)+3] = info.triple_par[:]
    info.results[fnum,4+(6*7)+3:4+(6*7)+6] = 0
    info.results[fnum,4+(6*7)+6] = np.sum((info.triple_out-info.triple_fit)**2)

def run_4(info,config):
    if config.output_type == 'none': return
    if config.output_type == 'summary': return
    # save out and fit as files
    fprefix = ''
    fnum = info.cur_files
    fdir = config.output_directory
    if config.output_numbering != 'none':
        fidx = str.format(config.output_numbering,config.name_min+fnum) 
        fprefix = fidx + '_'
    for i in range(6):
        if i <  3: fcode = 'AC' 
        if i >= 3: fcode = 'XC'
        fpath1 = fdir + fprefix + fcode + ALL_COLORS[i] + '.txt'
        fpath2 = fdir + fprefix + fcode + ALL_COLORS[i] + 'Fit.txt'
        np.savetxt(fpath1, info.dual_out[i,:,:], fmt='%9.5f')
        np.savetxt(fpath2, info.dual_fit[i,:,:], fmt='%9.5f')
    fpath1 = fdir + fprefix + 'TripleCrgb.txt'
    fpath2 = fdir + fprefix + 'TripleCrgbFit.txt'
    np.savetxt(fpath1, info.triple_out, fmt='%9.5f')
    np.savetxt(fpath2, info.triple_fit, fmt='%9.5f')

def finish(info,config):    
    info.lib.destroy()
    if config.output_type == 'none': return
    
    # generate table header
    colors = '--r:--g:--b:-rg:-rb:-gb:rgb'.split(':')
    parameters = 'g(0):---w:ginf:--dx:--dy:used:norm'.split(':')
    temp_header_1 = ['']*49
    for i, color in enumerate(colors):
        for j, param in enumerate(parameters):
            temp_header_1[i*7+j] = str.format('|{}-{}-',color,param)
    scolors = '--r:--g:--b'.split(':')
    temp_header_2 = [str.format('|{}--avg-',color) for color in scolors]
    header = ' '*9 + ''.join(temp_header_2) + ''.join(temp_header_1)
    
    # output summary of results for the whole batch
    fpath = config.output_directory + 'results.txt'
    with open(fpath,'w') as f:
        f.write(header+'\n')
        np.savetxt(f,info.results,fmt='%9.5f',delimiter='|')

def run_once(info,config):
    run_0(info,config)
    run_1(info,config)
    run_2(info,config)
    run_3(info,config)
    run_4(info,config)

def run(info,config):
    setup(info,config)
    while True:
        cfiles = info.cur_files
        nfiles = info.num_files
        if cfiles >= nfiles: break
        print str.format('Processing {:5d} of {:5d} ...',cfiles+1,nfiles)
        run_once(info,config)
        info.cur_files += 1
    finish(info,config)
    print 'Done'

def main(): run(Info(),configs.BadConfig())  
if __name__ == "__main__": main()
