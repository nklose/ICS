"""
Copryight (c) 2013 Nick Klose, Richard Leung, Cameron Mann, Glen Nelson,
Omar Qadri, and James Wang under the 401 IP License (see LICENSE file)
"""
import sys
import os.path
from numpy import arange
from PyQt4 import QtGui, QtCore
import matplotlib.pyplot as pp

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(CUR_DIR)
sys.path.append(ROOT_DIR)
TEMP_DIR = "./ics_tmp"

import backend.dual as dual
import backend.backend_utils as utils
import backend.bimloader as bimloader

# Intended to analyze the image using dual.core and the variables passed in.
# Then plot the values and axis, saving it to a temporary file.
# Then load this graph in the temp folder into the specific ui box.
def auto_cor_gen(self, image, range_val, g0, w, ginf, color, deltas):   
    if not os.path.exists(TEMP_DIR):
        os.mkdir(TEMP_DIR)

    name_template = "newFG%s.png"
    # I hope this is a proper filepath (probably not, TEMP_DIR is wrong)
    fname = os.path.join(TEMP_DIR, name_template % color)
    # stolen from backend_example.py
    (gnew, gs, used_deltas) = dual.core(image, None, range_val, g0, deltas)
    # need to figure the delta values
    if deltas:
        gfit = utils.gauss_2d(gs, g0, w, ginf)
    else:
        gfit = utils.gauss_2d_deltas(gs, g0, ginf, dx, dy)

    pp.clf()
    pp.plot(arange(0, range_val), gfit[0:, 0], '--',
            np.arange(1, range_val), gnew[1:, 0], 'o',
            linewidth=2.0)
    pp.axis([0, range_val, 0, max(gfit[0, 0], gnew[1, 0])])
    # requires a working filepath for me to even test this
    pp.savefig(fname)
    if color == "red":
        self.load_red_output_graph()
    elif color == "green":
        self.load_green_output_graph()
    elif color == "blue":
        self.load_blue_output_graph()
        
def load_red_output_graph(self):
    self.graph = fname
    self.ui.graphFile.setText(basename(self.graph))
    self.ui.imageAutoRed.setPixmap(QtGui.QPixmap(self.graph))

def load_green_output_graph(self):
    self.graph = output_dir+fname
    self.ui.graphFile.setText(basename(self.graph))
    self.ui.imageAutoGreen.setPixmap(QtGui.QPixmap(self.graph))

def load_blue_output_graph(self):
    self.graph = output_dir+fname
    self.ui.graphFile.setText(basename(self.graph))
    self.ui.imageAutoBlue.setPixMap(QtGui.QPixmap(self.graph))

## cross_cor_gen will virtually be a copy paste of auto, once auto is working
