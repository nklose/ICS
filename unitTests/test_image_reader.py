""" Tests the image_reader class. Requires the mock library, install via

sudo pip install -U mock

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
import unittest
from mock import Mock, patch

import image_reader


class TestICSE(unittest.TestCase):

    @patch.object(image_reader, "validate_image")
    @patch.object(image_reader.PIL, "Image")
    @patch.object(image_reader.scipy, "misc")
    def test_open_image(self, mockScipyMisc, mockPILImage, mockValidateImage):
        mockPILFile = Mock()
        mockSCIPYFile = Mock()
        mockScipyMisc.fromimage.return_value = mockSCIPYFile
        mockPILImage.open.return_value = mockPILFile
        ret_val = image_reader.open_image("foo")
        mockValidateImage.assert_called_with("foo")
        self.assertEqual(ret_val, mockSCIPYFile)
        mockScipyMisc.fromimage.assert_called_with(mockPILFile)

    @patch.object(image_reader, 'imghdr')
    def test_validate_image(self, mockImgHdr):
        ret_val_list = ['bmp', 'gif', 'png', 'tiff']
        for item in ret_val_list:
            mockImgHdr.what.return_value = item
            image_reader.validate_image("foo")
            mockImgHdr.what.assert_called_with("foo")
            mockImgHdr.reset_mock()

    @patch.object(image_reader, 'imghdr')
    def test_validate_image_bad(self, mockImgHdr):
        mockImgHdr.what.return_value = "bar"
        expectedMsg = "File foo has invalid image type: bar"
        self.assertRaisesRegexp(image_reader.ImageFormatException,
                                expectedMsg, image_reader.validate_image,
                                "foo")
        mockImgHdr.what.assert_called_with("foo")
