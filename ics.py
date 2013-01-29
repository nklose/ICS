#!/usr/bin/env python
""" Driver for ics program in python """
import icsLogger # required, runs code on import
import argparse
import logging
import icse
import os

logger = logging.getLogger("main")


def closeOptions(options):
    if options.infile_rgb:
        options.infile_rgb.close()
        options.infile_rgb = None
    if options.infile_r:
        options.infile_r.close()
        options.infile_r = None
    if options.infile_g:
        options.infile_g.close()
        options.infile_g = None
    if options.infile_b:
        options.infile_b.close()
        options.infile_b = None


def main():
    """ def main(options): """
    """ Main code here """
    """
    logger.info("Recieved Args: %s", str(options))
    if options.infile_rgb:
        fname = options.infile_rgb.name
        logger.info("Using rgb path: %s", fname)
        closeOptions(options)
    elif options.infile_r and options.infile_g and options.infile_b:
        fnames = {}
        fnames['r'] = options.infile_r.name
        fnames['g'] = options.infile_g.name
        fnames['b'] = options.infile_b.name
        logger.info("Using red: %s", fnames['r'])
        logger.info("Using green: %s", fnames['g'])
        logger.info("Using blue: %s", fnames['b'])
        closeOptions(options)
    else:
        closeOptions(options)
        logger.error("Invalid arguements. Please supply infile_rgb or  all of \
infile_r, infile_g, and infile_b.")
        return
    """
    if not os.path.exists(icse.OUTPUT_DIR):
        os.mkdir(icse.OUTPUT_DIR)
    icse.ics_run('')

if __name__ == "__main__":
    """
    parser = argparse.ArgumentParser(description='Loads a single image or three\
 monocolored images.')
    parser.add_argument('--infile_rgb', nargs='?', type=argparse.FileType('r'))
    parser.add_argument('--infile_r', nargs='?', type=argparse.FileType('r'))
    parser.add_argument('--infile_g', nargs='?', type=argparse.FileType('r'))
    parser.add_argument('--infile_b', nargs='?', type=argparse.FileType('r'))
    args = parser.parse_args()
    """
    main()
