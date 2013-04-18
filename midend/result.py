""" Module containing classes that are the result of using the backend.
"""
import numpy as np
import os

import graph


class NoSaveDataException(Exception):
    """ Exception for when there is nothing to be saved by a result. """
    pass


class BaseResult(object):
    """ Base class that contains functionality between all backend results.
    """

    def plotToStringIO(self):
        """ Plots the graph to a StringIO object and returns it.

        Return values:
            graphString: a StringIO object representing the graph.
        """
        raise NotImplementedError("All subclasses must implement "
                                  "plotToStringIo")

    def saveData(self, filepath, dataName=None, fitName=None):
        """ Saves the data described by the result object to file

        Arguments:
            filepath: the directory to save the data to.
            filepath type: string

            dataName: the name to save the data to, default depends on class.
            dataName type: string

            fitName: the name to save the fit to, default depends on class.
            fitName type: string

        Raises:
            NoSaveDataException: If the result type does not have any data to
                                 save.
        """
        raise NotImplementedError("All subclasses must implement "
                                  "saveData")

    def saveDataFileLike(self, dataFileLike, fitFileLike):
        """ Saves the data described by the result object to file

        Arguments:
            dataFileLike: the directory to save the data to.
            dataFileLike type: string

            fitFileLike: the directory to save the fit data to.
            fitFileLike type: string

        Raises:
            NoSaveDataException: If the result type does not have any data to
                                 save.
        """
        raise NotImplementedError("All subclasses must implement "
                                  "saveDataFileLike")


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
        
    def __str__(self):
        return "".join([self.__class__.__name__, " <g0: ", str(self.g0), "; w: ", str(self.w),
                        "; ginf: ", str(self.ginf), "; resNorm: ", str(self.resNorm),
                        "; Colors: ", str(self.color)])

    def plotToStringIO(self):
        """ Plots the graph to a StringIO object and returns it.

        Return values:
            graphString: a StringIO object representing the graph.
        """
        return graph.plot(self.outArray, self.fitArray, self.color, self.ginf)

    def saveData(self, filepath, dataName=None, fitName=None):
        """ Saves the data described by the result object to file

        Arguments:
            filepath: the directory to save the data to.
            filepath type: string

            dataName: the name to save the data to, default is based on color.
            dataName type: string

            fitName: the name to save the fit to, default is based on color.
            fitName type: string

        Raises:
            NoSaveDataException: If the result type does not have any data to
                                 save.
        """
        if len(self.color) == 1: code = 'AC'
        if len(self.color) == 2: code = 'XC'
        if dataName is None:
            dataName = code + self.color + '.txt'
        if fitName is None:
            fitName = code + self.color + 'Fit.txt'
        dataPath = os.path.join(filepath, dataName)
        fitPath = os.path.join(filepath, fitName)
        self.saveDataFileLike(dataPath, fitPath)

    def saveDataFileLike(self, dataFileLike, fitFileLike):
        """ Saves the data described by the result object to file

        Arguments:
            dataFileLike: the directory to save the data to.
            dataFileLike type: string

            fitFileLike: the directory to save the fit data to.
            fitFileLike type: string

        Raises:
            NoSaveDataException: If the result type does not have any data to
                                 save.
        """
        np.savetxt(dataFileLike, self.outArray, fmt='%9.5f')
        np.savetxt(fitFileLike, self.fitArray, fmt='%9.5f')


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

    def saveData(self, filepath, dataName=None, fitName=None):
        """ Saves the data described by the result object to file

        Arguments:
            filepath: the directory to save the data to.
            filepath type: string

            dataName: the name to save the data to.
            dataName type: string

            fitName: the name to save the fit to.
            fitName type: string

        Raises:
            NoSaveDataException: If the result type does not have any data to
                                 save.
        """
        raise NoSaveDataException("The triple correlation must be finished "
                                  "before it can be saved")

    def saveDataFileLike(self, dataFileLike, fitFileLike):
        """ Saves the data described by the result object to file

        Arguments:
            dataFileLike: the directory to save the data to.
            dataFileLike type: string

            fitFileLike: the directory to save the fit data to.
            fitFileLike type: string

        Raises:
            NoSaveDataException: If the result type does not have any data to
                                 save.
        """
        raise NoSaveDataException("The triple correlation must be finished "
                                  "before it can be saved")


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

    def saveData(self, filepath, dataName=None, fitName=None):
        """ Saves the data described by the result object to file

        Arguments:
            filepath: the directory to save the data to.
            filepath type: string

            dataName: the name to save the data to.
            dataName type: string

            fitName: the name to save the fit to.
            fitName type: string

        Raises:
            NoSaveDataException: If the result type does not have any data to
                                 save.
        """
        raise NoSaveDataException("The triple correlation must be finished "
                                  "before it can be saved")

    def saveDataFileLike(self, dataFileLike, fitFileLike):
        """ Saves the data described by the result object to file

        Arguments:
            dataFileLike: the directory to save the data to.
            dataFileLike type: string

            fitFileLike: the directory to save the fit data to.
            fitFileLike type: string

        Raises:
            NoSaveDataException: If the result type does not have any data to
                                 save.
        """
        raise NoSaveDataException("The triple correlation must be finished "
                                  "before it can be saved")


