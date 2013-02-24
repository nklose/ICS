""" Tests the image_reader class. Requires the mock library, install via

sudo pip install -U mock
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
