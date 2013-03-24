""" Sample driver file for batch mode.
"""

import midend.batchRunner as batchRunner
from backend.configs import BadConfig
import backend.batch as batch
import midend.graph as graph


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
    firstInfo = None

    while numLeft > 0:
        numLeft = bRunner.run()
        if firstInfo is None:
            firstInfo = bRunner.getResults()

            convertInfoToGraphs(firstInfo)
        printProgress(total - numLeft, total)
    myDict = bRunner.outputToStringIo()
    fileList = sorted(myDict.keys())
    # Should have 141 (14 files * 10 runs + 1 results.txt)
    print len(fileList), fileList


def convertInfoToGraphs(info):
    for i in range(6):
        if i < 3: fcode = 'AC'
        if i >= 3: fcode = 'XC'
        outArray = info.dual_out[i, :, :]
        fitArray = info.dual_fit[i, :, :]
        ginf = info.dual_par[i, 2]
        colors = batch.ALL_COLORS[i]
        graphString = graph.plot(outArray, fitArray, colors, ginf)
        with open("batch_1_graph_" + fcode + colors + ".png", "w") as f:
            f.writelines(graphString.readlines())
    ginf = info.triple_par[2]
    graphString = graph.plot_1d(info.triple_out, info.triple_fit, "rgb", ginf)
    with open("batch_1_graph_trip.png", "w") as f:
        f.writelines(graphString.readlines())


def runBadConfigOutputFiles():
    myBadConfig = BadConfig()
    # fix the input directory
    myBadConfig.input_directory = "accTests/inputs/badData/"
    myBadConfig.output_directory = "output/"
    bRunner = batchRunner.BatchRunner(myBadConfig)
    bRunner.runAll(printProgress)
    bRunner.outputAllFiles()


if __name__ == "__main__":
    runBadConfig()
    runBadConfigManual()
    runBadConfigOutputFiles()
