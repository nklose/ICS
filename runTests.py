#!/usr/bin/env python
import test_lib as test_lib
import argparse


def main(options):
    directory = "."
    if options.unit:
        directory = "unitTests"
    elif options.acceptance:
        directory = "accTests"
    elif options.integration:
        directory = "intTests"
    return test_lib.runTestInDirectory(directory)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Runs all tests for ICS, or \
only certain specified tests')
    parser.add_argument('-u', '--unit', action="store_true", default=False,
                        help="Run unit tests only.")
    parser.add_argument('-a', '--acceptance', action="store_true",
                        default=False, help="Run acceptance tests only.")
    parser.add_argument('-i', '--integration', action="store_true",
                        default=False, help="Run integration tests only.")
    args = parser.parse_args()
    main(args)
