"""Functions to compute the dual (auto and cross) correlation

This file contains functions that perform the core part of the dual
correlation. The main calculation is done by the core function. This
function is not stand-alone -- it is meant to be called by higher level
programs which interact with the user.

Copryight (c) 2013 Nick Klose, Richard Leung, Cameron Mann, Glen Nelson,
Omar Qadri, and James Wang under the 401 IP License (see LICENSE file)
"""

from __future__ import division
import numpy as np
import scipy.optimize
import backend_utils as butils

def core(image1,image2,range_val,initial_val):
    """Computes the auto or cross correlation

    Arguments:
        image1: [2^n 2^n f64] the first image
        image2: [2^n 2^n f64] the second image; if the function is
            used to compute autocorrelation, this arg should be None
        range_val: [int] the range to use for the computation
        initial_val: [3 f64] the initial guesses for the three curve
            fitting parameters -- amplitude, width and infinity value

    Return values:
        out: [range_val range_val f64] the calculated result
        par: [3 f64] the best curve-fitting parameters
    """
    if image2 == None:
        denom = np.average(image1)**2*np.size(image1)
        temp1 = np.fft.fft2(image1)
        temp2 = np.conj(temp1)
    else:
        denom = np.average(image1)*np.average(image2)*np.size(image1)
        temp1 = np.fft.fft2(image1)
        temp2 = np.conj(np.fft.fft2(image2))
    tmp = np.fft.ifft2(temp1*temp2)
    out = np.float64(tmp[0:range_val,0:range_val])/denom-1
    first_entry = out[0,0]
    out[0,0] = out[0,1]
    xdata = np.arange(range_val**2)
    ydata = np.reshape(out,range_val**2)
    (par,_) = scipy.optimize.curve_fit(butils.gauss_2d,xdata,ydata,initial_val)
    # since we later square w, we conventionally choose the positive value
    par[1] = abs(par[1])
    out[0,0] = first_entry
    return (out,par)
