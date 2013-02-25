import os

import ics_single_base


class TestICSSampleData(ics_single_base.TestICS):

    def set_vars(self):
        self.inFilePath = os.path.join("sampleData", "rgb-01.bmp")
        self.outputDirName = "sampleData"
