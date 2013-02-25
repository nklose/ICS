""" Contains the base class for an acceptance test using channel seperated
files.

Copryight (c) 2013 Nick Klose, Richard Leung, Cameron Mann, Glen Nelson, Omar
Qadri, and James Wang under the 401 IP License.

This Agreement, effective the 1st day of April 2013, is entered into by and
between Dr. Nils Petersen (hereinafter “client”) and the students of the
Biomembrane team (hereinafter “the development team”), in order to establish
terms and conditions concerning the completion of the Image Correlation
Spectroscopy application (hereinafter “The Application”) which is limited to the
application domain of application-domain (hereinafter “the domain of use for the
application”).  It is agreed by the client and the development team that all
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
import image_reader


class TestICSSeperate(ics_single_base.TestICS):
    inFilePathR = ""
    inFilePathG = ""
    inFilePathB = ""

    def set_vars(self):
        raise NotImplementedError("Sub-classes must use this method to set \
self.outputDirName and the file path for each color in self.inFilePathR, etc..")

    def setUp(self):
        super(TestICSSeperate, self).setUp()
        self.inFileR = os.path.join(ics_single_base.get_cur_dir(),
                                    os.path.join("inputs", self.inFilePathR))
        self.inFileG = os.path.join(ics_single_base.get_cur_dir(),
                                    os.path.join("inputs", self.inFilePathG))
        self.inFileB = os.path.join(ics_single_base.get_cur_dir(),
                                    os.path.join("inputs", self.inFilePathB))
        self.inFile = self.inFileR

    def loadImages(self):
        return image_reader.get_channels_separate(self.inFileR, self.inFileG,
                                                  self.inFileB)
