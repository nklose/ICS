""" Module containing classes that are the result of using the backend.
"""
import numpy as np

import graph


class BaseResult(object):
    """ Base class that contains functionality between all backend results.
    """

    def plotToStringIO(self):
        """ Plots the graph to a StringIO object and returns it.

        Return values:
            graphString: a StringIO object representing the graph.
        """
        raise NotImplementedError("All subclasses must implement plot")


class DualResult(BaseResult):
    """ Represents the result of an auto or cross run.
    """

    def __init__(self, g0, w, ginf, deltaX, deltaY, usedDeltas, resNorm,
                 outArray, fitArray, color, rangeVal):
        """ Arguments:
                g0: The amplitude of the curve.
                g0 type: float

                w: The width of the curve.
                w type: float

                ginf: The flat part of the curve.
                ginf type: float

                deltaX: The x shift of the curve
                deltaX type: float

                deltaY: The y shift of the curve
                deltaY type: float

                usedDeltas: whether the delta values were used.
                usedDeltas type: bool

                resNorm: The residual norm of the curve.
                resNorm type: float

                outArray: The calculated result
                outArray type: numpy.array

                fitArray: The calculated fit points
                fitArray type: numpy.array

                color: The color of the result. eg "rg"
                color type: string

                rangeVal: The range of the curve.
                rangeVal type: float
        """
        self.g0 = g0
        self.w = w
        self.ginf = ginf
        self.deltaX = deltaX
        self.deltaY = deltaY
        self.usedDeltas = usedDeltas
        self.resNorm = resNorm
        self.outArray = outArray
        self.fitArray = fitArray
        self.color = color
        self.rangeVal = rangeVal
        super(DualResult, self).__init__()

    def plotToStringIO(self):
        """ Plots the graph to a StringIO object and returns it.

        Return values:
            graphString: a StringIO object representing the graph.
        """
        return graph.plot(self.outArray, self.fitArray, self.color, self.ginf)


class TripleResult_part1(BaseResult):
    def __init__(self, avg_r, avg_g, avg_b, surfaceR, surfaceG, surfaceB, side):
        """ Arguments:
                avg_r: The average intensity of the red channel
                avg_r type: float

                avg_g: The average intensity of the green channel
                avg_g type: float

                avg_b: The average intensity of the blue channel
                avg_b type: float

                surfaceR: The red surface data
                surfaceR type: numpy.array

                surfaceG: The green surface data
                surfaceG type: numpy.array

                surfaceB: The blue surface data
                surfaceB type: numpy.array

                side: the length of a side of the image
                side type: int
        """
        self.avg_r = avg_r
        self.avg_g = avg_g
        self.avg_b = avg_b
        self.surfaceR = surfaceR
        self.surfaceG = surfaceG
        self.surfaceB = surfaceB
        self.side = side
        super(TripleResult_part1, self).__init__()

    def plotToStringIO(self):
        """ Plots the graph to a StringIO object and returns it.

        Return values:
            graphString: a StringIO object representing the graph.
        """
        zData = np.abs(self.surfaceR)
        rows, columns = zData.shape
        xArray = np.arange(columns)
        yArray = np.arange(rows)
        xData, yData = np.meshgrid(xArray, yArray)
        return graph.surfacePlot(xData, yData, zData, "r")


class TripleResult_part2(BaseResult):

    def __init__(self, side, lim, part_rgb):
        """ Arguments:
                side: The size of a side of the image
                side type: int

                lim: The limit of the graph to use.
                lim type: int

                part_rgb: The data at the end of the call.
                part_rgb type: np.array
        """
        self.side = side
        self.lim = lim
        self.part_rgb = part_rgb
        super(TripleResult_part2, self).__init__()

    def plotToStringIO(self):
        """ Plots the graph to a StringIO object and returns it.

        Return values:
            graphString: a StringIO object representing the graph.
        """
        zData = self.part_rgb[0, :, :]
        rows, columns = zData.shape
        xArray = np.arange(columns)
        yArray = np.arange(rows)
        xData, yData = np.meshgrid(xArray, yArray)
        return graph.surfacePlot(xData, yData, zData, "rgb")


class TripleResult_part3(DualResult):
    def plotToStringIO(self):
        """ Plots the graph to a StringIO object and returns it.

        Return values:
            graphString: a StringIO object representing the graph.
        """
        return graph.plot_1d(self.outArray, self.fitArray, self.color,
                             self.ginf)
