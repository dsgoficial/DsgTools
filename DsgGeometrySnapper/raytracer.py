# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-03-18
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
        email                : luiz.claudio@dsg.eb.mil.br
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import math

# Raytrace on an integer, unit - width 2D grid
# with floating point coordinates
# See http://playtechs.blogspot.ch/2007/03/raytracing-on-grid.html
class Raytracer:
    def __init__(self, x0, y0, x1, y1):
        self.dx = abs(x1 - x0)
        self.dy = abs(y1 - y0)
        self.x = math.floor(x0)
        self.y = math.floor(y0)
        self.n = 1

        if self.dx == 0.:
            self.xInc = 0.
            self.error = float("inf")
        elif x1 > x0:
            self.xInc = 1
            self.n += int(math.floor(x1)) - self.x
            self.error = (math.floor(x0) + 1 - x0) * self.dy
        else:
            self.xInc = -1
            self.n += self.x - int(math.floor(x1))
            self.error = (x0 - math.floor(x0)) * self.dy
        
        if self.dy == 0.:
            self.yInc = 0.
            self.error = -float("inf")
        elif y1 > y0:
            self.yInc = 1
            self.n += int(math.floor(y1)) - self.y
            self.error -= (math.floor(y0) + 1 - y0) * self.dx
        else:
            self.yInc = -1
            self.n += self.y - int(math.floor(y1))
            self.error -= (y0 - math.floor(y0)) * self.dx

    def curCol(self):
        return self.x

    def curRow(self):
        return self.y

    def next(self):
        if self.error > 0:
            self.y += self.yInc
            self.error -= self.dx
        elif self.error < 0:
            self.x += self.xInc
            self.error += self.dy
        else:
            self.x += self.xInc
            self.y += self.yInc
            self.error += self.dx
            self.error -= self.dy
            self.n -= 1
        self.n -= 1

    def isValid(self):
        return self.n > 0

if __name__ == '__main__':
    rt = Raytracer(0, 0, 10, 10)
    while rt.isValid():
        rt.next()
        print rt.n, rt.error, rt.x, rt.y
