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

class NumPathsException(Exception):
    """ The exception that is raised when an attempt is
    made to load images from an incorrect number of paths
    """
    def __init__(self, npaths):
        msg = "Must pass one or three paths to load"
        msg += str.format(", not {:d} paths", npaths)
        self.npaths = npaths
        super(NumPathsException, self).__init__(msg)

def load_image(fpaths):
    """Loads an image
    
    Arguments:
        fpaths: a list of file paths to open. For mixed images,
            this should contain a single element; for split ones,
            this should contain three elements
    
    Return values:
        max_pixel: [f64] the maximum possible pixel value
        channels: a 3-element list of the red, green and blue
            channels of the image, in that order. Each element
            of this list is a numpy array of 64-bit floats
            
    Exceptions: Same as check_paths() function
    """
    check_paths(fpaths)
    channels = [None,None,None]
    if len(fpaths) == 1:
        image = scipy.misc.imread(fpaths[0])
        for i in range(3):
            channels[i] = image[:,:,i].astype(np.float)
    elif len(fpaths) == 3:
        for i in range(3):
            image = scipy.misc.imread(fpaths[i])
            channels[i] = image.astype(np.float)
    return (2**(8*image.itemsize), channels)

def check_paths(fpaths):
    """Checks whether file paths are valid
    
    Arguments:
        fpaths: a list of file paths to check
    
    There are no return values.
    
    Exceptions:
        NumPathsException: this exception is raised when an
            incorrect number of paths is passed to the function
        ImageFormatException: this exception is raised when the
            image referred to by a file path has an unsupported 
            format (ie. rejected by the valid_format() function)
    """        
    npaths = len(fpaths)
    if npaths != 1 and npaths != 3:
        raise NumPathsException(npaths)
    for path in fpaths:
        if not valid_format(path):
            raise ImageFormatException(path)

def valid_format(fpath):
    """Checks whether the format of the image 
    referred to by a given path is valid.
    
    Arguments:
        fpath: a file path
    
    Return values:
        out: [boolean] true if valid, false otherwise
    """
    if fpath[-4:] == '.bmp': return True
    if fpath[-4:] == '.png': return True
    if fpath[-4:] == '.tif': return True
    if fpath[-5:] == '.tiff': return True
    return False

def load_image_batch(image,fpaths):
    """Loads an image for batch mode
    
    Arguments:
        image: the array in which to store the loaded image
        fpaths: a list of file paths to open. For mixed images,
            this should contain a single element; for split ones,
            this should contain three elements
    
    Return values:
        max_pixel: [f64] the maximum possible pixel value
            
    Exceptions: Same as check_paths() function
    """
    check_paths(fpaths)
    if len(fpaths) == 1:
        raw_image = scipy.misc.imread(fpaths[0])
        for i in range(3):
            image[i,:,:] = raw_image[:,:,i].astype(np.float)
    elif len(fpaths) == 3:
        for i in range(3):
            raw_image = scipy.misc.imread(fpaths[i])
            image[i,:,:] = raw_image.astype(np.float)
    return 2**(8*raw_image.itemsize)
