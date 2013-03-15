""" Contains code to convert an input image into a bitmap. This allows all
backend work to be done in one file format.

The standard way to open files now would be:

>>> import image_reader
>>> redImage, greenImage, blueImage = image_reader.get_channels(image)

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
import PIL.Image
import scipy.misc
import numpy as np


def get_channels(image, astype="d"):
    """ Returns the RGB channels for a single image.

    Arguments:
        filepath: The path to the file to open
        filepath type: string
        astype: The type to open the image as.
    :   astype type: string or Type.

    Return Value:
        Tuple of RGB channels.
    """
    r = image[:, :, 0].astype(astype)
    g = image[:, :, 1].astype(astype)
    b = image[:, :, 2].astype(astype)
    return (r, g, b)


def create_image(red, green, blue):
    rgb = np.dstack((red, green, blue)) 
    rgb_image = PIL.Image.fromarray(np.uint8(rgb))
    return rgb_image


def create_images(red, green, blue):
    red_image = PIL.Image.fromarray(np.uint8(red))
    green_image = PIL.Image.fromarray(np.uint8(green))
    blue_image = PIL.Image.fromarray(np.uint8(blue))
    return (red_image, green_image, blue_image)
