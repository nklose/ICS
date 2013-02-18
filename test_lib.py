""" Contains common functions between test libraries.
"""
import unittest
import os.path


def runTestInDirectory(directory):
    tests = loadTestsInDir(directory)
    return unittest.TextTestRunner(verbosity=1).run(tests)


def loadTestsInDir(directory, pattern="test_*"):
    loader = unittest.defaultTestLoader
    testSuite = unittest.TestSuite()

    # top level directory cached on loader instance
    this_dir = os.path.dirname(__file__)
    start_dir = os.path.join(this_dir, directory)
    package_tests = loader.discover(start_dir=start_dir, pattern=pattern)
    testSuite.addTests(package_tests)
    return testSuite
