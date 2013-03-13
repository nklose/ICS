""" Contains custom form fields. When possible, these should be used instead of
the django form fields.

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
from django import forms
from io import BytesIO
from django.core.exceptions import ValidationError
from PIL import Image
import tempfile
import os

import commandline.image_reader as image_reader


class LosslessImageField(forms.FileField):

    default_error_messages = {
        'invalid_image': ("Upload a valid image. The file you uploaded was "
                          "either not an image or a corrupted image."),
        'not_losseless': ("Upload a lossless image only. The file you "
                          "uploaded was unrecognized compression or had lossy "
                          "compression. Lossy compression may distort data "
                          "leading to incorrect results. png and bmp are good "
                          "lossless image types.")
    }

    def to_python(self, data):
        """
        Checks that the file-upload field data contains a valid image
        """
        f = super(LosslessImageField, self).to_python(data)

        if f is None:
            return None

        # We need to get a file object for PIL. We might have a path or we might
        # have to read the data into memory.
        isPath = hasattr(data, 'temporary_file_path')
        if isPath:
            file = data.temporary_file_path()
        else:
            if hasattr(data, 'read'):
                file = BytesIO(data.read())
            else:
                file = BytesIO(data['content'])

        try:
            # load() could spot a truncated JPEG, but it loads the entire
            # image in memory, which is a DoS vector. See #3848 and #18520.
            # verify() must be called immediately after the constructor.
            Image.open(file).verify()
        except ImportError:
            # Under PyPy, it is possible to import PIL. However, the underlying
            # _imaging C module isn't available, so an ImportError will be
            # raised. Catch and re-raise.
            raise
        except Exception:
            # Python Imaging Library doesn't recognize it as an image
            raise ValidationError(self.error_messages['invalid_image'])

        fd, path = tempfile.mkstemp()
        try:
            if isPath:
                image_reader.validate_image(file)
            else:
                file.seek(0)
                lines = file.readlines()
                for line in lines:
                    os.write(fd, line)
                os.close(fd)
                return image_reader.validate_image(path)
        except:
            raise ValidationError(self.error_messages['not_losseless'])
        finally:
            os.remove(path)
