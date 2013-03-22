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

import warnings
warnings.simplefilter('ignore', np.ComplexWarning)


def core(image1, image2, range_val, initial_val, consider_deltas):
    """Computes the auto or cross correlation

    Arguments:
        image1: [n n f64] the first image
        image2: [n n f64] the second image; if the function is
            used to compute autocorrelation, this arg should be None
        range_val: [int] the range to use for the computation
        initial_val: [5 f64] the initial guesses for the five curve fitting
            parameters -- amplitude, width, infinity value and deltas
        consider_deltas: [boolean] whether or not to consider deltas

    Return values:
        out: [range_val range_val f64] the calculated result
        par: [5 f64] the best curve-fitting parameters
        using_deltas: [boolean] whether the parameters were
            calculated with or without using deltas
    """
    if image2 is None:
        denom, temp1, temp2 = _get_single_image_values(image1)
    else:
        denom, temp1, temp2 = _get_two_image_values(image1, image2)
    first_entry, xdata, ydata, par, out = _get_inputs(range_val, temp1, temp2,
                                                      denom)
    using_deltas = consider_deltas
    if using_deltas:
        par, using_deltas = _get_deltas(par, xdata, ydata, initial_val)
    if not using_deltas:
        par = _default_no_deltas(par, xdata, ydata, initial_val)
    # since we later square w, we conventionally choose the positive value
    par[1] = abs(par[1])
    out[0, 0] = first_entry
    return (out, par, using_deltas)


def _get_single_image_values(image1):
    """Handles the single image (auto) case.

    Arguments:
        image1: [n n f64] the first image

    Return values:
        denom: [f64] a mathamatical constant used elsewhere
        temp1: [n n f64] The two dimensional fourier transform of the first
               image.
        temp2: [n n f64] The complex conjugate of the temp1.
    """
    denom = np.average(image1) ** 2 * np.size(image1)
    temp1 = np.fft.fft2(image1)
    temp2 = np.conj(temp1)
    return denom, temp1, temp2


def _get_two_image_values(image1, image2):
    """Handles the two image (cross) case.

    Arguments:
        image1: [n n f64] the first image
        image2: [n n f64] the second image

    Return values:
        denom: [f64] a mathamatical constant used elsewhere
        temp1: [n n f64] The two dimensional fourier transform of the first
               image.
        temp2: [n n f64] The complex conjugate of the two dimensional fourier
               transform of the second image.
    """
    denom = np.average(image1) * np.average(image2) * np.size(image1)
    temp1 = np.fft.fft2(image1)
    temp2 = np.conj(np.fft.fft2(image2))
    return denom, temp1, temp2


def _get_inputs(range_val, temp1, temp2, denom):
    """Handles the two image (cross) case.

    Arguments:
        range_val: [int] the range to use for the computation
        denom: [f64] a mathamatical constant
        temp1: [n n f64] The two dimensional fourier transform of the first
               image
        temp2: [n n f64] The complex conjugate of a fourier transform

    Return values:
        first_entry: The first entry of the calculated result
        xdata: [n f64] the xdata of the graph based on the range value
        ydata: [n f64] the output reshaped to fit as the ydata of the graph
        par: [5 f64] the best curve-fitting parameters
        out: [range_val range_val f64] the calculated result
    """
    tmp = np.fft.ifft2(temp1 * temp2)
    out = np.float64(tmp[0:range_val, 0:range_val]) / denom - 1
    first_entry = out[0, 0]
    out[0, 0] = out[0, 1]
    xdata = np.arange(range_val ** 2)
    ydata = np.reshape(out, range_val ** 2)
    par = np.zeros(5)
    return first_entry, xdata, ydata, par, out


def _get_deltas(par, xdata, ydata, initial_val):
    """Attempts to find any applicable deltas while curve fitting.

    Arguments:
        par: [5 f64] the best curve-fitting parameters
        xdata: [n f64] the xdata of the graph based on the range value
        ydata: [n f64] the output reshaped to fit as the ydata of the graph
        initial_val: [5 f64] the initial guesses for the five curve fitting
            parameters -- amplitude, width, infinity value and deltas

    Return values:
        par: [5 f64] the best curve-fitting parameters

        using_deltas: [bool] Whether deltas are being used
    """
    using_deltas = True
    (par, _) = scipy.optimize.curve_fit(butils.gauss_2d_deltas, xdata, ydata,
                                        initial_val)
    if par[3] > initial_val[1] or par[4] > initial_val[1]:
        using_deltas = False
    return par, using_deltas


def _default_no_deltas(par, xdata, ydata, initial_val):
    """ Curve fits without using deltas.

    Arguments:
        par: [5 f64] the best curve-fitting parameters
        xdata: [n f64] the xdata of the graph based on the range value
        ydata: [n f64] the output reshaped to fit as the ydata of the graph
        initial_val: [5 f64] the initial guesses for the five curve fitting
            parameters -- amplitude, width, infinity value and deltas

    Return values:
        par: [5 f64] the best curve-fitting parameters
    """
    (par[0:3], _) = scipy.optimize.curve_fit(butils.gauss_2d, xdata, ydata,
                                             initial_val[0:3])
    par[3] = 0
    par[4] = 0
    return par
