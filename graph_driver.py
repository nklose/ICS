import PIL.Image as Image

import midend.adaptor as adaptor


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


def generate_graphs(resultList, name_format="graph%d.png"):
    for i, x in enumerate(resultList):
        # Get a file like object that contains the string of the image.
        fileLike = x.plotToStringIO()
        outFile = open(name_format % i, "w")
        for line in fileLike.readlines():
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

if __name__ == "__main__":
    generate()
    generateTriple()
