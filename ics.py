#!/usr/bin/env python
"""Command Line interface

This file contains the command line interface that uses the functions provided
by dual.py and triple.py to calculate the dual and triple correlation of an
image and write out the results.

Type './ics.py -h' for help on how to run this program.  A simple run might look
 like: ./ics.py -f RGBtemp.bmp pdata

Type 'python -m cProfile -s time ics.py [args here] > prof.txt' to profile this
program -- the profiling results will be in a 'prof.txt' file and sorted by
total time taken.
"""
from __future__ import division
import icsLogger # required, runs code on import
import argparse
import logging
import os
import numpy as np
import scipy.misc
import dual
import triple
import warnings
warnings.simplefilter('ignore', np.ComplexWarning)

logger = logging.getLogger("main")
ALL_COLORS = str.split('r:g:b:rg:rb:gb:rgb', ':')


def closeOptions(options):
    if options.infile_rgb:
        options.infile_rgb.close()
        options.infile_rgb = None
    if options.infile_r:
        options.infile_r.close()
        options.infile_r = None
    if options.infile_g:
        options.infile_g.close()
        options.infile_g = None
    if options.infile_b:
        options.infile_b.close()
        options.infile_b = None


def run(pdata, image_name, colors):
    if not os.path.exists(pdata):
        os.makedirs(pdata)
    image = scipy.misc.imread(image_name)
    r = image[:, :, 0].astype('d')
    g = image[:, :, 1].astype('d')
    b = image[:, :, 2].astype('d')
    n = None
    p = [(r, n, n), (g, n, n), (b, n, n), (r, g, n), (r, b, n), (g, b, n),
         (r, g, b)]
    res = np.empty((7, 3))
    np.ndarray.fill(res, np.nan)
    for color in colors:
        i = list.index(ALL_COLORS, color)
        res[i] = run_any(pdata, p[i][0], p[i][1], p[i][2], color)
    np.savetxt(path(pdata, image_name[:-4], 'txt'), res, fmt='%9.5f')


def run_any(pdata, a, b, c, color):
    if len(color) <= 2: return run_dual(pdata, a, b, c, color)
    if len(color) == 3: return run_trip(pdata, a, b, c, color)


def run_dual(pdata, a, b, c, color):
    range_val = 20
    initial_val = np.array([1, 10, 0], dtype=np.float64)
    gnew, gs, _ = dual.core(a, b, range_val, initial_val)
    gfit = gauss_2d(range_val, gs)
    if len(color) == 1: code = 'AC'
    if len(color) == 2: code = 'XC'
    fname1 = code + color
    fname2 = code + color + 'Fit'
    np.savetxt(path(pdata, fname1, 'txt'), gnew, fmt='%9.5f')
    np.savetxt(path(pdata, fname2, 'txt'), gfit, fmt='%9.5f')
    return gs


def run_trip(pdata, r, g, b, color):
    sr, sg, sb, avg_rgb = triple.core_0(r, g, b)
    lowlim = 48
    _, tcmat, lim, side = triple.core_1(sr, sg, sb, avg_rgb, lowlim)
    range_val = 15
    initial_val = np.array([50, 2, 0], dtype=np.float64)
    gnew, gs, _ = triple.core_2(tcmat, lim, side, range_val, initial_val)
    gfit = gauss_1d(range_val, gs)
    gs[1] = int(gs[1] * (side / lim) * 10) / 10
    fname1 = 'TripleCrgb'
    fname2 = 'TripleCrgbFit'
    np.savetxt(path(pdata, fname1, 'txt'), gnew, fmt='%9.5f', delimiter='\n')
    np.savetxt(path(pdata, fname2, 'txt'), gfit, fmt='%9.5f', delimiter='\n')
    return gs


def gauss_2d(range_val, gs):
    g1_sq = gs[1] ** 2
    gmn = np.empty((range_val, range_val))
    for a in xrange(range_val):
        for b in xrange(a + 1):
            gmn[a, b] = gs[0] * np.exp((-(a ** 2 + b ** 2)) / g1_sq) + gs[2]
    for a in xrange(range_val):
        for b in xrange(a + 1, range_val):
            gmn[a, b] = gmn[b, a]
    return gmn


def gauss_1d(range_val, gs):
    g1_sq = gs[1] ** 2
    delta_sq = np.arange(range_val) ** 2
    return gs[0] * np.exp(-delta_sq / g1_sq) + gs[2]


def path(directory, fname, ext):
    return str.format('{}{}{}.{}', directory, os.sep, fname, ext)


def main(options):
    logger.info("Recieved Args: %s", str(options))
    if options.infile_rgb:
        fname = options.infile_rgb.name
        logger.info("Using rgb path: %s", fname)
        closeOptions(options)
    elif options.infile_r and options.infile_g and options.infile_b:
        fnames = {}
        fnames['r'] = options.infile_r.name
        fnames['g'] = options.infile_g.name
        fnames['b'] = options.infile_b.name
        logger.info("Using red: %s", fnames['r'])
        logger.info("Using green: %s", fnames['g'])
        logger.info("Using blue: %s", fnames['b'])
        closeOptions(options)
    else:
        closeOptions(options)
        logger.error("Invalid arguements. Please supply infile_rgb or  all of \
infile_r, infile_g, and infile_b.")
        return
    run(options.output_dir, fname, ALL_COLORS)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Loads a single image or three\
 monocolored images.')
    parser.add_argument('-f', '--infile_rgb', type=argparse.FileType('r'))
    parser.add_argument('-r', '--infile_r', type=argparse.FileType('r'),
                        help="required infile_g and inflie_b, not yet supported")
    parser.add_argument('-g', '--infile_g', type=argparse.FileType('r'),
                        help="required infile_r and inflie_b, not yet supported")
    parser.add_argument('-b', '--infile_b', type=argparse.FileType('r'),
                        help="required infile_r and inflie_g, not yet supported")
    parser.add_argument('output_dir', help="name of output directory")
    args = parser.parse_args()
    main(args)
