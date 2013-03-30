""" Module containing common graph functions for midend results
"""
from mpl_toolkits.mplot3d import Axes3D  # Required for 3d graphs
import matplotlib.pyplot as pp
from matplotlib import cm
import numpy as np
import StringIO
import math

TRIPLE_COLOR_MAP = cm.get_cmap("jet")
TRIPLE_LINE_WIDTH = 1.0


def plot(gnew, gfit, color, ginf):
    """ Plot a 2d curve.

    Arguments:
        gnew: the output array of data points
        gnew type: np.array

        gfit: the fit array of data points
        gfit type: np.array

        color: the color of the curve as a lowercase string, ie "rg".
        color type: string

        ginf: The flat value of the curve.
        ginf type: float

    Return values:
        graphString: a StringIO object representing the graph.
    """
    graphString = StringIO.StringIO()
    rangeVal = np.shape(gnew)[0]

    plotFit = gfit[0:, 0]
    plotNew = gnew[1:, 0]
    upperBound = max(gfit[0, 0], gnew[1, 0]) + 0.02
    lowerBound = ginf - 0.02

    __plot(plotFit, plotNew, color, rangeVal)

    pp.axis([0, rangeVal, min(0, lowerBound), upperBound])
    pp.savefig(graphString)
    graphString.seek(0)
    return graphString


def plot_1d(gnew, gfit, color, ginf):
    """ Plot a 1d curve.

    Arguments:
        gnew: the output array of data points
        gnew type: np.array

        gfit: the fit array of data points
        gfit type: np.array

        color: the color of the curve as a lowercase string, ie "rg".
        color type: string

        ginf: The flat value of the curve.
        ginf type: float

    Return values:
        graphString: a StringIO object representing the graph.
    """
    graphString = StringIO.StringIO()
    rangeVal = np.shape(gnew)[0]

    plotFit = gfit[0:]
    plotNew = gnew[1:]
    upperBound = max(gfit[0], gnew[1]) + 0.02
    lowerBound = ginf - 0.02

    __plot(plotFit, plotNew, color, rangeVal)

    pp.axis([0, rangeVal, lowerBound, upperBound])
    pp.savefig(graphString)
    graphString.seek(0)
    return graphString


def __plot(plotFit, plotNew, color, rangeVal):
    """ method that does the actual plotting

    Arguments:
        plotNew: the plottable array of data points
        plotNew type: np.array

        plotFit: the plottable array of fit data points
        plotFit type: np.array

        color: the color of the curve as a lowercase string, ie "rg".
        color type: string

        rangeVal: The maximum x value of the curve
        rangeVal type: float
    """
    title = __gen_title(color, 'Y')
    fit_style = __gen_style('--', color)
    new_style = __gen_style('o', color)

    pp.clf()
    pp.title(title)
    pp.plot(np.arange(0, rangeVal), plotFit, fit_style,
            np.arange(1, rangeVal), plotNew, new_style,
            linewidth=2.0)


def __gen_title(color, axis):
    """ Internal function for generating the graph title.

    Arguments:
        color: the color of the curve as a lowercase string, ie "rg".
        color type: string

        axis: The axis the title refers to.
        axis type: string

    Return value:
        The string representing the title
    """
    s = ''
    if len(color) == 1: s += 'Autocorrelation '
    if len(color) == 2: s += 'Crosscorrelation '
    if len(color) == 3: s += 'Triple-correlation '
    if 'r' in color: s += 'Red '
    if 'g' in color: s += 'Green '
    if 'b' in color: s += 'Blue '
    return s + axis


def __gen_style(style, color):
    """ Internal function for generating the graph style

    Arguments:
        style: The line or point style.
        style type: string

        color: the color of the curve as a lowercase string, ie "rg".
        color type: string

    Return value:
        The string representing the style
    """
    if len(color) == 1: return style + color[0]
    if 'r' in color and 'g' in color and 'b' in color:
        return style + "k"
    if 'r' and 'g' in color: return style + "y"
    if 'r' and 'b' in color: return style + "m"
    if 'g' and 'b' in color: return style + "c"


def surfacePlot(xData, yData, zData, color):
    """ Plot a surface curve.

    Arguments:
        xData: the data for the x axis.
        xData type: np.array

        yData: the data for the y axis.
        yData type: np.array

        zData: the data for the z axis.
        zData type: np.array

        color: the color of the curve as a lowercase string, ie "rg".
        color type: string

    Return values:
        graphString: a StringIO object representing the graph.
    """
    graphString = StringIO.StringIO()
    title = __gen_title(color, 'Y')
    pp.clf()

    fig = pp.figure()
    fig.suptitle(title)
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(xData, yData, zData, cmap=TRIPLE_COLOR_MAP,
                    linewidth=TRIPLE_LINE_WIDTH)
    fig.savefig(graphString)
    graphString.seek(0)
    return graphString
