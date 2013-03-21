""" Module containing classes that are the result of using the backend.
"""
import matplotlib.pyplot as pp
import numpy as np
import StringIO


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
        graphFile = StringIO.StringIO()
        beforeSurfc = np.abs(self.sr)
        # do surfc with beforeSurfc
        graphFile.seek(0)
        return graphFile


class TripleResult_part2(BaseResult):

    def __init__(self, side, lim, part_rgb):
        self.side = side
        self.lim = lim
        self.part_rgb = part_rgb
        super(TripleResult_part2, self).__init__()

    def plotToStringIO(self):
        graphFile = StringIO.StringIO()
        beforeSurfc = self.part_rgb[0, :, :]
        # do surfc
        graphFile.seek(0)
        return graphFile


class TripleResult_part3(DualResult):
    def plotToStringIO(self):
        return plot(self.outArray, self.gFit, self.colors)


def plot(gnew, gfit, color):
    graph_string = StringIO.StringIO()
    title = __gen_title(color, 'Y')
    range_val = np.shape(gnew)[0]

    plot_fit = gfit[0:, 0]
    plot_new = gnew[1:, 0]
    fit_style = __gen_style('--', color)
    new_style = __gen_style('o', color)

    pp.clf()
    pp.title(title)
    pp.plot(np.arange(0, range_val), plot_fit, fit_style,
            np.arange(1, range_val), plot_new, new_style,
            linewidth=2.0)
    pp.axis([0, range_val, 0, max(gfit[0, 0], gnew[1, 0])])
    pp.savefig(graph_string)
    graph_string.seek(0)
    return graph_string


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
    if 'r' and 'g' and 'b' in color: return style + ""
    if 'r' and 'g' in color: return style + "y"
    if 'r' and 'b' in color: return style + "m"
    if 'g' and 'b' in color: return style + "c"
