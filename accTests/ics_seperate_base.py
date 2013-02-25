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
