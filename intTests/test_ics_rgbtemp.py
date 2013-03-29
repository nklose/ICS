""" Contains the test for testing RGBtemp.png.

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

import os

import ics_single_base
from backend.bimloader import ImageFormatException
import backend.example as example


class TestICSRGBtempBmp(ics_single_base.TestBackendSingleImage):
    """ INT TEST ID: 1
    """

    def set_vars(self):
        self.inFilePath = os.path.join("RGBtemp", "rgb_001.bmp")
        self.outputDirName = "RGBtemp"


class TestICSRGBtempTif(ics_single_base.TestBackendSingleImage):
    """ INT TEST ID: 2
    """

    def set_vars(self):
        self.inFilePath = os.path.join("RGBtemp", "rgb_001.tif")
        self.outputDirName = "RGBtemp"

class TestICSRGBtempPng(ics_single_base.TestBackendSingleImage):
    """ INT TEST ID: 3
    """

    def set_vars(self):
        self.inFilePath = os.path.join("RGBtemp", "rgb_001.png")
        self.outputDirName = "RGBtemp"


class TestICSRGBtempGif(ics_single_base.TestBackendSingleImage):
    """ INT TEST ID: 4
    """

    def set_vars(self):
        self.inFilePath = os.path.join("RGBtemp_gif", "rgb_001.gif")
        self.outputDirName = "RGBtemp_gif"


class TestICSRGBtempJpeg(ics_single_base.TestBackendSingleImage):
    """ INT TEST ID: 5
    """

    def set_vars(self):
        self.inFilePath = os.path.join("RGBtemp", "rgb_001.jpeg")
        self.outputDirName = "RGBtemp"

    def test_ics_output(self):
        self.call_script()

    def call_script(self):
        exceptionRegex = "File " +  self.inFile + " has invalid image type"
        self.assertRaisesRegexp(ImageFormatException, exceptionRegex,
                                example.run, self.output, self.inFile,
                                example.ALL_COLORS)
