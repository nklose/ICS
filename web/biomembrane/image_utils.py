"""
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
import numpy as np
import StringIO


def get_channels(image, astype="d"):
    """ Returns the RGB channels for a single image. """
    r = image[:, :, 0].astype(astype)
    g = image[:, :, 1].astype(astype)
    b = image[:, :, 2].astype(astype)
    return (r, g, b)


def create_image(red, green, blue):
    """ Creates a single from color channels """
    rgb = np.dstack((red, green, blue))
    rgb_image = PIL.Image.fromarray(np.uint8(rgb))
    return rgb_image


def create_images(red, green, blue):
    """ Creates separate images for each color channel """
    zeros = np.zeros(red.shape)
    red = np.dstack((red, zeros, zeros))
    red_image = PIL.Image.fromarray(np.uint8(red))
    green = np.dstack((zeros, green, zeros))
    green_image = PIL.Image.fromarray(np.uint8(green))
    blue = np.dstack((zeros, zeros, blue))
    blue_image = PIL.Image.fromarray(np.uint8(blue))
    return (red_image, green_image, blue_image)


def get_intensities(rgb_image):
    array = np.asarray(rgb_image)
    r, g, b = get_channels(array)
    red_int = np.average(r)
    green_int = np.average(g)
    blue_int = np.average(b)
    return (red_int, green_int, blue_int)


def image_to_string_io(image):
    """ Convert PIL image to StringIO object """
    io = StringIO.StringIO()
    image.save(io, format='PNG')
    io.seek(0)
    return io
