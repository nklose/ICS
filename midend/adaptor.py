import numpy as np

import result

import sys
import os.path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)

import backend.bimloader as bimloader
import backend.dual as dual
import backend.backend_utils as butils

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
    r, g, b = bimloader.load_image_pil_mixed(pilImage)
    return __run_all_dual(r, g, b, colorList, g0, w, ginf, range_val,
                          consider_deltas)


def run_dual_seperate_image(pilR, pilG, pilB, colorList, g0, w, ginf, range_val,
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
    r = bimloader.load_image_pil_split(pilR)
    g = bimloader.load_image_pil_split(pilG)
    b = bimloader.load_image_pil_split(pilB)
    # Generate graphs not included currently.
    return __run_all_dual(r, g, b, colorList, g0, w, ginf, range_val,
                          consider_deltas)


def __run_all_dual(r, g, b, colorList, g0, w, ginf, range_val, consider_deltas):
    deltaX = 0
    deltaY = 0
    initial_val = np.array([g0, w, ginf, deltaX, deltaY], dtype=np.float64)
    p = [(r, None, None), (g, None, None), (b, None, None), (r, g, None),
         (r, b, None), (g, b, None), (r, g, b)]
    consider_deltas = False
    results = []
    for color in colorList:
        i = list.index(ALL_COLORS, color)
        results.append(__run_dual(p[i][0], p[i][1], color, range_val,
                                  initial_val, consider_deltas))
    return results


def __run_dual(firstChannel, secondChannel, color, range_val, initial_val,
               consider_deltas):
    (out, par, usedDeltas) = dual.core(firstChannel, secondChannel, range_val,
                                       initial_val, consider_deltas)
    fitBeforeReshape = butils.gauss_2d_deltas(np.arange(range_val ** 2), *par)
    fit = fitBeforeReshape.reshape(range_val, range_val)
    resnorm = np.sum((out - fit) ** 2)
    return result.DualResult(par[0], par[1], par[2], par[3], par[4],
                             usedDeltas, resnorm, out, fit, color,
                             range_val, fitBeforeReshape)
