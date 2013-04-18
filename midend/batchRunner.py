""" Contains class to make working with the batch mode easier.
"""
import StringIO
import numpy as np
import copy

import sys
import os.path
import logging

LOGGER = logging.getLogger("me.batch")

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)

import backend.batch as batch


def _default_interrupt_function(numberOfFilesFinished, numberOfFilesTotal):
    """ This function is the default interrupt function. It does nothing.

        Arguments:
            numberOfFilesFinished: The number of files currently finished.
            numberOfFilesFinished type: int

            numberOfFilesTotal: The number of files there are total.
            numberOfFilesTotal type: int

        Return Value:
            Interrupt functions return values are unused.
    """
    LOGGER.debug("%s / %s" % (numberOfFilesFinished, numberOfFilesTotal))
    return numberOfFilesFinished, numberOfFilesTotal


class BatchRunner(object):
    """ Midend object that acts as a go between for the front ends and batch
        mode.
    """

    def __init__(self, config):
        """ Arguments:
                config: The config file to use.  See batch.config for the
                        properties these objects should have.
                config type: object
        """
        self.config = config
        self.info = batch.Info()
        self.isDoneRunning = False
        self.hasSetUp = False
        self.__infoStorage = []
        super(BatchRunner, self).__init__()

    def reset(self):
        """ Resets the batch runner. This may be useful for running the same
            batch configuration multiple times.
        """
        self.isDoneRunning = False
        self.hasSetUp = False
        self.info = batch.Info()

    def run(self):
        """ Run through one batch call, and then return control to the caller.

            Return Value:
               The number of images left to process. If no images are left, zero
               is returned.
        """
        if self.isDoneRunning:
            return 0
        if not self.hasSetUp:
            self._setup()
        LOGGER.debug("Batch run (single) started")

        self._single_run()
        filesFinished = self.info.cur_files
        filesTotal = self.info.num_files
        if filesTotal <= filesFinished:
            self.isDoneRunning = True
        LOGGER.debug("Batch run (single) done")
        return filesTotal - filesFinished

    def _setup(self):
        """ Helper function to do necessary setup for the batch.
        """
        batch.setup(self.info, self.config)
        self.hasSetUp = True

    def _single_run(self):
        """ Does a single batch run.
        """
        batch.run_0(self.info, self.config)
        batch.run_1(self.info, self.config)
        batch.run_2(self.info, self.config)
        batch.run_3(self.info, self.config)
        # Skip run_4, it is file output
        self.__infoStorage.append(FlyWeightBatchInfo(self.info))
        self.info.cur_files += 1

    def runAll(self, interruptFunction=_default_interrupt_function):
        """ Run through all batch calls, calling a callback function between
            each run.

            Arguments:
                interruptFunction: The function to call back.
                interruptFunction type: function
        """
        if self.isDoneRunning:
            return
        self._setup()

        filesFinished = self.info.cur_files
        filesTotal = self.info.num_files
        while filesTotal > filesFinished:
            LOGGER.debug("Batch run (all) started")
            self._single_run()
            filesFinished = self.info.cur_files
            interruptFunction(filesFinished, filesTotal)
            LOGGER.debug("Batch run (all) looping")
        LOGGER.debug("Batch run (all) done")
        self.isDoneRunning = True

    def getResults(self):
        """ Get the batch.Info object describing the results of the run.

            Return Value:
                batch.Info object describing the run results.
        """
        return self.info

    def outputAllFiles(self):
        """ Outputs all necessary files to the filepath defined in the config
            object.
        """
        for item in self.__infoStorage:
            batch.run_4(item, self.config)
        _customFinish(self.info, self.config)

    def outputToStringIo(self):
        """ Outputs all necessary files to stringIo objects.

            Return Value:
               Dictionary of fileName to stringIo object.
        """
        fileDict = {}
        resultsText = StringIO.StringIO()
        if _customFinish(self.info, self.config, resultsText):
            fileDict["results.txt"] = resultsText
        for item in self.__infoStorage:
            newDict = _customRun4(item, self.config)
            if newDict is not None:
                fileDict.update(newDict)
        return fileDict


def _customRun4(info, config):
    """ Method that replicates batch.run_4 for the creation of StringIO objects.

        Arguments:
            info: the batch.Info object.
            info type: batch.Info

            config: the batch.Config object
            config type: batch.Config

        Return Value:
            Returns None if no file was output, or a dictionary containing
            all filenames as keys, and StringIO objects as values.
    """
    if config.output_type == 'none': return None
    if config.output_type == 'summary': return None
    fileDict = {}
    # save out and fit as files
    fprefix = ''
    fnum = info.cur_files
    if config.output_numbering != 'none':
        fidx = str.format(config.output_numbering, config.name_min + fnum)
        fprefix = fidx + '_'
    for i in range(6):
        if i < 3: fcode = 'AC'
        if i >= 3: fcode = 'XC'
        fileName1 = fprefix + fcode + batch.ALL_COLORS[i] + '.txt'
        file1 = StringIO.StringIO()
        fileName2 = fprefix + fcode + batch.ALL_COLORS[i] + 'Fit.txt'
        file2 = StringIO.StringIO()
        np.savetxt(file1, info.dual_out[i, :, :], fmt='%9.5f')
        np.savetxt(file2, info.dual_fit[i, :, :], fmt='%9.5f')
        file1.seek(0)
        file2.seek(0)
        fileDict[fileName1] = file1
        fileDict[fileName2] = file2
    fileName1 = fprefix + 'TripleCrgb.txt'
    file1 = StringIO.StringIO()
    fileName2 = fprefix + 'TripleCrgbFit.txt'
    file2 = StringIO.StringIO()
    np.savetxt(file1, info.triple_out, fmt='%9.5f')
    np.savetxt(file2, info.triple_fit, fmt='%9.5f')
    file1.seek(0)
    file2.seek(0)
    fileDict[fileName1] = file1
    fileDict[fileName2] = file2
    return fileDict


def _customFinish(info, config, fileObject=None):
    """ Method that changes finish to use a passed in fileObject,
        and return the file name. If no fileObject is provided, it acts instead
        as batch.finish

        Arguments:
            info: the batch.Info object.
            info type: batch.Info

            config: the batch.Config object
            config type: batch.Config

            fileObject: the File-like object to output to
            fileObject type: File

        Return Value:
            Returns None if no file was output, or True otherwise.
    """
    if fileObject is None:
        retVal = batch.finish(info, config)
        info.lib = None
        return retVal

    info.lib.destroy()
    info.lib = None
    if config.output_type == 'none': return

    # generate table header
    colors = '--r:--g:--b:-rg:-rb:-gb:rgb'.split(':')
    parameters = 'g(0):---w:ginf:--dx:--dy:used:norm'.split(':')
    temp_header_1 = [''] * 49
    for i, color in enumerate(colors):
        for j, param in enumerate(parameters):
            temp_header_1[i * 7 + j] = str.format('|{}-{}-', color, param)
    scolors = '--r:--g:--b'.split(':')
    temp_header_2 = [str.format('|{}--avg-', color) for color in scolors]
    header = ' ' * 9 + ''.join(temp_header_2) + ''.join(temp_header_1)

    fileObject.write(header + '\n')
    np.savetxt(fileObject, info.results, fmt='%9.5f', delimiter='|')
    return True


class FlyWeightBatchInfo(object):

    def __init__(self, info):
        self.cur_files = info.cur_files
        self.dual_out = info.dual_out
        self.dual_fit = info.dual_fit
        self.triple_out = info.triple_out
        self.triple_fit = info.triple_fit
