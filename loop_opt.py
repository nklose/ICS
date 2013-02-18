"""Optimized loop

This file contains the loop needed in the core_1 function in
the triple.py file. This is an optimized implementation,
which loads a C routine to perform the computation.
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
    
