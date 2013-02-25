"""Regular loop

This file contains the loop needed in the core_1 function in
the triple.py file. This is a straightforward implementation,
focusing on simplicity and clarity.

Copryight (c) 2013 Nick Klose, Richard Leung, Cameron Mann, Glen Nelson, Omar
Qadri, and James Wang under the 401 IP License.

This Agreement, effective the 1st day of April 2013, is entered into by and
between Dr. Nils Petersen (hereinafter “client”) and the students of the
Biomembrane team (hereinafter “the development team”), in order to establish
terms and conditions concerning the completion of the Image Correlation
Spectroscopy application (hereinafter “The Application”) which is limited to the
application domain of application-domain (hereinafter “the domain of use for the
application”).  It is agreed by the client and the development team that all
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

    There are no return values.
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
