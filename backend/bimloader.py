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
import PythonMagick
import wand.image
from PIL import Image


class ImageFormatException(Exception):
    """ The exception that is raised when
    the format of an image file is invalid
    """
    def __init__(self, fpath):
        msg = str.format("File {:s} has invalid image type", fpath)
        self.fpath = fpath
        super(ImageFormatException, self).__init__(msg)


def validate_image(filepath, mixed):
    """ Checks if the image file is valid (Lossless / uncompressed).

    Arguments:
        filepath: The path to the file to open
        filepath type: string

        mixed: Whether the image is a "mixed" image or not.
        mixed type: boolean

    Return Value:
        The image opened in PIL.

    Raises:
        image_converter.ImageFormatException: If file type is invalid
    """
    image = PythonMagick.Image(filepath)
    comp_type = image.attribute("CompressionType")
    img_format = image.format()
    jpeg_format = 'Joint Photographic Experts Group JFIF format'
    if comp_type != '' or img_format == jpeg_format:
        raise ImageFormatException(filepath)
    return convertWandtoScipy(wand.image.Image(filename=filepath), mixed)


def convertWandtoScipy(wandImage, mixed):
    """ Convert a Wand image to a scipy image

    Arguments:
        wandImage: The file in wand.
        wandImage type: wand.image.Image

        mixed: Whether the image is a "mixed" image or not.
        mixed type: boolean

    Return Value:
        The image opened in PIL.
    """
    img = wand.image.Image(wandImage)
    conv_wand = "RGB"
    conv_pil = "RGB"
    data = img.make_blob(conv_wand)
    pilimage = Image.fromstring(conv_pil, img.size, data)
    if mixed:
        array = scipy.misc.fromimage(pilimage)
    if not mixed:
        pilimage = pilimage.convert("L")
        array = scipy.misc.fromimage(pilimage)
    return array


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
    raw_image = validate_image(fpath, True)
    r = raw_image[:, :, 0].astype(np.float)
    g = raw_image[:, :, 1].astype(np.float)
    b = raw_image[:, :, 2].astype(np.float)
    return (r, g, b)


def load_image_pil_mixed(pilImage):
    """Loads a mixed image

    Arguments:
       pilImage: the PIL form of the image

    Return values:
        r: the red channel
        g: the green channel
        b: the blue channel

    Exceptions:
        ImageFormatException
    """
    raw_image = scipy.misc.fromimage(pilImage)
    r = raw_image[:, :, 0].astype(np.float)
    g = raw_image[:, :, 1].astype(np.float)
    b = raw_image[:, :, 2].astype(np.float)
    return (r, g, b)


def load_image_split(fpath):
    """Loads a channel of a split image

    Arguments:
        fpath: the file path to open
    Return values:
        channel: the loaded channel
    Exceptions:
        ImageFormatException
    """
    raw_channel = validate_image(fpath, False)
    channel = raw_channel.astype(np.float)
    return channel


def load_image_pil_split(pilImage):
    """Loads a channel of a split image

    Arguments:
       pilImage: the PIL form of the image
    Return values:
        channel: the loaded channel
    Exceptions:
        ImageFormatException
    """
    raw_channel = scipy.misc.fromimage(pilImage)
    channel = raw_channel.astype(np.float)
    return channel


def load_image_mixed_batch(image, fpath):
    """Loads a mixed image for batch mode

    Arguments:
        image: the array in which to store the loaded image
        fpath: the file path to open
    There are no return values.
    Exceptions:
        ImageFormatException
    """
    raw_image = validate_image(fpath, True)
    image[0, :, :] = raw_image[:, :, 0].astype(np.float)
    image[1, :, :] = raw_image[:, :, 1].astype(np.float)
    image[2, :, :] = raw_image[:, :, 2].astype(np.float)


def load_image_split_batch(image, fpath):
    """Loads one channel of a split image for batch mode

    Arguments:
        image: the array in which to store the loaded channel
        fpath: the file path to open
    There are no return values.
    Exceptions:
        ImageFormatException
    """
    raw_channel = validate_image(fpath, False)
    image[:, :] = raw_channel.astype(np.float)
