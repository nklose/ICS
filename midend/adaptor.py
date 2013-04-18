import numpy as np

import result
import debugWindowsMemory as winmem

import sys
import os.path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)

import backend.bimloader as bimloader
import backend.dual as dual
import backend.triple as triple
import backend.backend_utils as butils
import logging

LOGGER = logging.getLogger("me.adp")

ALL_COLORS = str.split('r:g:b:rg:rb:gb:rgb', ':')


def run_dual_mixed_image(pilImage, colorList, g0, w, ginf, range_val,
                         consider_deltas):
    """Runs dual on combinations of mixed image

    Arguments:
       pilImage: the PIL form of the image
       pilImage type: PIL.Image

       colorList: list of lowercase color strings (eg, ['r', 'g', 'rg'])
       colorList type: list

       g0: the initial g0 to use for all dual runs
       g0 type: int

       w:  the initial w to use for all dual runs
       w type: int

       ginf: the initial ginf to use for all dual runs
       ginf type: int

       range_val: the range value to use for all dual runs
       range_val type: integer

       consider_deltas: Whether to consider deltas
       consider_deltas type: boolean

    Return values:
        A list containing midened.result.DualResult
    """
    LOGGER.debug("===Starting Mixed dual===")
    r, g, b = bimloader.load_image_pil_mixed(pilImage)
    fresult = __run_all_dual(r, g, b, colorList, g0, w, ginf, range_val,
                            consider_deltas)
    LOGGER.debug("===Ending mixed dual===")
    return fresult


def run_dual_separate_image(pilR, pilG, pilB, colorList, g0, w, ginf, range_val,
                            consider_deltas):
    """Runs dual on seperated images

    Arguments:
       pilR: the PIL form of the red channel
       pilR type: PIL.Image

       pilG: the PIL form of the green channel
       pilG type: PIL.Image

       pilB: the PIL form of the blue channel
       pilB type: PIL.Image

       colorList: list of lowercase color strings (eg, ['r', 'g', 'rg'])
       colorList type: list

       g0: the initial g0 to use for all dual runs
       g0 type: int

       w:  the initial w to use for all dual runs
       w type: int

       ginf: the initial ginf to use for all dual runs
       ginf type: int

       range_val: the range value to use for all dual runs
       range_val type: integer

       consider_deltas: Whether to consider deltas
       consider_deltas type: boolean

    Return values:
        A list containing midened.result.DualResult
    """
    LOGGER.debug("===Starting seperate dual===")
    r = bimloader.load_image_pil_split(pilR)
    g = bimloader.load_image_pil_split(pilG)
    b = bimloader.load_image_pil_split(pilB)
    # Generate graphs not included currently.
    fresult = __run_all_dual(r, g, b, colorList, g0, w, ginf, range_val,
                            consider_deltas)
    LOGGER.debug("===Ending seperate dual===")
    return fresult


def __run_all_dual(r, g, b, colorList, g0, w, ginf, range_val, consider_deltas):
    """Runs dual on seperated images

    Arguments:
       r: the scipy form of the red channel
       r type: numpy.array

       g: the scipy form of the green channel
       g type: numpy.array

       b: the scipy form of the blue channel
       b type: numpy.array

       colorList: list of lowercase color strings (eg, ['r', 'g', 'rg'])
       colorList type: list

       g0: the initial g0 to use for all dual runs
       g0 type: int

       w:  the initial w to use for all dual runs
       w type: int

       ginf: the initial ginf to use for all dual runs
       ginf type: int

       range_val: the range value to use for all dual runs
       range_val type: integer

       consider_deltas: Whether to consider deltas
       consider_deltas type: boolean

    Return values:
        A list containing midened.result.DualResult
    """
    deltaX = 0
    deltaY = 0
    initial_val = np.array([g0, w, ginf, deltaX, deltaY], dtype=np.float64)
    p = [(r, None, None), (g, None, None), (b, None, None), (r, g, None),
         (r, b, None), (g, b, None), (r, g, b)]
    results = []
    for color in colorList:
        i = list.index(ALL_COLORS, color)
        LOGGER.debug("Running dual for " + str(color))
        newResult = __run_dual(p[i][0], p[i][1], color, range_val, 
                               initial_val, consider_deltas)
        results.append(newResult)
        LOGGER.debug("Generated Result: " + str(newResult))
    return results


def __run_dual(firstChannel, secondChannel, color, range_val, initial_val,
               consider_deltas):
    """Runs dual on seperated images

    Arguments:
       firstChannel: the scipy form of the first channel
       firstChannel type: numpy.array

       secondChannel: the scipy form of the second channel
       secondChannel type: numpy.array

       color: lowercase color string (eg, 'r', 'g', or 'rg')
       color type: string

       range_val: the range value to use for all dual runs
       range_val type: integer

       initial_val: the initial guesses for the three curve fitting parameters
                    -- amplitude, width and infinity value
       initial_val type: np.array

       consider_deltas: Whether to consider deltas
       consider_deltas type: boolean

    Return values:
        A midened.result.DualResult
    """
    LOGGER.debug("Calling backend - dual.core")
    (out, par, usedDeltas) = dual.core(firstChannel, secondChannel, range_val,
                                       initial_val, consider_deltas)
    if usedDeltas:
        LOGGER.debug("Calling backend - butils.gauss_2d_deltas")
        fitBeforeReshape = butils.gauss_2d_deltas(np.arange(range_val ** 2), *par)
    else:
        LOGGER.debug("Calling backend - butils.gauss_2d")
        fitBeforeReshape = butils.gauss_2d(np.arange(range_val ** 2), *par[:3])
    fit = fitBeforeReshape.reshape(range_val, range_val)
    resnorm = np.sum((out - fit) ** 2)
    return result.DualResult(par[0], par[1], par[2], par[3], par[4],
                             usedDeltas, resnorm, out, fit, color,
                             range_val)


