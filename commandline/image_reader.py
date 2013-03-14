""" Contains code to convert an input image into a bitmap. This allows all
backend work to be done in one file format.

The standard way to open files now would be:

>>> import image_reader
>>> redImage, greenImage, blueImage = image_reader.get_channels_single(image)

Copryight (c) 2013 Nick Klose, Richard Leung, Cameron Mann, Glen Nelson, Omar
Qadri, and James Wang under the 401 IP License.

This Agreement, effective the 1st day of April 2013, is entered into by and
between Dr. Nils Petersen (hereinafter "client") and the students of the
Biomembrane team (hereinafter "the development team"), in order to establish
terms and conditions concerning the completion of the Image Correlation
Spectroscopy application (hereinafter "The Application") which is limited to the
application domain of application-domain (hereinafter "the domain of use for the
application").  It is agreed by the client and the development team that all
domain specific knowledge and compiled research is the intellectual property of
the client, regarded as a copyrighted collection. The framework and code base
created by the development team is their own intellectual property, and may only
be used for the purposes outlined in the documentation of the application, which
has been provided to the client. The development team agrees not to use their
framework for, or take part in the development of, anything that falls within
the domain of use for the application, for a period of 6 (six) months after the
signing of this agreement.
"""
import PythonMagick
from PIL import Image
import scipy
import logging


LOGGER = logging.getLogger("imgrdr")


class ImageFormatException(Exception):
    """ Exception if the file has an invalid image type.
    """
    def __init__(self, filepath, imagetype):
        msg = "File %s has invalid image type: %s" % (filepath, imagetype)
        self.filepath = filepath
        self.imagetype = imagetype
        super(ImageFormatException, self).__init__(msg)


def open_image(filepath):
    """ Opens the given image if loseless and send the data to scipy.

    Arguments:
        filepath: The path to the file to open
        filepath type: string

    Return Value:
        The image opened in scipy.

    Raises:
        image_converter.ImageFormatException: If file type is invalid
    """
    image = validate_image(filepath)
    #image = PIL.Image.open(filepath)
    return scipy.misc.fromimage(image)


def validate_image(filepath):
    """ Checks if the image file is valid (Lossless / uncompressed).

    Arguments:
        filepath: The path to the file to open
        filepath type: string

    Return Value:
        The image opened in PIL.

    Raises:
        image_converter.ImageFormatException: If file type is invalid
    """
    image = PythonMagick.Image(filepath)
    comp_type = image.attribute("CompressionType")
    LOGGER.debug("File: %s has CompressionType \"%s\"" % (filepath, comp_type))
    if comp_type != '':
        raise ImageFormatException(filepath, comp_type)
    return convertMGtoPIL(image)


def convertMGtoPIL(magickimage):
    """ From http://www.imagemagick.org/download/python/README.txt
    """
    # make copy
    img = PythonMagick.Image(magickimage)
    # this takes 0.04 sec. for 640x480 image
    img.depth = 8
    img.magick = "RGB"
    blob = PythonMagick.Blob()
    img.write(blob, "RGB")
    data = PythonMagick.get_blob_data(blob)
    w, h = img.columns(), img.rows()
    # convert string array to an RGB Pil image
    pilimage = Image.fromstring('RGB', (w, h), data)
    return pilimage


def get_channels_single(filepath, astype="d"):
    """ Returns the RGB channels for a single image.

    Arguments:
        filepath: The path to the file to open
        filepath type: string
        astype: The type to open the image as.
    :   astype type: string or Type.

    Return Value:
        Tuple of RGB channels.
    """
    image = open_image(filepath)
    r = image[:, :, 0].astype(astype)
    g = image[:, :, 1].astype(astype)
    b = image[:, :, 2].astype(astype)
    return (r, g, b)


def get_channels_separate(red_path, green_path, blue_path, astype="d"):
    """ Returns the RGB channels for channel separated images.

    Arguments:
        red_path: The path to the red image
        red_path type: string
        green_path: The path to the green image
        green_path type: string
        blue_path: The path the blue image
        blue_path type: string
        astype: The type to open the image as.
    :   astype type: string or Type.

    Return Value:
        Tuple of RGB channels.
    """
    r = open_image(red_path).astype(astype)
    g = open_image(green_path).astype(astype)
    b = open_image(blue_path).astype(astype)
    return (r, g, b)
