"""
Copryight (c) 2013 Nick Klose, Richard Leung, Cameron Mann, Glen Nelson,
Omar Qadri, and James Wang under the 401 IP License (see LICENSE file)
"""
import sys
import os.path
from numpy import arange
from PyQt4 import QtGui, QtCore
import matplotlib.pyplot as graph

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(CUR_DIR)
sys.path.append(ROOT_DIR)
TEMP_DIR = "./ics_tmp"

import backend.backend_utils as utils
import backend.bimloader as bimloader

# Intended to analyze the image using dual.core and the variables passed in.
# Then plot the values and axis, saving it to a temporary file.
# Then load this graph in the temp folder into the specific ui box.
def auto_plot(self, image, range_val, g0, w, ginf, deltas):   
    
    
    
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
