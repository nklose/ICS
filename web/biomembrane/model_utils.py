from models import Parameters


class Colors:
    RED = 0
    GREEN = 1
    BLUE = 2


def __create_params(batch, rangeVal, g0, w, ginf, useDeltas):
    return Parameters(batch=batch, range_val=rangeVal, g0=g0, w=w, ginf=ginf, use_deltas=useDeltas)


def __set_colors(params, *args):
    for color in args:
        if color == Colors.RED:
            params.red = True
        elif color == Colors.GREEN:
            params.green = True
        else:
            params.blue = True

    return params


def create_params_auto(batch, color, rangeVal, g0, w, ginf, useDeltas):
    params = __create_params(batch, rangeVal, g0, w, ginf, useDeltas)
    params = __set_colors(params, color)
    params.correlationType = Parameters.AUTO
    params.save()
    return params

def create_params_cross(batch, color1, color2, rangeVal, g0, w, ginf, useDeltas):
    params = __create_params(batch, rangeVal, g0, w, ginf, useDeltas)
    params = __set_colors(params, color1, color2)
    params.correlationType = Parameters.CROSS
    params.save()
    return params
