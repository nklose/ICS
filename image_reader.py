""" Contains code to convert an input image into a bitmap. This allows all
backend work to be done in one file format.

The standard way to open files now would be:

>>> import image_converter
>>> scipyImage = image_converter.open_image(image)

I think the image is equivalent to opening a bitmap.
"""
import PIL
import scipy
import imghdr


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
    validate_image(filepath)
    image = PIL.Image.open(filepath)
    return scipy.misc.fromimage(image)


def validate_image(filepath):
    """ Checks if the image file is valid (Lossless / uncompressed).

    Arguments:
        filepath: The path to the file to open
        filepath type: string

    Raises:
        image_converter.ImageFormatException: If file type is invalid
    """
    header_type = imghdr.what(filepath)
    if header_type not in ['bmp', 'gif', 'png', 'tiff']:
        raise ImageFormatException(filepath, header_type)

def get_channels_single(filepath):
    """ Returns the RGB channels for a single image.

    Arguments:
        filepath: The path to the file to open
        filepath type: string

    Return Value:
        Tuple of RGB channels.
    """
    image = open_image(filepath)
    r = image[::0].astype('d')
    g = image[::1].astype('d')
    b = image[::2].astype('d')
    return (r, g, b)

def get_channels_separate(red_path, green_path, blue_path):
    """ Returns the RGB channels for channel separated images.

    Arguments:
        red_path: The path to the red image
        red_path type: string
        green_path: The path to the green image
        green_path type: string
        blue_path: The path the blue image
        blue_path type: string

    Return Value:
        Tuple of RGB channels.
    """
    r = open_image(red_path)[::0].astype('d')
    g = open_image(green_path)[::1].astype('d')
    b = open_image(blue_path)[::2].astype('d')
    return (r, g, b)
