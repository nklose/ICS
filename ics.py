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
import icsLogger # required, runs code on import
import argparse
import logging
import os
import numpy as np
import scipy.misc
import dual
import triple
import warnings
import graph
import image_reader
from color import COLOR
warnings.simplefilter('ignore', np.ComplexWarning)

logger = logging.getLogger("main")
ALL_COLORS = str.split('r:g:b:rg:rb:gb:rgb', ':')
ALL_INPUT_COLORS = [[COLOR.RED], [COLOR.GREEN], [COLOR.BLUE],
                    [COLOR.RED, COLOR.GREEN], [COLOR.RED, COLOR.BLUE],
                    [COLOR.GREEN, COLOR.BLUE],
                    [COLOR.RED, COLOR.GREEN, COLOR.BLUE]]


def color_to_string(color):
    """ Converts a color enum list to the string representation.

    Arguments:
        color: The colors to convert.
        color type: list

    Return Value:
        The colors as a string.
    """
    return "".join(color)


def closeOptions(options):
    """ Checks the options object for any file objects it has open, and
        closes them.

    Arguments:
        options: The object returned by argparse.
        options type: Type
    """
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


def run(output_dir, red_image, green_image, blue_image, image_name, colors,
        generate_graphs, auto_only=False, cross_only=False, triple_only=False):
    """ Run the correlations.

    Arguments:
        output_dir: The directory to output values to.
        output_dir type: string

        red_image: the red channel of the image.
        red_image type: nparray

        green_image: the green channel of the image.
        green_image type: nparray

        blue_image: the blue channel of the image.
        blue_image type: nparray

        image_name: the name of the image to use.
        image_name type: string

        colors: Correlations to call based on their colors.
        colors type: list

        generate_graphs: Whether to generate graphs or not
        generate_graphs type: bool

        auto_only: Whether to generate auto-correlation images only. Defaults to
                   False.
        auto_only type: bool

        cross_only: Whether to generate cross-correlation images only. Defaults
                    to False.
        cross_only type: bool

        triple_only: Whether to generate triple-correlation images only.
                     Defaults to False.
        triple_only type: bool
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    all_image_combinations = [(red_image, None, None),
                              (green_image, None, None),
                              (blue_image, None, None),
                              (red_image, green_image, None),
                              (red_image, blue_image, None),
                              (green_image, blue_image, None),
                              (red_image, green_image, blue_image)]
    if auto_only:
        image_combinations = all_image_combinations[0:3]
    elif cross_only:
        image_combinations = all_image_combinations[3:6]
    elif triple_only:
        image_combinations = all_image_combinations[-1:]
    else:
        image_combinations = all_image_combinations
    result = np.empty((7, 3))
    np.ndarray.fill(result, np.nan)
    for color in colors:
        i = list.index(ALL_INPUT_COLORS, color)
        result[i] = choose_correlation(output_dir, image_combinations[i][0],
                                       image_combinations[i][1],
                                       image_combinations[i][2],
                                       color, generate_graphs)
    np.savetxt(path(output_dir, image_name[:-4], 'txt'), result, fmt='%9.5f')


def choose_correlation(output_dir, first_image, second_image, third_image,
                       color, generate_graphs):
    """ Deterimine which correlation to run and then run it.

    Arguments:
        output_dir: The directory to output values to.
        output_dir type: string

        first_image: ???
        first_image type: ???

        second_image: ???
        second_image type: ???

        third_image: ???
        third_image type: ???

        color: Representation of the used colors
        color type: list

        generate_graphs: Whether to generate graphs or not
        generate_graphs type: bool

    Return Value:
        ???
    """
    if len(color) <= 2: return run_dual(output_dir, first_image, second_image,
                                        color, generate_graphs)
    if len(color) == 3: return run_trip(output_dir, first_image, second_image,
                                        third_image, color, generate_graphs)


def run_dual(output_dir, first_image, second_image, color, generate_graphs):
    """ Run a correlation between two images.

    Arguments:
        output_dir: The directory to output values to.
        output_dir type: string

        first_image: ???
        first_image type: ???

        second_image: ???
        second_image type: ???

        color: Representation of the used colors
        color type: list

        generate_graphs: Whether to generate graphs or not
        generate_graphs type: bool

    Return Value:
        ???
    """
    range_val = 20
    initial_val = np.array([1, 10, 0], dtype=np.float64)
    gnew, gs, _ = dual.core(first_image, second_image, range_val, initial_val)
    gfit = gauss_2d(range_val, gs)
    if len(color) == 1: fprefix = 'AC'
    if len(color) == 2: fprefix = 'XC'
    fname1 = fprefix + color_to_string(color)
    fname2 = fprefix + color_to_string(color) + 'Fit'
    np.savetxt(path(output_dir, fname1, 'txt'), gnew, fmt='%9.5f')
    np.savetxt(path(output_dir, fname2, 'txt'), gfit, fmt='%9.5f')
    if generate_graphs:
        graph.plot(gnew, gfit, color, directory=output_dir)
    return gs


def run_trip(output_dir, red_image, green_image, blue_image, color,
             generate_graphs):
    """ Run the Triple correlation

    Arguments:
        output_dir: The directory to output values to.
        output_dir type: string

        red_image: ???
        red_image type: ???

        green_image: ???
        green_image type: ???

        blue_image: ???
        blue_image type: ???

        color: Representation of the used colors
        color type: list

        generate_graphs: Whether to generate graphs or not
        generate_graphs type: bool

    Return Value:
        ???
    """
    sr, sg, sb, avg_rgb = triple.core_0(red_image, green_image, blue_image)
    lowlim = 48
    _, tcmat, lim, side = triple.core_1(sr, sg, sb, avg_rgb, lowlim)
    range_val = 15
    initial_val = np.array([50, 2, 0], dtype=np.float64)
    gnew, gs, _ = triple.core_2(tcmat, lim, side, range_val, initial_val)
    gfit = gauss_1d(range_val, gs)
    gs[1] = int(gs[1] * (side / lim) * 10) / 10
    fname1 = 'TripleCrgb'
    fname2 = 'TripleCrgbFit'
    np.savetxt(path(output_dir, fname1, 'txt'), gnew, fmt='%9.5f',
               delimiter='\n')
    np.savetxt(path(output_dir, fname2, 'txt'), gfit, fmt='%9.5f',
               delimiter='\n')
    if generate_graphs:
        graph.plot(gnew, gfit, color, directory=output_dir)
    return gs


def gauss_2d(range_val, gs):
    """ TODO: Figuring out.

    Arguments:
        range_val: ???
        range_val type: ???

        gs: ???
        gs type: ???

    Return Value:
        ???
    """
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
    """ TODO: Figuring out.

    Arguments:
        range_val: ???
        range_val type: ???

        gs: ???
        gs type: ???

    Return Value:
        ???
    """
    g1_sq = gs[1] ** 2
    delta_sq = np.arange(range_val) ** 2
    return gs[0] * np.exp(-delta_sq / g1_sq) + gs[2]


def path(directory, filename, extension):
    """ Generate the given file path

    Arguments:
        directory: The directory the file should be in.
        directory type: string

        filename: The name of the file. eg. "test"
        filename type: string

        extension: The extension of the file. Eg. "txt"
        extension type: string

    Return Value:
        Filepath string formated appropiately for the operating system.
    """
    return os.path.join(directory, "%s.%s" % (filename, extension))


def main(options):
    """ Main function, handles options and calls correct functions.

    Arguments:
        options: Object holding options from the argparse library parser.
        options type: type
    """
    logger.debug("Recieved Args: %s", str(options))
    if options.infile_rgb:
        fname = options.infile_rgb.name
        logger.info("Using rgb path: %s", fname)
        closeOptions(options)
        redChannel, greenChannel, blueChannel = image_reader.\
            get_channels_single(fname)
    elif options.infile_r and options.infile_g and options.infile_b:
        fnames = (options.infile_r.name, options.infile_g.name,
                  options.infile_b.name)
        logger.info("Using red: %s", fnames[0])
        logger.info("Using green: %s", fnames[1])
        logger.info("Using blue: %s", fnames[2])
        closeOptions(options)
        redChannel, greenChannel, blueChannel = image_reader.\
            get_channels_separate(*fnames)
    else:
        closeOptions(options)
        logger.error("Invalid arguments. Please supply infile_rgb or all of \
infile_r, infile_g, and infile_b.")
        return
    color_list = ALL_INPUT_COLORS
    return run(options.output_dir, redChannel, greenChannel, blueChannel, fname,
               color_list, options.generate_graphs, auto_only=options.auto_only,
               cross_only=options.cross_only, triple_only=options.triple_only)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Loads a single image or three\
 monocolored images.')
    parser.add_argument('-p', '--generate_graphs', action="store_true")
    parser.add_argument('-f', '--infile_rgb', type=argparse.FileType('r'))
    parser.add_argument('-r', '--infile_r', type=argparse.FileType('r'),
                        help="required infile_g and inflie_b, not yet supported")
    parser.add_argument('-g', '--infile_g', type=argparse.FileType('r'),
                        help="required infile_r and inflie_b, not yet supported")
    parser.add_argument('-b', '--infile_b', type=argparse.FileType('r'),
                        help="required infile_r and inflie_g, not yet supported")
    parser.add_argument('output_dir', help="name of output directory")
    parser.add_argument('-u', "--auto-only", action="store_true",
                        help="Create auto correlations only")
    parser.add_argument('-c', "--cross-only", action="store_true",
                        help="Create cross correlations only")
    parser.add_argument('-t', "--triple-only", action="store_true",
                        help="Create triple correlations only")
    args = parser.parse_args()
    main(args)
