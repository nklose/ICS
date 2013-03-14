"""Sample configurations

This file contains three sample batch configurations.

Copryight (c) 2013 Nick Klose, Richard Leung, Cameron Mann, Glen Nelson,
Omar Qadri, and James Wang under the 401 IP License (see LICENSE file)
"""

from __future__ import division
import numpy as np

class MixedConfig:
    side = 128
    input_directory = '../accTests/inputs/RGBtemp/'
    output_directory = 'output/'
    name_min = 1
    name_max = 1
    name_format = 'rgb_{:03d}.bmp'
    dual_range = 20
    triple_range = 15
    auto_consider_deltas = False
    cross_consider_deltas = False
    dual_initial = np.array([1,10,0,0,0],dtype=np.float)
    triple_initial = np.array([50,2,0],dtype=np.float)
    triple_lim = 32
    input_type = 'mixed'
    output_type = 'full'
    output_numbering = 'none'

class SplitConfig:
    side = 128
    input_directory = '../accTests/inputs/RGBtemp/'
    output_directory = 'output/'
    name_min = 1
    name_max = 1
    name_format = '{:s}_{:03d}.bmp'
    dual_range = 20
    triple_range = 15
    auto_consider_deltas = False
    cross_consider_deltas = False
    dual_initial = np.array([1,10,0,0,0],dtype=np.float)
    triple_initial = np.array([50,2,0],dtype=np.float)
    triple_lim = 32
    input_type = 'split'
    output_type = 'summary'
    output_numbering = 'none'

class BadConfig:
    side = 512
    input_directory = '../accTests/inputs/badData/'
    output_directory = 'output/'
    name_min = 1
    name_max = 10
    name_format = '{:s}_{:03d}.bmp'
    dual_range = 20
    triple_range = 15
    auto_consider_deltas = False
    cross_consider_deltas = False
    dual_initial = np.array([1,10,0,0,0],dtype=np.float)
    triple_initial = np.array([50,2,0],dtype=np.float)
    triple_lim = 64
    input_type = 'split'
    output_type = 'full'
    output_numbering = '{:03d}'
