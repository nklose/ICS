"""
Code for using matplotlib with Qt4 borrowed from:
http://matplotlib.org/examples/user_interfaces/embedding_in_qt4.html

Copryight (c) 2013 Nick Klose, Richard Leung, Cameron Mann, Glen Nelson,
Omar Qadri, and James Wang under the 401 IP License (see LICENSE file)
"""
import sys
import os.path
from numpy import arange
from PyQt4 import QtGui, QtCore
import matplotlib.pyplot as pp
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
CUR_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(CUR_DIR)
sys.path.append(ROOT_DIR)

import backend.dual as dual
import backend.backend_utils as utils

def auto_cor_gen(self, image, range_val, g0, ginf, color, deltas):
# stolen from graph.py (depreciated)
    
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(output_dir)

    name_template = "newFG%s.png"
    fname = os.path.join(directory, name % color)
    # stolen from backend_example.py
    (gnew, gs, used_deltas) = dual.core(image, None, range_val, g0, deltas)
    # need to figure out w, ginf, and the delta values
    if deltas:
        gfit = utils.gauss_2d(gs, g0, w, ginf)
    else:
        gfit = utils.gauss_2d_deltas(gs, g0, ginf, dx, dy)

    pp.clf()
    pp.plot(arange(0, range_val), gfit[0:, 0], '--',
            np.arange(1, range_val), gnew[1:, 0], 'o',
            linewidth=2.0)
    pp.axis([0, range_val, 0, max(gfit[0, 0], gnew[1, 0])])
    pp.savefig(fname)
    if color == "red":
        self.load_red_output_graph()
    elif color == "green":
        self.load_green_output_graph()
    elif color == "blue":
        self.load_blue_output_graph()
        
def load_red_output_graph(self):
    self.graph = output_dir+fname
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

