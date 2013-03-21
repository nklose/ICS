""" Tests the backend_utils module. Requires the mock library, install via

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
import os

import backend.backend_utils as beutils


class TestBackendUtils(unittest.TestCase):

    @patch.object(beutils, "np")
    def test_gauss_1d(self, mockNp):
        mockX = MagicMock()
        mockNp.exp.return_value = 5
        mockPower = MagicMock()
        mockNeg = MagicMock()
        mockTrueDiv = MagicMock()
        mockNeg.__truediv__.return_value = mockTrueDiv
        mockPower.__neg__.return_value = mockNeg
        mockX.__pow__.return_value = mockPower

        retVal = beutils.gauss_1d(mockX, 10, 2, 3)

        self.assertEqual(53, retVal)
        self.assertTrue(mockNp.exp.called)
        mockNp.exp.assert_called_with(mockTrueDiv)

    @patch.object(beutils, "np")
    def test_gauss_2d(self, mockNp):
        mockX = MagicMock()
        mockNp.size.return_value = 25.0
        mockNp.sqrt.return_value = 5.0
        mockNp.exp.return_value = 5

        retVal = beutils.gauss_2d(mockX, 10, 2, 3)

        self.assertEqual(53, retVal)
        self.assertTrue(mockNp.exp.called)
        mockNp.size.assert_called_with(mockX)
        mockNp.sqrt.assert_called_with(25.0)

    @patch.object(beutils, "np")
    def test_gauss_2d_deltas(self, mockNp):
        mockX = MagicMock()
        mockNp.size.return_value = 25.0
        mockNp.sqrt.return_value = 5.0
        mockNp.exp.return_value = 5

        retVal = beutils.gauss_2d_deltas(mockX, 10, 2, 3, 7, 14)

        self.assertEqual(53, retVal)
        self.assertTrue(mockNp.exp.called)
        mockNp.size.assert_called_with(mockX)
        mockNp.sqrt.assert_called_with(25.0)

    @patch.object(beutils, "os")
    @patch.object(beutils.ctypes, "cdll")
    def test_load_library_linux(self, mockCdll, mockOs):
        mockOs.name = "linux"
        mockOs.path.dirname.return_value = "foo"
        mockOs.path.join.side_effect = os.path.join

        retVal = beutils.load_library()

        self.assertEqual(retVal, mockCdll.LoadLibrary.return_value)
        call_path = os.path.join("foo", "libbackend.so")
        mockCdll.LoadLibrary.assert_called_with(call_path)

    @patch.object(beutils, "os")
    @patch.object(beutils.ctypes, "cdll")
    def test_load_library_windows(self, mockCdll, mockOs):
        mockOs.name = "nt"
        mockOs.path.dirname.return_value = "foo"
        mockOs.path.join.side_effect = os.path.join

        retVal = beutils.load_library()

        self.assertEqual(retVal, mockCdll.LoadLibrary.return_value)
        call_path = os.path.join("", "libbackend.dll")
        mockCdll.LoadLibrary.assert_called_with(call_path)