def run_triple_mixed_image_part1(pilImage):
    """Runs triple on the mixed image

    Arguments:
       pilImage: the PIL form of the image
       pilImage type: PIL.Image

    Return values:
        A midened.result.TripleResult_part1
    """
    LOGGER.debug("===Starting triple mixed part 1===")
    r, g, b = bimloader.load_image_pil_mixed(pilImage)
    fresult = __run_triple_1(r, g, b)
    LOGGER.debug("===Ending triple mixed part 1===")
    return fresult


def run_triple_split_image_part1(pilR, pilG, pilB):
    """Runs triple on seperated images

    Arguments:
       pilR: the PIL form of the red channel
       pilR type: PIL.Image

       pilG: the PIL form of the green channel
       pilG type: PIL.Image

       pilB: the PIL form of the blue channel
       pilB type: PIL.Image

    Return values:
        A midened.result.TripleResult_part1
    """
    LOGGER.debug("===Starting triple split part 1===")
    r = bimloader.load_image_pil_split(pilR)
    g = bimloader.load_image_pil_split(pilG)
    b = bimloader.load_image_pil_split(pilB)
    fresult = __run_triple_1(r, g, b)
    LOGGER.debug("===Ending triple split part 1===")
    return fresult


def __run_triple_1(r, g, b):
    """Runs triple on seperated images

    Arguments:
       r: the scipy form of the red channel
       r type: numpy.array

       g: the scipy form of the green channel
       g type: numpy.array

       b: the scipy form of the blue channel
       b type: numpy.array

    Return values:
        A midened.result.TripleResult_part1
    """
    side = np.shape(r)[0]
    LOGGER.debug("Calling backend - triple.core0 on red")
    (avg_r, sr) = triple.core_0(r)
    LOGGER.debug("Calling backend - triple.core0 on green")
    (avg_g, sg) = triple.core_0(g)
    LOGGER.debug("Calling backend - triple.core0 on blue")
    (avg_b, sb) = triple.core_0(b)
    return result.TripleResult_part1(avg_r, avg_g, avg_b, sr, sg, sb, side)


def run_triple_part2(firstResults, limit):
    """Continues running triple with the given limit.

    Arguments:
       firstResults: the return value from running part 1 of triple
       firstResults type: midened.result.TripleResult_part1

       limit: the limit size to constrain data to.
       limit type: int

    Return values:
        A midened.result.TripleResult_part2
    """
    LOGGER.debug("===Starting Triple part 2===")
    avg_rgb = firstResults.avg_r * firstResults.avg_g * firstResults.avg_b
    LOGGER.debug("Calling backend - triple.core_1")
    try:
        part_rgb = triple.core_1(firstResults.surfaceR, firstResults.surfaceG,
                                 firstResults.surfaceB, avg_rgb, limit)
    except MemoryError as e:
        LOGGER.error("Memory Error - insufficient memory.")
        LOGGER.exception(e)
        if os.name == "nt":
            LOGGER.debug("Memory Load: %s" % winmem.getMemoryLoad())
            LOGGER.debug("Memory Available (physical): %s" % winmem.getMemoryAvailablePhysical())
        raise e
    LOGGER.debug("===Ending Triple part 2===")
    fresult = result.TripleResult_part2(firstResults.side, limit, part_rgb)
    return fresult


def run_triple_part3(secondResults, range_val, g0, w, ginf):
    """Continues running triple with the given limit.

    Arguments:
       secondResults: the return value from running part 2 of triple
       secondResults type: midened.result.TripleResult_part2

       range_val: the range value to use for the triple run
       range_val type: int

       g0: the initial g0 to use for all dual runs
       g0 type: int

       w:  the initial w to use for all dual runs
       w type: int

       ginf: the initial ginf to use for all dual runs
       ginf type: int

    Return values:
        A midened.result.TripleResult_part3
    """
    LOGGER.debug("===Starting Triple part 3===")
    initial_val = np.array([g0, w, ginf], dtype=np.float64)
    LOGGER.debug("Calling backend - triple.core_2")
    (out, par) = triple.core_2(secondResults.part_rgb, range_val, initial_val)
    LOGGER.debug("Calling backend - butils.gauss_1d")
    fit = butils.gauss_1d(np.arange(range_val), *par)
    LOGGER.debug("backend done")
    par[1] = int(par[1] * (secondResults.side / secondResults.lim) * 10) / 10
    resnorm = np.sum((out - fit) ** 2)
    fResult = result.TripleResult_part3(par[0], par[1], par[2], 0, 0,
                                        False, resnorm, out, fit, 'rgb',
                                        range_val)
    LOGGER.debug("===Ending Triple part 3===")
    return fResult
