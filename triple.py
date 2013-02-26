"""Functions to compute triple correlation

This file contains functions that perform the core part of the triple
correlation procedure. The calculation is spread across three functions
to acommodate parts of the calculation that depend on user input, which in
turn may depend on the output of a previous part. These functions are not
stand-alone -- they are meant to be called by higher level programs which
interact with the user. The functions should be called in order, starting
from core_0 up until the core_2 function. The gauss_1d function is
meant only for internal use by the curve fitting routine.

In the unoptimized case, the majority of the time taken by these functions
is spent in a loop in the core_1 function. This loop is in a separate file.

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
import scipy.optimize
import loop_reg as loop

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
        avg_rgb: [f64] the product of the averages of the
            red, green, blue channels of the original image
    """
    avg_r = np.average(r)
    avg_g = np.average(g)
    avg_b = np.average(b)
    return (np.fft.fftshift(np.fft.fftn(r-avg_r)),
            np.fft.fftshift(np.fft.fftn(g-avg_g)),
            np.fft.fftshift(np.fft.fftn(b-avg_b)),
            avg_r*avg_g*avg_b)

def core_1(sr,sg,sb,avg_rgb,lowlim):
    """Computes the second part of the triple correlation

    Arguments:
        sr: [2^n 2^n c128] the preprocessed red channel
        sg: [2^n 2^n c128] the preprocessed green channel
        sb: [2^n 2^n c128] the preprocessed blue channel
        avg_rgb: [f64] the product of the averages of the
            red, green, blue channels of the original image
        lowlim: [int] the lower limit of part that requires
            further computation (this will be mirrored across
            the center of the image to obtain the upper limit)

    Return values:
        bsdisp: [lim lim f64] values needed to display the bispectrum
        tcmat: [lim lim 6 f64] values needed to display the triple
            correlation function and to compute the final results
        lim: [int] the difference between the upper and lower limits
        side: [int] the length in pixels of one side of the square image
    """
    side = np.shape(sr)[0]
    lim = side-(lowlim*2)
    tb = np.conj(sb)/(side**2)
    r1 = np.zeros((lim,lim,lim,lim),dtype=np.complex128)
    loop.core(r1,sr,sg,tb,side,lim)
    hlim = int(lim/2)
    bsdisp = np.float64(r1[:,:,hlim,hlim])
    tcorr = np.fft.ifftn(np.fft.fftshift(r1))
    tcmat = np.empty((lim,lim,6))
    tcmat[:,:,0] = np.float64(tcorr[:,:,0,0])
    tcmat[:,:,1] = np.float64(tcorr[0,:,:,0])
    tcmat[:,:,2] = np.float64(tcorr[0,0,:,:])
    tcmat[:,:,3] = np.float64(tcorr[0,:,0,:])
    tcmat[:,:,4] = np.float64(tcorr[:,0,:,0])
    tcmat[:,:,5] = np.float64(tcorr[:,0,0,:])
    tcmat *= lim**4/(side**4*avg_rgb)
    return (bsdisp,tcmat,lim,side)

def core_2(tcmat,lim,side,range_val,initial_val):
    """Computes the third (final) part of the triple correlation

    Arguments:
        tcmat: [lim lim 6 f64] values needed to display the triple
            correlation function and to compute the final results
        lim: [int] the difference between the upper and lower limits
        side: [int] the length in pixels of one side of the square image
        range_val: [int] the range to use for the computation
        initial_val: [3 f64] the initial guesses for the three curve
            fitting parameters -- amplitude, width and infinity value

    Return values:
        gnew: [range_val f64] the calculated result
        gs: [3 f64] the best curve-fitting parameters
        gcov: [3 3 f64] the estimated covariance
    """
    gnew = np.zeros(range_val)
    for i in range(6):
        gnew += tcmat[0,0:range_val,i]
        gnew += tcmat[0:range_val,0,i]
    gnew /= 12
    delta = np.arange(range_val)
    (gs,gcov) = scipy.optimize.curve_fit(gauss_1d,delta,gnew,initial_val)
    # since we later square w, we conventionally choose the positive value
    gs[1] = abs(gs[1])
    return (gnew,gs,gcov)

def gauss_1d(x,g0,g1,g2):
    """Computes a 1d gaussian curve at various points

    Arguments:
        x: [n int] the points at which to calculate the function
        g0: [f64] the first curve fitting parameter -- amplitude
        g1: [f64] the second curve fitting parameter -- width
        g2: [f64] the third curve fitting parameter -- value at infinity

    Return values:
        out: [n f64] the value of the gaussian curve with the
            given parameters at the points given in array x
    """
    return g0*np.exp(-(x**2)/(g1**2))+g2
