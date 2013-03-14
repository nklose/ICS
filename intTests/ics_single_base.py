""" Contains the base class for an integration test using a single image.

Copryight (c) 2013 Nick Klose, Richard Leung, Cameron Mann, Glen Nelson, Omar
Qadri, and James Wang under the 401 IP License.

This Agreement, effective the 1st day of April 2013, is entered into by and
between Dr. Nils Petersen (hereinafter "client") and the students of the
Biomembrane team (hereinafter "the development team"), in order to establish
terms and conditions concerning the completion of the Image Correlation
Spectroscopy application (hereinafter "The Application") which is limited to the
application domain of application-domain (hereinafter "the domain of use for the
application").  It is agreed by the client and the development team that all
domain specific knowledge and compiled research is the intellectual property of
the client, regarded as a copyrighted collection. The framework and code base
created by the development team is their own intellectual property, and may only
be used for the purposes outlined in the documentation of the application, which
has been provided to the client. The development team agrees not to use their
framework for, or take part in the development of, anything that falls within
the domain of use for the application, for a period of 6 (six) months after the
signing of this agreement.
"""

import unittest
import os
import shutil
import numpy as np
import backend.example as example


class TestBackendSingleImage(unittest.TestCase):
    outputDirName = ""
    inFilePath = ""
    d_range = 20
    t_range = 15

    def set_vars(self):
        raise NotImplementedError("Sub-classes must use this method to set \
self.outputDirName and self.inFilePath.")

    def setUp(self):
        self.set_vars()
        self.output = os.path.join(get_root_dir(), "pdata")
        self.expectedOutput = os.path.join(
            get_acceptance_path(), os.path.join("outputs", self.outputDirName))
        self.inFile = os.path.join(
            get_acceptance_path(), os.path.join("inputs", self.inFilePath))
        if (os.path.exists(self.output)):
            shutil.rmtree(self.output)

    def assertIsSimiliar(self, oldFile, newFile):
        self.assertTrue(ics_similar(oldFile, newFile))

    def test_ics_output(self):
        self.call_script()
        self.validate_output()

    def call_script(self):
        example.run(self.output, self.inFile, example.ALL_COLORS,
                    d_range=self.d_range, t_range=self.t_range)

    def validate_output(self):
        fnames = ['ACb', 'ACg', 'ACr', 'XCrg', 'XCrb', 'XCrg']
        fname_old = fname_new = None
        for fname in fnames:
            fname_old = os.path.join(self.expectedOutput, '%s.txt' % (fname))
            fname_new = os.path.join(self.output, '%s.txt' % fname)
            self.assertIsSimiliar(fname_old, fname_new)

            fname_old = os.path.join(self.expectedOutput, '%sFit.txt' % (fname))
            fname_new = os.path.join(self.output, '%sFit.txt' % fname)
            self.assertIsSimiliar(fname_old, fname_new)

    def tearDown(self):
        if (os.path.exists(self.output)):
            shutil.rmtree(self.output)


def get_root_dir():
    return os.path.dirname(os.path.abspath(get_cur_dir()))


def get_cur_dir():
    return os.path.dirname(__file__)


def get_acceptance_path():
    """ inputs are stored with the acceptance tests, so grab input from there.
    """
    return os.path.join(get_root_dir(), "accTests")


def ics_similar(fname_old, fname_new):
    a = np.loadtxt(fname_old)
    b = np.loadtxt(fname_new)
    return np.all(np.abs(a - b) < 0.05)
