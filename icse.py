import numpy as np
import scipy as sp
import scipy.misc
import scipy.optimize
import matplotlib.pyplot as pp
import os
import math
import sys
import warnings
import logging
warnings.simplefilter("ignore", np.ComplexWarning)

# this file is _experimental_ and
# things are still being tried out

LOGGER = logging.getLogger("icse")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")


def ics_run(tt):
    image = sp.misc.imread('RGBtemp.bmp')
    r = image[:, :, 0].astype('d')
    g = image[:, :, 1].astype('d')
    b = image[:, :, 2].astype('d')
    rval = 20
    init = np.array([1, 10, 0], dtype=np.float64)
    res = np.empty((7, 3))
    res[:] = np.nan
    LOGGER.info("Running tests")
    if tt in ('', 'x', 'r'): res[0] = ics_single(r, 'r', rval, init)
    if tt in ('', 'x', 'g'): res[1] = ics_single(g, 'g', rval, init)
    if tt in ('', 'x', 'b'): res[2] = ics_single(b, 'b', rval, init)
    if tt in ('', 'xx', 'rg'): res[3] = ics_double(r, g, 'r', 'g', rval, init)
    if tt in ('', 'xx', 'rb'): res[4] = ics_double(r, b, 'r', 'b', rval, init)
    if tt in ('', 'xx', 'gb'): res[5] = ics_double(g, b, 'g', 'b', rval, init)
    if tt in ('', 'xxx', 'rgb'): res[6] = ics_triple(r, g, b, rval, init)
    ics_save_res(os.path.join(OUTPUT_DIR, 'newRGBtemp.txt'), res)
    LOGGER.info("Done tests")


def ics_entire_test():
    ics_run('')


def ics_single_test():
    ics_run('x')


def ics_double_test():
    ics_run('xx')


def ics_single(image, color, range_val, initial_val):
    size = np.size(image)
    avg = np.average(image)
    inside = (np.fft.fft2(image) * np.conj(np.fft.fft2(image)))
    g = np.float64((np.fft.ifft2(inside) / (avg ** 2 * size)) - 1)
    (gnew, gfit, gs) = ics_compute(g, range_val, initial_val)
    fname1 = os.path.join(OUTPUT_DIR, 'newAC%s.txt' % color)
    fname2 = os.path.join(OUTPUT_DIR, 'newAC%sFit.txt' % color)
    ics_save(fname1, fname2, gnew, gfit)
    ics_plot(gnew, gfit, color)
    return gs


def ics_double(image1, image2, color1, color2, range_val, initial_val):
    size = np.size(image1)
    avg1 = np.average(image1)
    avg2 = np.average(image2)
    inside = (np.fft.fft2(image1) * np.conj(np.fft.fft2(image2)))
    g = np.float64((np.fft.ifft2(inside) / (avg1 * avg2 * size)) - 1)
    (gnew, gfit, gs) = ics_compute(g, range_val, initial_val)
    color = color1 + color2
    fname1 = os.path.join(OUTPUT_DIR, 'newXC%s.txt' % color)
    fname2 = os.path.join(OUTPUT_DIR, 'newXC%sFit.txt' % color)
    ics_save(fname1, fname2, gnew, gfit)
    ics_plot(gnew, gfit, color)
    return gs


def ics_triple(r, g, b, range_val, initial_val):
    # todo, incomplete
    return np.zeros(3)


def ics_compute(g, range_val, initial_val):
    gnew = g[0:range_val, 0:range_val]
    temp = gnew[0, 0]
    gnew[0, 0] = gnew[0, 1]
    xdata = np.arange(range_val ** 2)
    ydata = np.reshape(gnew, range_val ** 2)
    gs = sp.optimize.curve_fit(ics_corr_opt, xdata, ydata, initial_val)[0]
    # since we later square w, we conventionally choose the positive value
    gs[1] = abs(gs[1])
    gfit = ics_corr(range_val, gs)
    gnew[0, 0] = temp
    return (gnew, gfit, gs)


def ics_save(fname1, fname2, gnew, gfit):
    LOGGER.debug("Saving: %s, %s", fname1, fname2)
    np.savetxt(fname1, gnew, fmt='%5.4f', delimiter='\t')
    np.savetxt(fname2, gfit, fmt='%5.4f', delimiter='\t')


def ics_plot(gnew, gfit, color):
    range_val = np.shape(gnew)[0]
    fname = os.path.join(OUTPUT_DIR, 'newFG%s.png' % color)
    pp.clf()
    pp.title(ics_gen_title(color, 'Y'))
    pp.plot(np.arange(0, range_val), gfit[0:, 0], ics_gen_style('--', color),
            np.arange(1, range_val), gnew[1:, 0], ics_gen_style('o', color),
            linewidth=2.0)
    pp.axis([0, range_val, 0, max(gfit[0, 0], gnew[1, 0])])
    pp.savefig(fname)


def ics_gen_title(color, axis):
    s = ''
    if len(color) == 1: s += 'Autocorrelation '
    if len(color) == 2: s += 'Crosscorrelation '
    if color in ('r', 'rg', 'rb'): s += 'Red '
    if color in ('g', 'rg', 'gb'): s += 'Green '
    if color in ('b', 'rb', 'gb'): s += 'Blue '
    return s + axis


def ics_gen_style(style, color):
    s = style
    if len(color) == 1: return s + color
    if color == 'rg': return s + 'y'
    if color == 'rb': return s + 'm'
    if color == 'gb': return s + 'c'


def ics_save_res(fname, res):
    names = ['red', 'green', 'blue',
             'red-green', 'red-blue', 'green-blue',
             'red-green-blue']
    r0 = r1 = r2 = None
    fmt = '%-19s%-10s%-10s%-10s\n'
    f = open(fname, 'w+')
    f.write(fmt % ('parameters:', 'G(0)', 'w', 'Ginf'))
    f.write('\n')
    for i, name in enumerate(names):
        r0 = r1 = r2 = ''
        if not np.isnan(res[i, 0]): r0 = '%7.5f' % res[i, 0]
        if not np.isnan(res[i, 1]): r1 = '%7.5f' % res[i, 1]
        if not np.isnan(res[i, 2]): r2 = '%7.5f' % res[i, 2]
        f.write(fmt % (name.upper(), r0, r1, r2))
    f.close()


def ics_corr(size, gs):
    gmn = np.empty((size, size))
    for a in range(size):
        for b in range(a + 1):
            exponent = (-(a ** 2 + b ** 2)) / (gs[1] ** 2)
            gmn[a, b] = gs[0] * math.exp(exponent) + gs[2]
    for a in range(size):
        for b in range(a + 1, size):
            gmn[a, b] = gmn[b, a]
    return gmn


def ics_corr_opt(x, g0, g1, g2):
    size = np.size(x)
    dim = int(math.sqrt(size))
    return g0 * np.exp((-((x / dim) ** 2 + (x % dim) ** 2)) / (g1 ** 2)) + g2


def ics_corr_test():
    gmn = ics_corr(20, np.array([3.9434, 4.7035, 0.1902]))
    np.savetxt(sys.stdout, gmn, '%5.4f')


def ics_corr_opt_test():
    # Guessing this is just a debug function?
    gmn = np.reshape(ics_corr_opt(np.arange(400), 3.9434,
                                  4.7035, 0.1902), (20, 20))
    np.savetxt(sys.stdout, gmn, '%5.4f')
