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
from DsgTools.DsgGeometrySnapper.cell import Cell

class GridRow:
    def __init__(self):
        self.cells = []
        self.colStartIdx = 0
        
    def __del__(self):
        for cell in self.cells:
            del cell

    def getCreateCell(self, col):
        """
        Get create cell
        :param col: int
        :return: Cell
        """
        if col < self.colStartIdx:
            for i in xrange(col, self.colStartIdx):
                self.cells.insert(0, Cell())
            self.colStartIdx = col
            return self.cells[0]
        elif col >= self.colStartIdx + len(self.cells):
            for i in xrange(self.colStartIdx + len(self.cells), col + 1):
                self.cells.append(Cell())
            return self.cells[-1]
        else:
            return self.cells[col - self.colStartIdx]
    
    def getCell(self, col):
        """
        get Cell object
        :param col: int
        :return:
        """
        if col < self.colStartIdx or col >= self.colStartIdx + len(self.cells):
            return None
        else:
            return self.cells[col - self.colStartIdx]
    
    def getSnapItems(self, colStart, colEnd):
        """
        Get SnapItems
        :param colStart: int
        :param colEnd: int
        :return:
        """
        colStart = max(colStart, self.colStartIdx)
        colEnd = min(colEnd, self.colStartIdx + len(self.cells) - 1)

        items = []
        for col in xrange(colStart, colEnd + 1):
            items.append(self.cells[col - self.colStartIdx])
        return items
