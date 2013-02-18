#!/usr/bin/env python
import test_lib as test_lib
import argparse


def main(args):
    directory = "."
    if args.unit:
        directory = "unitTests"
    elif args.acceptance:
        directory = "accTests"
    return test_lib.runTestInDirectory(directory)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Loads a single image or three\
 monocolored images.')
    parser.add_argument('-u', '--unit', action="store_true", default=False)
    parser.add_argument('-a', '--acceptance', action="store_true",
                        default=False)
    args = parser.parse_args()
    main(args)
