# -*- coding: utf-8 -*-

import math

from PyQt5 import QtGui


def hsl(hue, saturation, lightness):
    return QtGui.QColor.fromHsvF((hue % 360) / 360, saturation / 100, lightness / 100)

def deg2rad(deg):
    return deg / 180 * math.pi

def rad2deg(rad):
    return rad * 180 / math.pi

def lerp(x, old_min, old_max, new_min, new_max):
    return (x - old_min) / (old_max - old_min) * (new_max - new_min) + new_min
