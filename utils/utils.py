import numpy as np


def clamp(val, min, max):
    if val < min:
        return min
    elif val > max:
        return max
    else:
        return val
