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
from mock import MagicMock, Mock, patch

import backend.bimloader as bimloader


class TestBackendImageLoader(unittest.TestCase):

    @patch.object(bimloader, 'PythonMagick')
    def test_validate_image(self, mockPythonMagick):
        mockImage = Mock()
        mockImage.attribute.return_value = ""
        mockPythonMagick.Image.return_value = mockImage
        bimloader.validate_image("foo")
        mockPythonMagick.Image.assert_called_with("foo")
        mockImage.attribute.assert_called_with("CompressionType")

    @patch.object(bimloader, 'PythonMagick')
    def test_validate_image_bad(self, mockPythonMagick):
        mockImage = Mock()
        mockImage.attribute.return_value = "bar"
        mockPythonMagick.Image.return_value = mockImage
        expectedMsg = "File foo has invalid image type"
        self.assertRaisesRegexp(bimloader.ImageFormatException,
                                expectedMsg, bimloader.validate_image,
                                "foo")
        mockPythonMagick.Image.assert_called_with("foo")
        mockImage.attribute.assert_called_with("CompressionType")

    @patch.object(bimloader, "validate_image")
    @patch.object(bimloader.scipy, "misc")
    def test_load_image_mixed(self, mockScipyMisc, mockValidateImage):
        mockRawImage = MagicMock()
        mockChannel = Mock()
        mockRawImage.__getitem__.return_value.astype.return_value = mockChannel
        mockScipyMisc.imread.return_value = mockRawImage

        expectedReturn = (mockChannel, mockChannel, mockChannel)
        retVal = bimloader.load_image_mixed("foo")

        self.assertEqual(expectedReturn, retVal)
        call_count = mockRawImage.__getitem__.return_value.astype.call_count
        self.assertEqual(call_count, 3)
        mockValidateImage.assert_called_with("foo")
        mockScipyMisc.imread.assert_called_with("foo")

    @patch.object(bimloader.scipy, "misc")
    def test_load_image_pil_mixed(self, mockScipyMisc):
        mockRawImage = MagicMock()
        mockChannel = Mock()
        mockRawImage.__getitem__.return_value.astype.return_value = mockChannel
        mockScipyMisc.fromimage.return_value = mockRawImage
        mockPilImage = Mock()

        expectedReturn = (mockChannel, mockChannel, mockChannel)

        retVal = bimloader.load_image_pil_mixed(mockPilImage)

        self.assertEqual(expectedReturn, retVal)
        mockScipyMisc.fromimage.assert_called_with(mockPilImage)

    @patch.object(bimloader, "validate_image")
    @patch.object(bimloader.scipy, "misc")
    def test_load_image_split(self, mockScipyMisc, mockValidateImage):
        mockRawChannel = Mock()
        mockScipyMisc.imread.return_value = mockRawChannel

        expectedReturn = mockRawChannel.astype.return_value
        retVal = bimloader.load_image_split("foo")

        self.assertEqual(expectedReturn, retVal)
        call_count = mockRawChannel.astype.call_count
        self.assertEqual(call_count, 1)
        mockValidateImage.assert_called_with("foo")
        mockScipyMisc.imread.assert_called_with("foo")

    @patch.object(bimloader.scipy, "misc")
    def test_load_image_pil_split(self, mockScipyMisc):
        mockRawChannel = Mock()
        mockScipyMisc.fromimage.return_value = mockRawChannel
        mockPilImage = Mock()

        retVal = bimloader.load_image_pil_split(mockPilImage)

        self.assertEqual(mockRawChannel.astype.return_value, retVal)
        mockScipyMisc.fromimage.assert_called_with(mockPilImage)

    @patch.object(bimloader, "validate_image")
    @patch.object(bimloader.scipy, "misc")
    def test_load_image_mixed_batch(self, mockScipyMisc, mockValidateImage):
        mockRawImage = MagicMock()
        mockChannel = Mock()
        mockRawImage.__getitem__.return_value = mockChannel
        mockScipyMisc.imread.return_value = mockRawImage
        mockBatchImage = MagicMock()

        bimloader.load_image_mixed_batch(mockBatchImage, "foo")

        self.assertEqual(mockChannel.astype.call_count, 3)
        mockValidateImage.assert_called_with("foo")
        mockScipyMisc.imread.assert_called_with("foo")
        self.assertEqual(mockBatchImage.__setitem__.call_count, 3)

    @patch.object(bimloader, "validate_image")
    @patch.object(bimloader.scipy, "misc")
    def test_load_image_split_batch(self, mockScipyMisc, mockValidateImage):
        mockRawChannel = Mock()
        mockScipyMisc.imread.return_value = mockRawChannel
        mockBatchImage = MagicMock()

        bimloader.load_image_split_batch(mockBatchImage, "foo")

        self.assertTrue(mockRawChannel.astype.called)
        mockValidateImage.assert_called_with("foo")
        mockScipyMisc.imread.assert_called_with("foo")
        self.assertEqual(mockBatchImage.__setitem__.call_count, 1)