class TripleResult_part3(DualResult):
    def plotToStringIO(self):
        """ Plots the graph to a StringIO object and returns it.

        Return values:
            graphString: a StringIO object representing the graph.
        """
        return graph.plot_1d(self.outArray, self.fitArray, self.color,
                             self.ginf)

    def saveData(self, filepath, dataName=None, fitName=None):
        """ Saves the data described by the result object to file

        Arguments:
            filepath: the directory to save the data to.
            filepath type: string

            dataName: the name to save the data to, default is TripleCrgb.txt.
            dataName type: string

            fitName: the name to save the fit to, default is TripleCrgbFit.txt.
            fitName type: string

        Raises:
            NoSaveDataException: If the result type does not have any data to
                                 save.
        """
        if dataName is None:
            dataName = "TripleCrgb.txt"
        if fitName is None:
            fitName = "TripleCrgbFit.txt"
        dataPath = os.path.join(filepath, dataName)
        fitPath = os.path.join(filepath, fitName)
        self.saveDataFileLike(dataPath, fitPath)

    def saveDataFileLike(self, dataFileLike, fitFileLike):
        """ Saves the data described by the result object to file

        Arguments:
            dataFileLike: the directory to save the data to.
            dataFileLike type: string

            fitFileLike: the directory to save the fit data to.
            fitFileLike type: string

        Raises:
            NoSaveDataException: If the result type does not have any data to
                                 save.
        """
        np.savetxt(dataFileLike, self.outArray, fmt='%9.5f', delimiter='\n')
        np.savetxt(fitFileLike, self.fitArray, fmt='%9.5f', delimiter='\n')


def saveResultsFile(filepath, resultList, filename="results.txt"):
    """ Saves the result file summarizing all entries in resultList.

        Arguments:
            filepath: the filepath to save results.txt to.
            filepath type: string

            resultList: the list of DualResult and TripleResult_part3 objects.
            resultList type: list

            filename: the name of the file to save data in. Defaults to
                      results.txt
            filename type: string

        Raises:
            ValueError: if an entry in resultList is invalid.
    """
    results = np.empty((len(resultList), 7))
    np.ndarray.fill(results, np.nan)
    header = str.format('{:>9s} {:>9s} {:>9s} {:>9s} {:>9s} {:>9s} {:>9s}',
                        'g(0)', 'w', 'ginf', 'dx', 'dy', 'used', 'norm')
    for index, result in enumerate(resultList):
        if not isinstance(result, DualResult):
            # Triple is subclassed by dual.
            raise ValueError("Invalid result type for final results: %s" %
                             type(result))
        results[index, 0] = result.g0
        results[index, 1] = result.w
        results[index, 2] = result.ginf
        results[index, 3] = result.deltaX
        results[index, 4] = result.deltaY
        results[index, 5] = result.usedDeltas
        results[index, 6] = result.resNorm
    finalPath = os.path.join(filepath, filename)
    with open(finalPath, "w") as resultsFile:
        resultsFile.write(header + '\n')
        np.savetxt(resultsFile, results, fmt='%9.5f')
