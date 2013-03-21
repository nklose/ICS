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
    for i, x in enumerate(resultLists):
        # Get a file like object that contains the string of the image.
        fileLike = x.plotToStringIO()
        outFile = open("graph%d.png" % i, "w")
        for line in fileLike.readlines():
            outFile.write(line)
    # Should now be a graph0.png, graph1.png, graph2.png


if __name__ == "__main__":
    generate()
