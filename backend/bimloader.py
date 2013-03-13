"""Loads images

This file contains functions to load images from the filesystem.
Only certain image formats are allowed, and attempting to use 
unsupported formats will raise an exception.

Copryight (c) 2013 Nick Klose, Richard Leung, Cameron Mann, Glen Nelson,
Omar Qadri, and James Wang under the 401 IP License (see LICENSE file)
"""

from __future__ import division
import numpy as np
import scipy.misc
import sys

raw_image = None

class ImageFormatException(Exception):
    """ The exception that is raised when
    the format of an image file is invalid
    """
    def __init__(self, fpath):
        msg = str.format("File {:s} has invalid image type", fpath)
        self.fpath = fpath
        super(ImageFormatException, self).__init__(msg)

def validate_format(fpath):
    """Raises an exception if 
    format of image is invalid
    """
    if fpath[-4:] == '.bmp': return
    if fpath[-4:] == '.png': return
    if fpath[-4:] == '.tif': return
    if fpath[-5:] == '.tiff': return
    raise ImageFormatException(fpath)

def load_image_mixed(fpath):
    """Loads a mixed image
    
    Arguments:
        fpath: the file path to open
        
    Return values:
        r: the red channel
        g: the green channel
        b: the blue channel
        
    Exceptions:
        ImageFormatException
    """
    validate_format(fpath)
    image = scipy.misc.imread(fpath)
    r = image[:,:,0].astype(np.float)
    g = image[:,:,1].astype(np.float)
    b = image[:,:,2].astype(np.float)
    return (r,g,b)
    
def load_image_split(fpath):
    """Loads a channel of a split image
    
    Arguments: 
        fpath: the file path to open        
    Return values: 
        channel: the loaded channel        
    Exceptions: 
        ImageFormatException
    """
    validate_format(fpath)
    image = scipy.misc.imread(fpath)
    channel = image.astype(np.float)
    return channel
    
def load_image_mixed_batch(image,fpath):
    """Loads a mixed image for batch mode
    
    Arguments:
        image: the array in which to store the loaded image
        fpath: the file path to open        
    There are no return values.
    Exceptions:
        ImageFormatException        
    """
    validate_format(fpath)
    raw_image = scipy.misc.imread(fpath)
    image[0,:,:] = raw_image[:,:,0].astype(np.float)
    image[1,:,:] = raw_image[:,:,1].astype(np.float)
    image[2,:,:] = raw_image[:,:,2].astype(np.float)
    return

def load_image_split_batch(image,fpath):
    """Loads one channel of a split image for batch mode
    
    Arguments:
        image: the array in which to store the loaded channel
        fpath: the file path to open
    There are no return values.
    Exceptions:
        ImageFormatException
    """
    validate_format(fpath)
    raw_image = scipy.misc.imread(fpath)
    image[:,:] = raw_image.astype(np.float)

