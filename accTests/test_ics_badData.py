import os

import ics_seperate_base


class TestICSBadData(ics_seperate_base.TestICSSeperate):

    def set_vars(self):
        self.inFilePathR = os.path.join("badData", "r_001.bmp")
        self.inFilePathG = os.path.join("badData", "g_001.bmp")
        self.inFilePathB = os.path.join("badData", "b_001.bmp")
        self.outputDirName = "badData"
