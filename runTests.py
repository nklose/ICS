#!/usr/bin/env python
""" Runs tests for the ICS application. Call with -h for more information on how
to use the script.

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
