"""Graphing functions

This file contains code to generate graphs of the correlation data.  This
creates output to the "output" directory by default.
"""
import numpy as np
import matplotlib.pyplot as pp
import os
import logging
from color import COLOR

LOGGER = logging.getLogger("graph")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
NAME_TEMPLATE = "newFG%s.png"


def plot(gnew, gfit, color, directory=OUTPUT_DIR, name=NAME_TEMPLATE):
    """ Plots and saves the graph that fits the given parameters.

    Arguments:
        gnew: ???
        gnew type: ???

        gfit: ???
        gfit type: ???

        color: The colors present in the graph.
        color type: list containing COLOR enumerated values.

        directory: The directory to output the file to. By default the relative
            directory "output".
        directory type: string

        name: The name template of the file to output to. Must contain one "%s".
            By default, "newFG%s.png"
        name type: string
    """
    __check_dir_exists(directory)
    title = __gen_title(color, 'Y')
    range_val = np.shape(gnew)[0]
    fname = os.path.join(directory, name % color)
    LOGGER.debug("Generating %s in %s" % (title, fname))
    pp.clf()
    pp.title(title)
    pp.plot(np.arange(0, range_val), gfit[0:, 0], __gen_style('--', color),
            np.arange(1, range_val), gnew[1:, 0], __gen_style('o', color),
            linewidth=2.0)
    pp.axis([0, range_val, 0, max(gfit[0, 0], gnew[1, 0])])
    pp.savefig(fname)


def __gen_title(color, axis):
    """ Internal function for generating the graph title.
    """
    s = ''
    if len(color) == 1: s += 'Autocorrelation '
    if len(color) == 2: s += 'Crosscorrelation '
    if len(color) == 3: s += 'Triple-correlation '
    if COLOR.RED in color: s += 'Red '
    if COLOR.GREEN in color: s += 'Green '
    if COLOR.BLUE in color: s += 'Blue '
    return s + axis


def __gen_style(style, color):
    """ Internal function for generating the graph style.
    """
    s = style
    if len(color) == 1: return s + color[0]
    if COLOR.RED and COLOR.GREEN and COLOR.BLUE in color: return s + ""
    if COLOR.RED and COLOR.GREEN in color: return s + "y"
    if COLOR.RED and COLOR.BLUE in color: return s + "m"
    if COLOR.GREEN and COLOR.BLUE in color: return s + "c"


def __check_dir_exists(directory):
    """ Internal function that creates the output directory if required.
    """
    if not os.path.exists(directory):
        os.mkdir(directory)
