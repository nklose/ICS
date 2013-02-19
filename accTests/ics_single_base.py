import unittest
import os
import shutil
import numpy as np
import ics
import image_reader


class TestICS(unittest.TestCase):
    outputDirName = ""
    inFilePath = ""

    def set_vars(self):
        raise NotImplementedError("Sub-classes must use this method to set \
self.outputDirName and self.inFilePath.")

    def setUp(self):
        self.set_vars()
        self.output = os.path.join(get_root_dir(), "mdata")
        self.expectedOutput = os.path.join(
            get_cur_dir(), os.path.join("outputs", self.outputDirName))
        self.inFile = os.path.join(
            get_cur_dir(), os.path.join("inputs", self.inFilePath))
        if (os.path.exists(self.output)):
            shutil.rmtree(self.output)

    def assertIsSimiliar(self, oldFile, newFile):
        self.assertTrue(ics_similar(oldFile, newFile))

    def test_ics_output(self):
        fnames = ['ACb', 'ACg', 'ACr', 'XCrg', 'XCrb', 'XCrg']
        fname_old = fname_new = None
        red, green, blue = self.loadImages()
        ics.run(self.output, red, green, blue, self.inFile,
                ics.ALL_INPUT_COLORS, False)
        for fname in fnames:
            fname_old = os.path.join(self.expectedOutput, '%s.txt' % (fname))
            fname_new = os.path.join(self.output, '%s.txt' % fname)
            self.assertIsSimiliar(fname_old, fname_new)

            fname_old = os.path.join(self.expectedOutput, '%sFit.txt' % (fname))
            fname_new = os.path.join(self.output, '%sFit.txt' % fname)
            self.assertIsSimiliar(fname_old, fname_new)

    def loadImages(self):
        return image_reader.get_channels_single(self.inFile)


def get_root_dir():
    return os.path.dirname(get_cur_dir())


def get_cur_dir():
    return os.path.dirname(__file__)


def ics_similar(fname_old, fname_new):
    a = np.loadtxt(fname_old)
    b = np.loadtxt(fname_new)
    return np.all(np.abs(a - b) < 0.05)
