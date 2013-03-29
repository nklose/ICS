""" Tests one item of the "badData" data set. TODO, add correct output data.x

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
import numpy as np

import ics_batch
import ics_single_base
import ics_seperate_base

IN_PATH_ACC = ics_single_base.get_acceptance_path()
IN_PATH_IN = os.path.join(IN_PATH_ACC, "inputs")


class BadConfig:
    side = 512
    input_directory = os.path.join(IN_PATH_IN, "badData")
    output_directory = os.path.join(ics_single_base.get_cur_dir(), 'output')
    name_min = 1
    name_max = 10
    name_format = '{:s}_{:03d}.bmp'
    dual_range = 20
    triple_range = 15
    auto_consider_deltas = False
    cross_consider_deltas = False
    dual_initial = np.array([1, 10, 0, 0, 0], dtype=np.float)
    triple_initial = np.array([50, 2, 0], dtype=np.float)
    triple_lim = 64
    input_type = 'split'
    output_type = 'full'
    output_numbering = '{:03d}'


class TestICSBadData(ics_batch.TestBatch):
    """ INT TEST ID: 6
    """

    def set_vars(self):
        self.config = BadConfig()
        self.outputDirName = "badData"

    def validate_output(self):
        fnames = ['ACb', 'ACg', 'ACr', 'XCrg', 'XCrb', 'XCrg', 'TripleCrgb']
        fname_old = fname_new = None
        errorMsg = "Expected %s different then %s"
        for i in range(self.config.name_min, self.config.name_max + 1):
            for fname in fnames:
                fname_old = os.path.join(self.expectedOutput,
                                         '%03d_%s.txt' % (i, fname))
                fname_new = os.path.join(self.config.output_directory,
                                         '%03d_%s.txt' % (i, fname))
                self.assertIsSimiliar(fname_old, fname_new,
                                      msg=errorMsg % (fname_old, fname_new))

                fname_old = os.path.join(self.expectedOutput,
                                         '%03d_%sFit.txt' % (i, fname))
                fname_new = os.path.join(self.config.output_directory,
                                         '%03d_%sFit.txt' % (i, fname))
                self.assertIsSimiliar(fname_old, fname_new,
                                      msg=errorMsg % (fname_old, fname_new))


class TestICSBadDataSingle(ics_seperate_base.TestBackendSeperateImage):
    def set_vars(self):
        self.d_range = 20
        self.inFilePathR = os.path.join("badData", "r_000.bmp")
        self.inFilePathG = os.path.join("badData", "g_000.bmp")
        self.inFilePathB = os.path.join("badData", "b_000.bmp")
        self.outputDirName = "badData"

    def validate_output(self):
        fnames = ['ACb', 'ACg', 'ACr', 'XCrg', 'XCrb', 'XCrg']
        errorMsg = "Expected %s different then %s"
        fname_old = fname_new = None
        for fname in fnames:
            fname_old = os.path.join(self.expectedOutput,
                                     '001_%s.txt' % (fname))
            fname_new = os.path.join(self.output, '%s.txt' % fname)
            self.assertIsSimiliar(fname_old, fname_new,
                                  msg=errorMsg % (fname_old, fname_new))

            fname_old = os.path.join(self.expectedOutput,
                                     '001_%sFit.txt' % (fname))
            fname_new = os.path.join(self.output, '%sFit.txt' % fname)
            self.assertIsSimiliar(fname_old, fname_new,
                                  msg=errorMsg % (fname_old, fname_new))
