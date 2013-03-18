""" Tests the dual module. Requires the mock library, install via

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

import backend.dual as dual


class TestBackendDual(unittest.TestCase):
    """ This module had one function but many paths. As part of this test, I
        have split it into units so that path testing and functional testing
        is simplier.
    """

    @patch.object(dual, '_default_no_deltas')
    @patch.object(dual, '_get_deltas')
    @patch.object(dual, '_get_inputs')
    @patch.object(dual, '_get_two_image_values')
    @patch.object(dual, '_get_single_image_values')
    def test_core_auto_using_deltas(self, mockgsiv, mockgwiv, mockgi, mockgd,
                                    mockdnd):
        mockTemp = Mock()
        mockgwiv.return_value = (5, mockTemp, mockTemp)
        mockgsiv.return_value = (5, mockTemp, mockTemp)
        mockFirstEntry = Mock()
        mockOut = MagicMock()
        mockOut.__setitem__.return_value = Mock()
        mockParValue = MagicMock()
        mockParValue.__abs__.return_value = Mock()
        mockPar = MagicMock()
        mockPar.__getitem__.return_value = mockParValue
        mockPar.__setitem__.return_value = mockParValue
        mockXData = Mock()
        mockYData = Mock()
        mockgi.return_value = (mockFirstEntry, mockXData, mockYData, mockPar,
                               mockOut)
        mockgd.return_value = (mockPar, True)
        mockdnd.return_value = mockPar

        mockImage = Mock()
        mockInitVal = Mock()

        retVal = dual.core(mockImage, None, 20, mockInitVal, True)
        self.assertFalse(mockgwiv.called)
        self.assertFalse(mockdnd.called)
        mockgsiv.assert_called_with(mockImage)
        mockgi.assert_called_with(20, mockTemp, mockTemp, 5)
        mockgd.assert_called_with(mockPar, mockXData, mockYData, mockInitVal)
        self.assertEqual((mockOut, mockPar, True), retVal)

    @patch.object(dual, '_default_no_deltas')
    @patch.object(dual, '_get_deltas')
    @patch.object(dual, '_get_inputs')
    @patch.object(dual, '_get_two_image_values')
    @patch.object(dual, '_get_single_image_values')
    def test_core_auto_using_deltas_failed(self, mockgsiv, mockgwiv, mockgi,
                                           mockgd, mockdnd):
        mockTemp = Mock()
        mockgwiv.return_value = (5, mockTemp, mockTemp)
        mockgsiv.return_value = (5, mockTemp, mockTemp)
        mockFirstEntry = Mock()
        mockOut = MagicMock()
        mockOut.__setitem__.return_value = Mock()
        mockParValue = MagicMock()
        mockParValue.__abs__.return_value = Mock()
        mockPar = MagicMock()
        mockPar.__getitem__.return_value = mockParValue
        mockPar.__setitem__.return_value = mockParValue
        mockXData = Mock()
        mockYData = Mock()
        mockgi.return_value = (mockFirstEntry, mockXData, mockYData, mockPar,
                               mockOut)
        mockgd.return_value = (mockPar, False)
        mockdnd.return_value = mockPar

        mockImage = Mock()
        mockInitVal = Mock()

        retVal = dual.core(mockImage, None, 20, mockInitVal, True)
        self.assertFalse(mockgwiv.called)
        mockgsiv.assert_called_with(mockImage)
        mockgi.assert_called_with(20, mockTemp, mockTemp, 5)
        mockgd.assert_called_with(mockPar, mockXData, mockYData, mockInitVal)
        mockdnd.assert_called_with(mockPar, mockXData, mockYData, mockInitVal)
        self.assertEqual((mockOut, mockPar, False), retVal)

    @patch.object(dual, '_default_no_deltas')
    @patch.object(dual, '_get_deltas')
    @patch.object(dual, '_get_inputs')
    @patch.object(dual, '_get_two_image_values')
    @patch.object(dual, '_get_single_image_values')
    def test_core_auto_no_deltas(self, mockgsiv, mockgwiv, mockgi, mockgd,
                                 mockdnd):
        mockTemp = Mock()
        mockgwiv.return_value = (5, mockTemp, mockTemp)
        mockgsiv.return_value = (5, mockTemp, mockTemp)
        mockFirstEntry = Mock()
        mockOut = MagicMock()
        mockOut.__setitem__.return_value = Mock()
        mockParValue = MagicMock()
        mockParValue.__abs__.return_value = Mock()
        mockPar = MagicMock()
        mockPar.__getitem__.return_value = mockParValue
        mockPar.__setitem__.return_value = mockParValue
        mockXData = Mock()
        mockYData = Mock()
        mockgi.return_value = (mockFirstEntry, mockXData, mockYData, mockPar,
                               mockOut)
        mockgd.return_value = (mockPar, True)
        mockdnd.return_value = mockPar

        mockImage = Mock()
        mockInitVal = Mock()

        retVal = dual.core(mockImage, None, 20, mockInitVal, False)
        self.assertFalse(mockgwiv.called)
        self.assertFalse(mockgd.called)
        mockgsiv.assert_called_with(mockImage)
        mockgi.assert_called_with(20, mockTemp, mockTemp, 5)
        mockdnd.assert_called_with(mockPar, mockXData, mockYData, mockInitVal)
        self.assertEqual((mockOut, mockPar, False), retVal)

    @patch.object(dual, '_default_no_deltas')
    @patch.object(dual, '_get_deltas')
    @patch.object(dual, '_get_inputs')
    @patch.object(dual, '_get_two_image_values')
    @patch.object(dual, '_get_single_image_values')
    def test_core_cross_using_deltas(self, mockgsiv, mockgwiv, mockgi, mockgd,
                                     mockdnd):
        mockTemp = Mock()
        mockgwiv.return_value = (5, mockTemp, mockTemp)
        mockgsiv.return_value = (5, mockTemp, mockTemp)
        mockFirstEntry = Mock()
        mockOut = MagicMock()
        mockOut.__setitem__.return_value = Mock()
        mockParValue = MagicMock()
        mockParValue.__abs__.return_value = Mock()
        mockPar = MagicMock()
        mockPar.__getitem__.return_value = mockParValue
        mockPar.__setitem__.return_value = mockParValue
        mockXData = Mock()
        mockYData = Mock()
        mockgi.return_value = (mockFirstEntry, mockXData, mockYData, mockPar,
                               mockOut)
        mockgd.return_value = (mockPar, True)
        mockdnd.return_value = mockPar

        mockImage = Mock()
        mockInitVal = Mock()

        retVal = dual.core(mockImage, mockImage, 20, mockInitVal, True)
        self.assertFalse(mockgsiv.called)
        self.assertFalse(mockdnd.called)
        mockgwiv.assert_called_with(mockImage, mockImage)
        mockgi.assert_called_with(20, mockTemp, mockTemp, 5)
        mockgd.assert_called_with(mockPar, mockXData, mockYData, mockInitVal)
        self.assertEqual((mockOut, mockPar, True), retVal)

    @patch.object(dual, '_default_no_deltas')
    @patch.object(dual, '_get_deltas')
    @patch.object(dual, '_get_inputs')
    @patch.object(dual, '_get_two_image_values')
    @patch.object(dual, '_get_single_image_values')
    def test_core_cross_no_deltas(self, mockgsiv, mockgwiv, mockgi, mockgd,
                                  mockdnd):
        mockTemp = Mock()
        mockgwiv.return_value = (5, mockTemp, mockTemp)
        mockgsiv.return_value = (5, mockTemp, mockTemp)
        mockFirstEntry = Mock()
        mockOut = MagicMock()
        mockOut.__setitem__.return_value = Mock()
        mockParValue = MagicMock()
        mockParValue.__abs__.return_value = Mock()
        mockPar = MagicMock()
        mockPar.__getitem__.return_value = mockParValue
        mockPar.__setitem__.return_value = mockParValue
        mockXData = Mock()
        mockYData = Mock()
        mockgi.return_value = (mockFirstEntry, mockXData, mockYData, mockPar,
                               mockOut)
        mockgd.return_value = (mockPar, True)
        mockdnd.return_value = mockPar

        mockImage = Mock()
        mockInitVal = Mock()

        retVal = dual.core(mockImage, mockImage, 20, mockInitVal, False)
        self.assertFalse(mockgsiv.called)
        self.assertFalse(mockgd.called)
        mockgwiv.assert_called_with(mockImage, mockImage)
        mockgi.assert_called_with(20, mockTemp, mockTemp, 5)
        mockdnd.assert_called_with(mockPar, mockXData, mockYData, mockInitVal)
        self.assertEqual((mockOut, mockPar, False), retVal)

    @patch.object(dual, "np")
    def test_get_single_image_values(self, mockNumPy):
        mockTemp1 = Mock()
        mockTemp2 = Mock()
        mockNumPy.average.return_value = 5
        mockNumPy.size.return_value = 10
        mockNumPy.fft.fft2.return_value = mockTemp1
        mockNumPy.conj.return_value = mockTemp2
        mockImage = Mock()

        expectedReturn = (250, mockTemp1, mockTemp2)
        retVal = dual._get_single_image_values(mockImage)

        self.assertEqual(expectedReturn, retVal)
        mockNumPy.average.assert_called_with(mockImage)
        mockNumPy.size.assert_called_with(mockImage)
        mockNumPy.fft.fft2.assert_called_with(mockImage)
        mockNumPy.conj.assert_called_with(mockTemp1)

    @patch.object(dual, "np")
    def test_get_two_image_values(self, mockNumPy):
        mockTemp1 = MagicMock()
        mockTemp2 = MagicMock()
        mockNumPy.average.return_value = 5
        mockNumPy.size.return_value = 10
        mockNumPy.fft.fft2.return_value = mockTemp1
        mockNumPy.conj.return_value = mockTemp2
        mockImage1 = Mock()
        mockImage2 = Mock()

        expectedReturn = (250, mockTemp1, mockTemp2)
        retVal = dual._get_two_image_values(mockImage1, mockImage2)

        self.assertEqual(expectedReturn, retVal)
        self.assertEqual(mockNumPy.average.call_count, 2)
        mockNumPy.size.assert_called_with(mockImage1)
        self.assertEqual(mockNumPy.fft.fft2.call_count, 2)
        mockNumPy.conj.assert_called_with(mockTemp1)

    @patch.object(dual, "np")
    def test_get_inputs(self, mockNumPy):
        mockTmp = MagicMock()
        mockTemp1 = MagicMock()
        mockTemp2 = MagicMock()
        mockTemp1.__mul__.return_value = Mock()
        mockFinalOut = Mock()
        mockOut = MagicMock()
        mockOut.__truediv__.return_value.__sub__.return_value = mockFinalOut
        mockFinalOut.__getitem__ = Mock()
        mockFinalOut.__setitem__ = Mock()
        mockXData = Mock()
        mockYData = Mock()
        mockPar = Mock()

        mockNumPy.fft.ifft2.return_value = mockTmp
        mockNumPy.float64.return_value = mockOut
        mockNumPy.arange.return_value = mockXData
        mockNumPy.reshape.return_value = mockYData
        mockNumPy.zeros.return_value = mockPar

        expectedValue = (mockFinalOut.__getitem__.return_value, mockXData,
                         mockYData, mockPar, mockFinalOut)

        retVal = dual._get_inputs(20, mockTemp1, mockTemp2, 10)

        self.assertEqual(expectedValue, retVal)
        self.assertTrue(mockNumPy.fft.ifft2.called)
        self.assertTrue(mockNumPy.float64.called)
        self.assertTrue(mockNumPy.arange.called)
        self.assertTrue(mockNumPy.reshape.called)
        self.assertTrue(mockNumPy.zeros.called)

    @patch.object(dual, 'butils')
    @patch.object(dual.scipy, "optimize")
    def test_get_deltas_truePath(self, mockScipy, mockBackendUtils):
        mockPar = MagicMock()
        mockPar.__getitem__.return_value = 0
        mockInitVal = MagicMock()
        mockInitVal.__getitem__.return_value = 10
        mockScipy.curve_fit.return_value = (mockPar, Mock())
        mockXData = Mock()
        mockYData = Mock()

        expectedValue = (mockPar, True)
        retVal = dual._get_deltas(mockPar, mockXData, mockYData, mockInitVal)
        mockScipy.curve_fit.assert_called_with(
            mockBackendUtils.gauss_2d_deltas, mockXData, mockYData, mockInitVal)

        self.assertEqual(expectedValue, retVal)

    @patch.object(dual, 'butils')
    @patch.object(dual.scipy, "optimize")
    def test_get_deltas_falsePath(self, mockScipy, mockBackendUtils):
        mockPar = MagicMock()
        mockPar.__getitem__.return_value = 10
        mockInitVal = MagicMock()
        mockInitVal.__getitem__.return_value = 1
        mockScipy.curve_fit.return_value = (mockPar, Mock())
        mockXData = Mock()
        mockYData = Mock()

        expectedValue = (mockPar, False)
        retVal = dual._get_deltas(mockPar, mockXData, mockYData, mockInitVal)
        mockScipy.curve_fit.assert_called_with(
            mockBackendUtils.gauss_2d_deltas, mockXData, mockYData, mockInitVal)

        self.assertEqual(expectedValue, retVal)

    @patch.object(dual, 'butils')
    @patch.object(dual.scipy, "optimize")
    def test_default_no_deltas(self, mockScipy, mockBackendUtils):
        mockPar = MagicMock()
        mockPar.__getitem__.return_value = 10
        mockInitVal = MagicMock()
        mockInitVal.__getitem__.return_value = 1
        mockScipy.curve_fit.return_value = (mockPar, Mock())
        mockXData = Mock()
        mockYData = Mock()

        expectedValue = mockPar
        retVal = dual._default_no_deltas(mockPar, mockXData, mockYData,
                                         mockInitVal)
        mockScipy.curve_fit.assert_called_with(
            mockBackendUtils.gauss_2d, mockXData, mockYData,
            mockInitVal.__getitem__.return_value)

        self.assertEqual(expectedValue, retVal)
