import argparse
import numpy as np
import os.path
import sys


def ics_similar(fname_old, fname_new):
    a = np.loadtxt(fname_old)
    b = np.loadtxt(fname_new)
    return np.all(np.abs(a - b) < 0.05)


def validate_output(expectedOutput, output):
    fnames = ['ACb', 'ACg', 'ACr', 'XCrg', 'XCrb', 'XCrg', "TripleCrgb"]
    fname_old = fname_new = None
    for fname in fnames:
        fname_old = os.path.join(expectedOutput, '%s.txt' % (fname))
        fname_new = os.path.join(output, '%s.txt' % fname)
        assertIsSimiliar(fname_old, fname_new)

        fname_old = os.path.join(expectedOutput, '%sFit.txt' % (fname))
        fname_new = os.path.join(output, '%sFit.txt' % fname)
        assertIsSimiliar(fname_old, fname_new)


def assertIsSimiliar(fname_old, fname_new):
    if not ics_similar(fname_old, fname_new):
        print "%s doesn't match %s" % (fname_old, fname_new)
        sys.exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("expectedOutput")
    parser.add_argument("actualOutput")
    args = parser.parse_args()
    validate_output(args.expectedOutput, args.actualOutput)
    print "All values match"
