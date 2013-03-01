"""Functions to compute triple correlation

This file contains functions that perform the core part of the triple
correlation procedure. The calculation is spread across three functions
to acommodate parts of the calculation that depend on user input, which in
turn may depend on the output of a previous part. These functions are not
stand-alone -- they are meant to be called by higher level programs which
interact with the user. The functions should be called in order, starting
from core_0 up until the core_2 function.

Copryight (c) 2013 Nick Klose, Richard Leung, Cameron Mann, Glen Nelson,
Omar Qadri, and James Wang under the 401 IP License (see LICENSE file)
"""

from __future__ import division
import numpy as np
import scipy.optimize
import backend_utils as butils

import ctypes
from ctypes import c_int
from ctypes import c_void_p

def core_0(r,g,b):
    """Computes the first part of the triple correlation

    Arguments:
        r: [2^n 2^n f64] the red channel of the image
        g: [2^n 2^n f64] the green channel of the image
        b: [2^n 2^n f64] the blue channel of the image

    Return values:
        sr: [2^n 2^n c128] the preprocessed red channel
        sg: [2^n 2^n c128] the preprocessed green channel
        sb: [2^n 2^n c128] the preprocessed blue channel
    """
    avg_r = np.average(r)
    avg_g = np.average(g)
    avg_b = np.average(b)
    return (np.fft.fftshift(np.fft.fftn(r-avg_r)),
            np.fft.fftshift(np.fft.fftn(g-avg_g)),
            np.fft.fftshift(np.fft.fftn(b-avg_b)))

def core_1(sr,sg,sb,avg_rgb,lim):
    """Computes the second part of the triple correlation

    Arguments:
        sr: [2^n 2^n c128] the preprocessed red channel
        sg: [2^n 2^n c128] the preprocessed green channel
        sb: [2^n 2^n c128] the preprocessed blue channel
        avg_rgb: [f64] the product of the averages of the
            red, green, blue channels of the original image
        lim: [2^n] the length of the side of part that requires
            further computation (the part is square, so this sets
            the sides for all dimensions)

    Return values:
        part_rgb: [lim lim 6 f64] values needed to display the
            triple correlation and to compute the final results
    """
    side = np.shape(sr)[0]
    sb = np.conj(sb)/(side**2)
    data_rgb = np.zeros((lim,lim,lim,lim),dtype=np.complex128)
    
    idata = data_rgb.ctypes.data_as(c_void_p)
    isr = sr.ctypes.data_as(c_void_p)
    isg = sg.ctypes.data_as(c_void_p)
    isb = sb.ctypes.data_as(c_void_p)
    iside = c_int(side)
    ilim = c_int(lim)
    
    lib = butils.backend_lib
    lib.core(idata,isr,isg,isb,iside,ilim)
    data_rgb = np.fft.ifftn(np.fft.fftshift(data_rgb))
    part_rgb = np.empty((lim,lim,6))
    part_rgb[:,:,0] = np.float64(data_rgb[:,:,0,0])
    part_rgb[:,:,1] = np.float64(data_rgb[0,:,:,0])
    part_rgb[:,:,2] = np.float64(data_rgb[0,0,:,:])
    part_rgb[:,:,3] = np.float64(data_rgb[0,:,0,:])
    part_rgb[:,:,4] = np.float64(data_rgb[:,0,:,0])
    part_rgb[:,:,5] = np.float64(data_rgb[:,0,0,:])
    part_rgb *= lim**4/(side**4*avg_rgb)
    return part_rgb

def core_2(part_rgb,range_val,initial_val):
    """Computes the third (final) part of the triple correlation

    Arguments:
        part_rgb: [lim lim 6 f64] values needed to display the triple
            correlation function and to compute the final results
        range_val: [int] the range to use for the computation
        initial_val: [3 f64] the initial guesses for the three curve
            fitting parameters -- amplitude, width and infinity value

    Return values:
        out: [range_val f64] the calculated result
        par: [3 f64] the best curve-fitting parameters
    """
    lim = part_rgb.shape[1]
    out = np.zeros(range_val)
    for i in range(6):
        out += part_rgb[0,0:range_val,i]
        out += part_rgb[0:range_val,0,i]
    out /= 12
    xdata = np.arange(range_val)
    (par,_) = scipy.optimize.curve_fit(butils.gauss_1d,
        np.arange(range_val),out,initial_val)
    # since we later square w, we conventionally choose the positive value
    par[1] = abs(par[1])
    return (out,par)

