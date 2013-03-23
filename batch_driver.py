""" Sample driver file for batch mode.
"""

import midend.batchRunner as batchRunner
from backend.configs import BadConfig


def printProgress(numberOfFilesFinished, numberOfFilesTotal):
    print numberOfFilesFinished, "done of", numberOfFilesTotal


def runBadConfig():
    myBadConfig = BadConfig()
    # fix the input directory
    myBadConfig.input_directory = "accTests/inputs/badData/"
    bRunner = batchRunner.BatchRunner(myBadConfig)
    bRunner.runAll(printProgress)
    myDict = bRunner.outputToStringIo()
    fileList = sorted(myDict.keys())
    # Should have 141 (14 files * 10 runs + 1 results.txt)
    print len(fileList), fileList

def runBadConfigManual():
    myBadConfig = BadConfig()
    # fix the input directory
    myBadConfig.input_directory = "accTests/inputs/badData/"
    bRunner = batchRunner.BatchRunner(myBadConfig)
    total = myBadConfig.name_max - myBadConfig.name_min + 1
    numLeft = total
    while numLeft > 0:
        numLeft = bRunner.run()
        printProgress(total - numLeft, total)
    myDict = bRunner.outputToStringIo()
    fileList = sorted(myDict.keys())
    # Should have 141 (14 files * 10 runs + 1 results.txt)
    print len(fileList), fileList


if __name__ == "__main__":
    runBadConfig()
    runBadConfigManual()
