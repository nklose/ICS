""" Module containing classes that are the result of using the backend.
"""
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as pp
import numpy as np
import StringIO
from matplotlib import cm

class BaseResult(object):

    def plotToStringIO(self):
        """ Plots the graph to a StringIO object and returns it.
        """
        raise NotImplementedError("All subclasses must implement plot")


class DualResult(BaseResult):
    def __init__(self, g0, w, ginf, deltaX, deltaY, usedDeltas, resNorm,
                 outArray, fitArray, colors, rangeVal, gFit):
        self.g0 = g0
        self.w = w
        self.ginf = ginf
        self.deltaX = deltaX
        self.deltaY = deltaY
        self.usedDeltas = usedDeltas
        self.resNorm = resNorm
        self.outArray = outArray
        self.fitArray = fitArray
        self.colors = colors
        self.rangeVal = rangeVal
        self.gFit = gFit
        super(DualResult, self).__init__()

    def plotToStringIO(self):
        return plot(self.outArray, self.gFit, self.colors)


class TripleResult_part1(BaseResult):
    def __init__(self, avg_r, avg_g, avg_b, sr, sg, sb, side):
        self.avg_r = avg_r
        self.avg_g = avg_g
        self.avg_b = avg_b
        self.sr = sr
        self.sg = sg
        self.sb = sb
        self.side = side
        super(TripleResult_part1, self).__init__()

    def plotToStringIO(self):
        Z = np.abs(self.sr)
        m, n = Z.shape
        x = np.arange(n)
        y = np.arange(m)
        X, Y = np.meshgrid(x, y)
        return surfacePlot(X, Y, Z, "r")


class TripleResult_part2(BaseResult):

    def __init__(self, side, lim, part_rgb):
        self.side = side
        self.lim = lim
        self.part_rgb = part_rgb
        super(TripleResult_part2, self).__init__()

    def plotToStringIO(self):
        Z = self.part_rgb[0, :, :]
        m, n = Z.shape
        x = np.arange(n)
        y = np.arange(m)
        X, Y = np.meshgrid(x, y)
        return surfacePlot(X, Y, Z, "rgb")


class TripleResult_part3(DualResult):
    def plotToStringIO(self):
        return plot_1d(self.outArray, self.gFit, self.colors)


def plot(gnew, gfit, color):
    graph_string = StringIO.StringIO()
    range_val = np.shape(gnew)[0]

    plot_fit = gfit[0:, 0]
    plot_new = gnew[1:, 0]

    __plot(plot_fit, plot_new, color, range_val)

    pp.axis([0, range_val, 0, max(gfit[0, 0], gnew[1, 0])])
    pp.savefig(graph_string)
    graph_string.seek(0)
    return graph_string


def plot_1d(gnew, gfit, color):
    graph_string = StringIO.StringIO()
    range_val = np.shape(gnew)[0]

    plot_fit = gfit[0:]
    plot_new = gnew[1:]
    __plot(plot_fit, plot_new, color, range_val)

    pp.axis([0, range_val, 0, max(gfit[0], gnew[1])])
    pp.savefig(graph_string)
    graph_string.seek(0)
    return graph_string


def __plot(plot_fit, plot_new, color, range_val):
    title = __gen_title(color, 'Y')
    fit_style = __gen_style('--', color)
    new_style = __gen_style('o', color)

    pp.clf()
    pp.title(title)
    pp.plot(np.arange(0, range_val), plot_fit, fit_style,
            np.arange(1, range_val), plot_new, new_style,
            linewidth=2.0)


def __gen_title(color, axis):
    """ Internal function for generating the graph title.
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
    """ Internal function for generating the graph style.
    """
    if len(color) == 1: return style + color[0]
    if 'r' and 'g' and 'b' in color:
        return style + "k"
    if 'r' and 'g' in color: return style + "y"
    if 'r' and 'b' in color: return style + "m"
    if 'g' and 'b' in color: return style + "c"


def surfacePlot(xData, yData, zData, color):
    graph_string = StringIO.StringIO()
    title = __gen_title(color, 'Y')
    pp.clf()
    pp.title(title)

    fig = pp.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(xData, yData, zData, cmap=cm.get_cmap("jet"),
                    linewidth=0)
    pp.savefig(graph_string)
    graph_string.seek(0)
    return graph_string
