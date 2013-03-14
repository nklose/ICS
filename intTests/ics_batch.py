""" Contains the base class for an integration test batch mode.

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
import shutil

import ics_single_base
import backend.batch as batch


class TestBatch(ics_single_base.TestBackendSingleImage):
    config = None

    def set_vars(self):
        raise NotImplementedError("Sub-classes must use this method to set \
self.config and self.outputDirName.")

    def setUp(self):
        self.set_vars()
        self.output = self.config.output_directory
        self.expectedOutput = os.path.join(
            ics_single_base.get_acceptance_path(),
            os.path.join("outputs", self.outputDirName))
        if (os.path.exists(self.output)):
            shutil.rmtree(self.output)

    def call_script(self):
        batch.run(batch.Info(), self.config)
