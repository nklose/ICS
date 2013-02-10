"""Regular loop

This file contains the loop needed in the core_1 function in
the triple.py file. This is a straightforward implementation,
focusing on simplicity and clarity.
"""

from __future__ import division
import numpy as np

def core(r1,sr,sg,tb,side,lim):
    """
    Performs the loop required by the second part of
    the triple correlation (ie. the core_1 function)
    
    Arguments:
        sr: [2^n 2^n c128] the preprocessed red channel
        sg: [2^n 2^n c128] the preprocessed green channel
        tb: [2^n 2^n c128] the complex conjugate of the
            preprocessed blue channel of the image
        side: [int] the length of one side of the image
        lim: [int] the length of one side of the portion of
            the image over which to perform the computation
        r1: [lim lim lim lim c128] the array in which
            to store the results of the computation
            
    This function has no return values.
    """
    na = int(side/2)
    nb = int(lim/2)
    lowlim = na-nb
    low = lowlim-na
    high = na-lowlim
    for v1 in xrange(low,high):
        for u1 in xrange(low-min(v1-1,0),high-max(v1,0)):
            for v2 in xrange(low,high):
                for u2 in xrange(low,high):
                    if abs(u2+v2) < na:
                        r1[nb+v1,nb+u1,nb+v2,nb+u2] = \
                          sr[na+u1,na+u2] * \
                          sg[na+v1,na+v2] * \
                          tb[na+u1+v1,na+u2+v2]
