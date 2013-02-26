"""Functions to compute the dual (auto and cross) correlation

This file contains functions that perform the core part of the dual
correlation. The main calculation is done by the core function. This
function is not stand-alone -- it is meant to be called by higher level
programs which interact with the user. The gauss_2d function is meant
only for internal use by the curve fitting routine.

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
        gnew: [range_val range_val f64] the calculated result
        gs: [3 f64] the best curve-fitting parameters
        gcov: [3 3 f64] the estimated covariance
    """
    if image2 == None:
        denom = np.average(image1)**2*np.size(image1)
        temp1 = np.fft.fft2(image1)
        temp2 = np.conj(temp1)
    else:
        denom = np.average(image1)*np.average(image2)*np.size(image1)
        temp1 = np.fft.fft2(image1)
        temp2 = np.conj(np.fft.fft2(image2))
    g = np.fft.ifft2(temp1*temp2)
    gnew = np.float64(g[0:range_val,0:range_val])/denom-1
    temp = gnew[0,0]
    gnew[0,0] = gnew[0,1]
    xdata = np.arange(range_val**2)
    ydata = np.reshape(gnew,range_val**2)
    (gs,gcov) = scipy.optimize.curve_fit(gauss_2d,xdata,ydata,initial_val)
    # since we later square w, we conventionally choose the positive value
    gs[1] = abs(gs[1])
    gnew[0,0] = temp
    return (gnew,gs,gcov)

def gauss_2d(x,g0,g1,g2):
    """Computes a 2d gaussian curve at various points

    Arguments:
        x: [n^2 int] the array from which the region to calculate
            the function over is obtained as [0,n) x [0,n)
        g0: [f64] the first curve fitting parameter -- amplitude
        g1: [f64] the second curve fitting parameter -- width
        g2: [f64] the third curve fitting parameter -- value at infinity

    Return values:
        out: [n^2 f64] the value of the gaussian curve with the
            given parameters at the points obtained from array x
    """
    g1_sq = g1**2
    dim = int(np.sqrt(np.size(x)))
    return g0*np.exp((-((x//dim)**2+(x%dim)**2))/g1_sq)+g2
