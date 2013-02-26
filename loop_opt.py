"""Optimized loop

This file contains the loop needed in the core_1 function in
the triple.py file. This is an optimized implementation,
which loads a C routine to perform the computation.

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
import ctypes
import os
from ctypes import c_void_p
from ctypes import c_int

# todo: the procedure for loading shared libraries may
# be different on windows -- need to add support for that
dir = os.path.dirname(os.path.realpath(__file__))
path = str.format('{}{}{}.so',dir,os.sep,'libloop')
lib = ctypes.cdll.LoadLibrary(path)
lib.core.argtypes = [c_void_p,c_void_p,c_void_p,c_void_p,c_int,c_int]

def core(r1,sr,sg,tb,side,lim):
    """
    See the core function of loop_reg.py for a description
    of this function and its arguments and return values.
    """
    ir1 = r1.ctypes.data_as(c_void_p)
    isr = sr.ctypes.data_as(c_void_p)
    isg = sg.ctypes.data_as(c_void_p)
    itb = tb.ctypes.data_as(c_void_p)
    iside = c_int(side)
    ilim = c_int(lim)
    lib.core(ir1,isr,isg,itb,iside,ilim)
