import argparse
import os
import shutil

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("actualOutput")
    args = parser.parse_args()
    old_names = ['b', 'g', 'r', 'rg', 'rb', 'gb', 'rgb']
    new_names = ['ACb', 'ACg', 'ACr', 'XCrg', 'XCrb', 'XCgb', "TripleCrgb"]
    for old, new in zip(old_names, new_names):
        oldFile = os.path.join(args.actualOutput, "%s.txt" % old)
        oldFileFit = os.path.join(args.actualOutput, "%s_fit.txt" % old)
        newFile = os.path.join(args.actualOutput, "%s.txt" % new)
        newFileFit = os.path.join(args.actualOutput, "%sFit.txt" % new)
        shutil.move(oldFile, newFile)
        shutil.move(oldFileFit, newFileFit)
    print "Done adjusting files"
