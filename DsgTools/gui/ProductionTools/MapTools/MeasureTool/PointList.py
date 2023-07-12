# -*- coding: utf-8 -*-


class PointList(list):
    def __init__(self):
        list.__init__(self)

    def empty(self):
        self[:] = []

    def newPoint(self):
        if len(self) > 0:
            self.insert(0, self[0])

    def updateCurrentPoint(self, point):
        if len(self) > 0:
            self[0] = point
        else:
            self.insert(0, point)

    def previousPoint(self):
        if len(self) > 1:
            return self[1]
        else:
            return None

    def removeLastPoint(self):
        if len(self) > 1:
            del self[1]
