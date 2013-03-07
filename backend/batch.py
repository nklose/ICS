"""Runs a batch job

This file contains functions that run a batch job with a given
configuration. Three sample configurations are given below.
Run with 'python batch.py'.

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
import backend_utils as butils

import warnings
warnings.simplefilter('ignore',np.ComplexWarning)

raw_image = None
ALL_COLORS = str.split('r:g:b:rg:rb:gb:rgb',':')

def load_image(image,fpaths):
    if len(fpaths) == 1:
        raw_image = scipy.misc.imread(fpaths[0])
        for i in range(3):
            image[i,:,:] = raw_image[:,:,i].astype(np.float)
    elif len(fpaths) == 3:
        for i in range(3):
            raw_image = scipy.misc.imread(fpaths[i])
            image[i,:,:] = raw_image.astype(np.float)
    return 2**(8*raw_image.itemsize)

class MixedConfig:
    side = 128
    input_directory = '../accTests/inputs/RGBtemp/'
    output_directory = 'output/'
    name_min = 1
    name_max = 1
    name_format = 'rgb_{:03d}.bmp'
    dual_range = 20
    triple_range = 15
    auto_consider_deltas = False
    cross_consider_deltas = False
    dual_initial = np.array([1,10,0,0,0],dtype=np.float)
    triple_initial = np.array([50,2,0],dtype=np.float)
    triple_lim = 32
    input_type = 'mixed'
    output_type = 'full'
    output_numbering = 'none'

class SplitConfig:
    side = 128
    input_directory = '../accTests/inputs/RGBtemp/'
    output_directory = 'output/'
    name_min = 1
    name_max = 1
    name_format = '{:s}_{:03d}.bmp'
    dual_range = 20
    triple_range = 15
    auto_consider_deltas = False
    cross_consider_deltas = False
    dual_initial = np.array([1,10,0,0,0],dtype=np.float)
    triple_initial = np.array([50,2,0],dtype=np.float)
    triple_lim = 32
    input_type = 'split'
    output_type = 'summary'
    output_numbering = 'none'

class BadConfig:
    side = 512
    input_directory = '../accTests/inputs/badData/'
    output_directory = 'output/'
    name_min = 1
    name_max = 10
    name_format = '{:s}_{:03d}.bmp'
    dual_range = 20
    triple_range = 15
    auto_consider_deltas = False
    cross_consider_deltas = False
    dual_initial = np.array([1,10,0,0,0],dtype=np.float)
    triple_initial = np.array([50,2,0],dtype=np.float)
    triple_lim = 64
    input_type = 'split'
    output_type = 'summary'
    output_numbering = '{:03d}'

def run(config):
    
    # get a handle to the library
    lib = butils.backend_lib
    
    # create output directory if needed
    if not os.path.exists(config.output_directory):
        os.makedirs(config.output_directory)
    
    # declare python variables
    side = config.side
    image = np.empty((3,side,side))
    
    avg = np.empty(3)
    max_possible_pixel = None
    fft = np.empty((3,side,side), dtype=np.complex)
    conj_fft = np.empty((3,side,side), dtype=np.complex)
    dual_combinations = [(0,0),(1,1),(2,2),(0,1),(0,2),(1,2)]
    
    lim = config.triple_lim
    shifted = np.empty((3,side,side), dtype=np.complex)
    part_rgb = np.empty((6,lim,lim))
    
    # align data_rgb to 16-byte boundary
    nbytes = lim**4*16
    raw_data_rgb = np.empty(nbytes+16,dtype=np.uint8)
    start_idx = -raw_data_rgb.ctypes.data % 16
    data_rgb = raw_data_rgb[start_idx:start_idx+nbytes]\
        .view(dtype=np.complex).reshape(lim,lim,lim,lim)
    
    grid = np.ogrid[:lim,:lim]
    flip = 1-2*((grid[0]+grid[1])%2==1)
    
    dual_xdata = np.arange(config.dual_range**2)
    triple_xdata = np.arange(config.triple_range)
    
    # align dual_tmp to 16-byte boundary
    nbytes = side**2*16
    raw_dual_tmp = np.empty(nbytes+16,dtype=np.uint8)
    start_idx = -raw_dual_tmp.ctypes.data % 16
    dual_tmp = raw_dual_tmp[start_idx:start_idx+nbytes]\
        .view(dtype=np.complex).reshape(side,side)
    
    # store output results for dual correlations
    dual_out = np.empty((6,config.dual_range,config.dual_range))
    dual_fit = np.empty((6,config.dual_range,config.dual_range))
    dual_par = np.empty((6,5))
    dual_used = np.empty(6)
    
    # store output results for triple correlations
    triple_out = np.empty(config.triple_range)
    triple_fit = np.empty(config.triple_range)
    triple_par = np.empty(3)
    
    name_min = config.name_min
    name_fmt = config.name_format
    num_files = config.name_max-config.name_min+1
    
    # store summary results
    results = np.empty((num_files,53))
    
    # prepare arguments to pass to c code
    ilim = c_int(lim)
    iside = c_int(side)
    isr = shifted[0,:,:].ctypes.data_as(c_void_p)
    isg = shifted[1,:,:].ctypes.data_as(c_void_p)
    isb = shifted[2,:,:].ctypes.data_as(c_void_p)
    idata = data_rgb.ctypes.data_as(c_void_p);
    
    # initialize the c library
    lib.init(ilim,idata)
    
    for fnum in range(num_files):
        
        print str.format('Processing {:5d} of {:5d} ...',fnum+1,num_files)
        
        # generate file paths
        if config.input_type == 'mixed':
            fname = str.format(name_fmt,name_min+fnum)
            fpaths = [config.input_directory + fname]
        elif config.input_type == 'split':
            fpaths = ['','','']
            for i in range(3):
                fname = str.format(name_fmt,'rgb'[i],name_min+fnum)
                fpaths[i] = config.input_directory + fname
        else:
            print 'Invalid input type: ' + config.input_type
            sys.exit(1)
        
        # read image
        max_possible_pixel = load_image(image,fpaths)
        
        # perform some preprocessing
        for i in range(3):
            avg[i] = np.average(image[i,:,:])
            fft[i,:,:] = np.fft.fft2(image[i,:,:])
            conj_fft[i,:,:] = np.conj(fft[i,:,:])
        
        # perform dual correlation
        for i, comb in enumerate(dual_combinations):
            rval = config.dual_range
            denom = avg[comb[0]]*avg[comb[1]]*side**2
            dual_tmp = np.fft.ifft2(fft[comb[0],:,:]*conj_fft[comb[1],:,:])
            dual_out[i,:,:] = np.float64(dual_tmp[0:rval,0:rval])/denom - 1
            first_entry = dual_out[i,0,0]
            dual_out[i,0,0] = dual_out[i,0,1]
            
            # dual curve fitting
            if i<3: using_deltas = config.auto_consider_deltas
            if i>=3: using_deltas = config.cross_consider_deltas
            if using_deltas:
                (dual_par[i,:],_) = \
                    scipy.optimize.curve_fit(butils.gauss_2d_deltas,dual_xdata,
                    np.reshape(dual_out[i,:,:],rval**2),config.dual_initial)
                if (dual_par[i,3]>config.dual_initial[1] or \
                    dual_par[i,4]>config.dual_initial[1]): 
                    using_deltas = False
            if not using_deltas:
                (dual_par[i,0:3],_) = \
                    scipy.optimize.curve_fit(butils.gauss_2d,dual_xdata,
                    np.reshape(dual_out[i,:,:],rval**2),config.dual_initial[0:3])
                dual_par[i,3] = 0
                dual_par[i,4] = 0
            dual_par[i,1] = abs(dual_par[i,1])
            dual_fit[i,:,:] = butils.gauss_2d_deltas(dual_xdata,*dual_par[i,:])\
                .reshape(rval,rval)
            dual_used[i] = float(using_deltas)
            dual_out[i,0,0] = first_entry
        
        # perform triple correlation
        for i in range(3):
            shifted[i,:,:] = np.fft.fft2(image[i,:,:]-avg[i])
            shifted[i,:,:] = np.fft.fftshift(shifted[i,:,:])
        shifted[2,:,:] = np.conj(shifted[2,:,:])/(side**2)
        
        # call c functions
        lib.core(idata,isr,isg,isb,iside,ilim)
        lib.execute()
        
        # the line below uses the built-in function rather than fftw
        # if using this, multiply part_rgb by lim**4 rather than flip
        # data_rgb = np.fft.ifftn(data_rgb)
        
        part_rgb[0,:,:] = np.float64(data_rgb[:,:,0,0])
        part_rgb[1,:,:] = np.float64(data_rgb[0,:,:,0])
        part_rgb[2,:,:] = np.float64(data_rgb[0,0,:,:])
        part_rgb[3,:,:] = np.float64(data_rgb[0,:,0,:])
        part_rgb[4,:,:] = np.float64(data_rgb[:,0,:,0])
        part_rgb[5,:,:] = np.float64(data_rgb[:,0,0,:])
        part_rgb *= flip/(side**4*np.prod(avg))
        
        np.ndarray.fill(triple_out,0)
        for i in range(6):
            triple_out += part_rgb[i,0,0:config.triple_range]
            triple_out += part_rgb[i,0:config.triple_range,0]
        triple_out /= 12
        
        # triple curve fitting
        (triple_par[:],_) = \
            scipy.optimize.curve_fit(butils.gauss_1d,triple_xdata,
            triple_out,config.triple_initial)
        triple_par[1] = abs(triple_par[1])
        triple_fit = butils.gauss_1d(triple_xdata,*triple_par)
        triple_par[1] = int(triple_par[1]*(side/lim)*10)/10
        
        # assign results for a single row
        results[fnum,0] = name_min+fnum
        results[fnum,1:4] = avg[:]/max_possible_pixel
        
        # assign dual results for a single row
        for i in range(6):
            results[fnum,4+(i*7):4+(i*7)+5] = dual_par[i,:]
            results[fnum,4+(i*7)+5] = dual_used[i]
            results[fnum,4+(i*7)+6] = \
                np.sum((dual_out[i,:,:]-dual_fit[i,:,:])**2)
        
        # assign triple results for a single row
        results[fnum,4+(6*7):4+(6*7)+3] = triple_par[:]
        results[fnum,4+(6*7)+3:4+(6*7)+6] = 0
        results[fnum,4+(6*7)+6] = np.sum((triple_out-triple_fit)**2)
        
        # write out and fit only for output_type full
        if config.output_type == 'full':
            fprefix = ''
            fdir = config.output_directory
            if config.output_numbering != 'none':
                fidx = str.format(config.output_numbering,name_min+fnum) 
                fprefix = fidx + '_'
            for i in range(6):
                if i <  3: fcode = 'AC' 
                if i >= 3: fcode = 'XC'
                fpath1 = fdir + fprefix + fcode + ALL_COLORS[i] + '.txt'
                fpath2 = fdir + fprefix + fcode + ALL_COLORS[i] + 'Fit.txt'
                np.savetxt(fpath1, dual_out[i,:,:], fmt='%9.5f')
                np.savetxt(fpath2, dual_fit[i,:,:], fmt='%9.5f')
            fpath1 = fdir + fprefix + 'TripleCrgb.txt'
            fpath2 = fdir + fprefix + 'TripleCrgbFit.txt'
            np.savetxt(fpath1, triple_out, fmt='%9.5f')
            np.savetxt(fpath2, triple_fit, fmt='%9.5f')
        # end write

    # clean up the c library
    lib.destroy()
    
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
        np.savetxt(f,results,fmt='%9.5f',delimiter='|')
    print 'Done'

def main(): run(MixedConfig())  
if __name__ == "__main__": main()
