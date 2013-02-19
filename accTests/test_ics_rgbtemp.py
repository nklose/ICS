import os

import ics_single_base


class TestICSRGBtemp(ics_single_base.TestICS):

    def set_vars(self):
        self.inFilePath = os.path.join("RGBtemp", "RGBtemp.png")
        self.outputDirName = "RGBtemp"
