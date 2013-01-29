#!/usr/bin/env python
"""
    Runs the automated acceptance tests.  Acceptance tests are based on the
    unittest module.
"""
import sys
import unittest
import os.path


def load_tests(loader, standard_tests, pattern):
    # top level directory cached on loader instance
    this_dir = os.path.dirname(__file__)
    start_dir = os.path.join(this_dir, "accTests")
    package_tests = loader.discover(start_dir=start_dir, pattern=pattern)
    standard_tests.addTests(package_tests)
    return standard_tests


def main():
    curDir = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(curDir)
    loader = unittest.defaultTestLoader
    tests = load_tests(loader, unittest.TestSuite(), "test_*")

    return unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == "__main__":
    main()
