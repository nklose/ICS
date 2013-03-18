"""Backend utilities

This file contains utility functions that are used by the backend.

Copryight (c) 2013 Nick Klose, Richard Leung, Cameron Mann, Glen Nelson,
Omar Qadri, and James Wang under the 401 IP License (see LICENSE file)
"""

from __future__ import division
import numpy as np
import scipy.misc

import os
import sys
import ctypes
from ctypes import c_int
from ctypes import c_void_p

def gauss_1d(x,g0,w,ginf):
    """Computes a 1d gaussian curve at various points

    Arguments:
        x: [n int] the points at which to calculate the function
        g0: [f64] the first parameter -- amplitude
        w: [f64] the second parameter -- width
        ginf: [f64] the third parameter -- value at infinity

    Return values:
        out: [n f64] the value of the gaussian curve with the
            given parameters at the points given in array x
    """
    return g0*np.exp(-(x**2)/(w**2))+ginf

def gauss_2d(x,g0,w,ginf):
    """Computes a 2d gaussian curve at various points

    Arguments:
        x: [n^2 int] the array from which the region to calculate
            the function over is obtained as [0,n) x [0,n)
        g0: [f64] the first parameter -- amplitude
        w: [f64] the second parameter -- width
        ginf: [f64] the third parameter -- value at infinity

    Return values:
        out: [n^2 f64] the value of the gaussian curve with the
            given parameters at the points obtained from array x
    """
    w_sq = w**2
    dim = int(np.sqrt(np.size(x)))
    return g0*np.exp((-((x//dim)**2+(x%dim)**2))/w_sq)+ginf

def gauss_2d_deltas(x,g0,w,ginf,dx,dy):
    """Computes a 2d gaussian curve at various points,
    considering deltas in the x and y directions

    Arguments:
        x: [n^2 int] the array from which the region to calculate
            the function over is obtained as [0,n) x [0,n)
        g0: [f64] the first parameter -- amplitude
        w: [f64] the second parameter -- width
        ginf: [f64] the third parameter -- value at infinity
        dx: [f64] the fourth parameter -- delta x
        dy: [f64] the fifth parameter -- delta y

    Return values:
        out: [n^2 f64] the value of the gaussian curve with the
            given parameters at the points obtained from array x
    """
    w_sq = w**2
    dim = int(np.sqrt(np.size(x)))
    return g0*np.exp((-(((x//dim)+dy)**2+((x%dim)+dx)**2))/w_sq)+ginf

def load_library():
    """Loads the C library used to speed up the program

    There are no arguments

    Return values:
        lib: the library that was loaded
    """
    lib_dir = os.path.dirname(os.path.realpath(__file__))
    if (os.name != 'nt'):
        lib_path = os.path.join(lib_dir, 'libbackend.so')
    else:
        lib_path = 'libbackend.dll'
    lib_path = verify_path(lib_path)
    lib = ctypes.cdll.LoadLibrary(lib_path)

    lib.core.argtypes = [c_void_p,c_void_p,c_void_p,c_void_p,c_int,c_int]
    lib.init.argtypes = [c_int,c_void_p]
    lib.execute.argtypes = []
    lib.destroy.argtypes = []
    return lib


def verify_path(path):
    """ I have to explain myself here for this hack.

        When cx_freeze compiles, it creates a huge ZIP file containing a bunch
        of things. However, libbackend.so does not go in there. Even if I force
        it to, the loader cannot load a so file inside the zip.  So
        BUILD_CONSTANTS is created during the build. Inside I have a variable,
        currently called HACKITY_HACK_HACK.  If this value exists, then I use it
        and set the lib_path correctly further on. If it doesn't exist, I do
        not.
    """
    try:
        root_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        if root_dir not in sys.path:
            sys.path.append(root_dir)
        from BUILD_CONSTANTS import HACKITY_HACK_HACK
    except ImportError:
        return path
    if HACKITY_HACK_HACK:
        return "backend.libbackend.so"
    return path

# a handle to the C library
backend_lib = load_library()
