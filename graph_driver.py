import PIL.Image as Image
import os
import shutil

import midend.adaptor as adaptor
import midend.result as result


def generate():
    fileIn = "accTests/inputs/RGBtemp/rgb_001.png"
    pilImage = Image.open(fileIn)
    # Run red, green and blue autos:
    color_list = ["r", "g", "b"]
    g0 = 1
    w = 10
    ginf = 0
    range_val = 20
    consider_deltas = True

    resultLists = adaptor.run_dual_mixed_image(pilImage, color_list, g0, w,
                                               ginf, range_val, consider_deltas)
    generate_graphs(resultLists)
    # Should now be a graph0.png, graph1.png, graph2.png
    return resultLists


def generate_graphs(resultList, name_format="graph%d.png"):
    for i, x in enumerate(resultList):
        # Get a file like object that contains the string of the image.
        fileLike = x.plotToStringIO()
        lines = fileLike.readlines()
        outFile = open(name_format % i, "wb")
        firstLine = True
        for line in lines:
            outFile.write(line)


def generateTriple():
    fileIn = "accTests/inputs/RGBtemp/rgb_001.png"
    pilImage = Image.open(fileIn)
    limit = 32  # Hardcoded as example
    range_val = 15  # Hardcoded as example
    g0 = 50
    w = 2
    ginf = 0

    firstResult = adaptor.run_triple_mixed_image_part1(pilImage)
    generate_graphs([firstResult], name_format="triplegraph_1_%d.png")
    secondResult = adaptor.run_triple_part2(firstResult, limit)
    generate_graphs([secondResult], name_format="triplegraph_2_%d.png")
    finalResult = adaptor.run_triple_part3(secondResult, range_val, g0, w, ginf)
    generate_graphs([finalResult], name_format="triplegraph_3_%d.png")
    return finalResult


def saveAllFiles(results):
    outputPath = "output/"
    # save results.txt, filename is usually "results.txt", just making the
    # argument obvious
    if os.path.exists(outputPath):
        shutil.rmtree(outputPath)
    os.mkdir(outputPath)
    result.saveResultsFile(outputPath, results, filename="results.txt")
    # result.saveResultsFile(outputPath, results) is equivalent
    # Save other files
    for res in results:
        #Save data, setting names to their default values
        res.saveData(outputPath, dataName=None, fitName=None)
        # res.saveData(outputPath) is equivalent
        # can also save to a file like object:
        # res.saveDataFileLike(dataFileLike, fitFileLike)


if __name__ == "__main__":
    outputs = generate()
    outputs.append(generateTriple())
    saveAllFiles(outputs)
