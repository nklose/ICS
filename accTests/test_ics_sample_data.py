import unittest
import os
import numpy as np
import icse


class TestICSE(unittest.TestCase):

    def setUp(self):
        self.mdata = os.path.join(os.path.dirname(__file__), "mdata")

    def test_ics_output(self):
        icse.ics_entire_test()
        root_dir = get_root_dir()
        output_dir = os.path.join(root_dir, 'output')
        fnames = ['ACb', 'ACg', 'ACr', 'XCrg', 'XCrb', 'XCrg']
        fname_old = fname_new = None
        for fname in fnames:
            fname_old = os.path.join(self.mdata, '%s.txt' % (fname))
            fname_new = os.path.join(output_dir, 'new%s.txt' % fname)
            if not ics_similar(fname_old, fname_new):
                print '%s %s' % (fname_old, fname_new)
                fname_old = os.path.join(self.mdata, '%sFit.txt' % (fname))
                fname_new = os.path.join(output_dir, 'new%sFit.txt' % fname)
                if not ics_similar(fname_old, fname_new):
                    print '%s %s' % (fname_old, fname_new)


def get_root_dir():
    return os.path.dirname(os.path.dirname(__file__))


def ics_similar(fname_old, fname_new):
    a = np.loadtxt(fname_old)
    b = np.loadtxt(fname_new)
    return np.all(np.abs(a - b) < 0.05)
