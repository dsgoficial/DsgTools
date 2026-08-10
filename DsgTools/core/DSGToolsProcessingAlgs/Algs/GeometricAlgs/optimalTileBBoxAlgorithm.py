# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2026-05-28
        git sha              : $Format:%H$
        copyright            : (C) 2026 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba.philipe@eb.mil.br
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from __future__ import annotations

from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed

from qgis.PyQt.QtCore import QCoreApplication, QVariant
from qgis.core import (
    QgsFeature,
    QgsFeatureSink,
    QgsField,
    QgsFields,
    QgsGeometry,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorLayer,
    QgsRectangle,
    QgsWkbTypes,
)


# ═══════════════════════════════════════════════════════════════════════════
# Pure functions — no external state, thread-safe by construction
# ═══════════════════════════════════════════════════════════════════════════


def _runs(row_data: list) -> tuple:
    result, i, n = [], 0, len(row_data)
    while i < n:
        if row_data[i]:
            j = i + 1
            while j < n and row_data[j]:
                j += 1
            result.append((i, j))
            i = j
        else:
            i += 1
    return tuple(result)


def _greedy_merge(rects: list, threshold: float) -> list:
    EPS = 1e-10
    changed = True

    while changed and len(rects) > 1:
        changed = False
        best_score = -1.0
        best = None

        for i in range(len(rects)):
            for j in range(i + 1, len(rects)):
                a, b = rects[i], rects[j]

                xmin = min(a["xmin"], b["xmin"])
                xmax = max(a["xmax"], b["xmax"])
                ymin = min(a["ymin"], b["ymin"])
                ymax = max(a["ymax"], b["ymax"])
                bbox_area = (xmax - xmin) * (ymax - ymin)

                if bbox_area < EPS:
                    continue

                combined_tile_area = a["tile_area"] + b["tile_area"]
                cov = combined_tile_area / bbox_area * 100.0

                if cov < threshold:
                    continue

                score = cov * bbox_area
                if score > best_score:
                    best_score = score
                    best = (
                        i,
                        j,
                        {
                            "xmin": xmin,
                            "xmax": xmax,
                            "ymin": ymin,
                            "ymax": ymax,
                            "tile_area": combined_tile_area,
                            "coverage_pct": cov,
                            "tile_count": a["tile_count"] + b["tile_count"],
                        },
                    )

        if best is not None:
            i, j, merged = best
            rects = [rects[k] for k in range(len(rects)) if k not in (i, j)]
            rects.append(merged)
            changed = True

    return rects


def _decompose_component(
    comp_cells: list,
    xs: list,
    ys: list,
    occ: list,
    tile_area_grid: list,
    tile_count_grid: list,
    threshold: float,
) -> list:
    rs = [r for r, _ in comp_cells]
    cs = [c for _, c in comp_cells]
    r_lo, r_hi = min(rs), max(rs) + 1
    c_lo, c_hi = min(cs), max(cs) + 1
    sny = r_hi - r_lo
    snx = c_hi - c_lo

    def sub_occ(r, c):
        return occ[r_lo + r][c_lo + c]

    def sub_area(r, c):
        return tile_area_grid[r_lo + r][c_lo + c]

    def sub_count(r, c):
        return tile_count_grid[r_lo + r][c_lo + c]

    rects = []
    row = 0
    while row < sny:
        row_runs = _runs([sub_occ(row, c) for c in range(snx)])
        if not row_runs:
            row += 1
            continue

        row_end = row + 1
        while row_end < sny:
            if _runs([sub_occ(row_end, c) for c in range(snx)]) == row_runs:
                row_end += 1
            else:
                break

        ymin = ys[r_lo + row]
        ymax = ys[r_lo + row_end]

        for c_s, c_e in row_runs:
            xmin = xs[c_lo + c_s]
            xmax = xs[c_lo + c_e]
            bbox_area = (xmax - xmin) * (ymax - ymin)

            tile_area = sum(
                sub_area(rr, cc) for rr in range(row, row_end) for cc in range(c_s, c_e)
            )
            tile_count = sum(
                sub_count(rr, cc)
                for rr in range(row, row_end)
                for cc in range(c_s, c_e)
            )
            rects.append(
                {
                    "xmin": xmin,
                    "xmax": xmax,
                    "ymin": ymin,
                    "ymax": ymax,
                    "tile_area": tile_area,
                    "coverage_pct": (tile_area / bbox_area * 100.0)
                    if bbox_area > 0
                    else 0.0,
                    "tile_count": tile_count,
                }
            )
        row = row_end

    return _greedy_merge(rects, threshold)


# ═══════════════════════════════════════════════════════════════════════════
# QGIS Processing Algorithm
# ═══════════════════════════════════════════════════════════════════════════


class OptimalTileBBoxAlgorithm(QgsProcessingAlgorithm):

    INPUT_TILES = "INPUT_TILES"
    OUTPUT_BBOXES = "OUTPUT_BBOXES"
    COVERAGE_THRESH = "COVERAGE_THRESH"
    MAX_WORKERS = "MAX_WORKERS"

    def tr(self, string):
        return QCoreApplication.translate("OptimalTileBBoxAlgorithm", string)

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_TILES,
                self.tr("Tile layer"),
                [QgsProcessing.TypeVectorPolygon],
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_BBOXES,
                self.tr("Optimized bounding boxes"),
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.COVERAGE_THRESH,
                self.tr("Minimum coverage for rectangle merging (%)"),
                type=QgsProcessingParameterNumber.Double,
                defaultValue=85.0,
                minValue=0.0,
                maxValue=100.0,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.MAX_WORKERS,
                self.tr("Parallel workers"),
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=4,
                minValue=1,
                maxValue=32,
            )
        )

    def processAlgorithm(self, parameters, context, feedback):

        layer = self.parameterAsVectorLayer(parameters, self.INPUT_TILES, context)
        threshold = self.parameterAsDouble(parameters, self.COVERAGE_THRESH, context)
        n_workers = self.parameterAsInt(parameters, self.MAX_WORKERS, context)

        feedback.pushInfo(self.tr("[ 1/3 ] Reading tile geometries..."))
        tiles = []
        for feat in layer.getFeatures():
            if feedback.isCanceled():
                return {}
            b = feat.geometry().boundingBox()
            tiles.append(
                {
                    "xmin": b.xMinimum(),
                    "xmax": b.xMaximum(),
                    "ymin": b.yMinimum(),
                    "ymax": b.yMaximum(),
                }
            )

        if not tiles:
            feedback.reportError(self.tr("No tiles found."), fatalError=True)
            return {}
        feedback.pushInfo(self.tr("       {0} tile(s) read.").format(len(tiles)))

        feedback.pushInfo(self.tr("[ 2/3 ] Building coordinate grid..."))
        PREC = 8
        xs = sorted({round(v, PREC) for t in tiles for v in (t["xmin"], t["xmax"])})
        ys = sorted({round(v, PREC) for t in tiles for v in (t["ymin"], t["ymax"])})
        nx, ny = len(xs) - 1, len(ys) - 1
        xi = {v: i for i, v in enumerate(xs)}
        yi = {v: i for i, v in enumerate(ys)}

        occ = [[False] * nx for _ in range(ny)]
        tile_area_grid = [[0.0] * nx for _ in range(ny)]
        tile_count_grid = [[0] * nx for _ in range(ny)]

        for t in tiles:
            c0 = xi[round(t["xmin"], PREC)]
            c1 = xi[round(t["xmax"], PREC)]
            r0 = yi[round(t["ymin"], PREC)]
            r1 = yi[round(t["ymax"], PREC)]
            for r in range(r0, r1):
                for c in range(c0, c1):
                    occ[r][c] = True
                    tile_area_grid[r][c] = (xs[c + 1] - xs[c]) * (ys[r + 1] - ys[r])
                    tile_count_grid[r][c] += 1

        feedback.pushInfo(self.tr("[ 3/3 ] Detecting components and decomposing..."))
        visited = [[False] * nx for _ in range(ny)]
        components = []

        for r0 in range(ny):
            for c0 in range(nx):
                if occ[r0][c0] and not visited[r0][c0]:
                    comp = []
                    q = deque([(r0, c0)])
                    visited[r0][c0] = True
                    while q:
                        r, c = q.popleft()
                        comp.append((r, c))
                        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                            nr, nc = r + dr, c + dc
                            if (
                                0 <= nr < ny
                                and 0 <= nc < nx
                                and occ[nr][nc]
                                and not visited[nr][nc]
                            ):
                                visited[nr][nc] = True
                                q.append((nr, nc))
                    components.append(comp)

        feedback.pushInfo(
            self.tr("       {0} component(s) detected.").format(len(components))
        )

        all_rects = []
        with ThreadPoolExecutor(max_workers=n_workers) as pool:
            future_to_idx = {
                pool.submit(
                    _decompose_component,
                    comp,
                    xs,
                    ys,
                    occ,
                    tile_area_grid,
                    tile_count_grid,
                    threshold,
                ): idx
                for idx, comp in enumerate(components)
            }
            done = 0
            for future in as_completed(future_to_idx):
                if feedback.isCanceled():
                    try:
                        pool.shutdown(wait=False, cancel_futures=True)
                    except TypeError:
                        pool.shutdown(wait=False)
                    return {}
                done += 1
                feedback.setProgress(int(done / len(components) * 90))
                try:
                    all_rects.extend(future.result())
                except Exception as exc:
                    feedback.reportError(
                        self.tr("Error in component {0}: {1}").format(
                            future_to_idx[future], exc
                        )
                    )

        feedback.pushInfo(
            self.tr("       {0} rectangle(s) generated.").format(len(all_rects))
        )

        fields = QgsFields()
        fields.append(QgsField("rect_id", QVariant.Int))
        fields.append(QgsField("coverage_pct", QVariant.Double))
        fields.append(QgsField("tile_count", QVariant.Int))

        sink, dest_id = self.parameterAsSink(
            parameters,
            self.OUTPUT_BBOXES,
            context,
            fields,
            QgsWkbTypes.Polygon,
            layer.crs(),
        )

        for i, rect in enumerate(all_rects):
            feat = QgsFeature(fields)
            feat.setGeometry(
                QgsGeometry.fromRect(
                    QgsRectangle(
                        rect["xmin"],
                        rect["ymin"],
                        rect["xmax"],
                        rect["ymax"],
                    )
                )
            )
            feat["rect_id"] = i
            feat["coverage_pct"] = round(rect["coverage_pct"], 2)
            feat["tile_count"] = rect["tile_count"]
            sink.addFeature(feat, QgsFeatureSink.FastInsert)

        feedback.setProgress(100)
        return {self.OUTPUT_BBOXES: dest_id}

    def name(self) -> str:
        return "optimal_tile_bboxes"

    def displayName(self) -> str:
        return self.tr("Optimal Tile Bounding Boxes")

    def group(self) -> str:
        return self.tr("Geometric Algorithms")

    def groupId(self) -> str:
        return "DSGTools - Geometric Algorithms"

    def createInstance(self):
        return OptimalTileBBoxAlgorithm()

    def shortHelpString(self) -> str:
        return self.tr(
            "<b>Decomposes tiles into optimal bounding boxes minimizing NoData.</b><br><br>"
            "Use the output layer to clip rasters with QGIS native "
            '"Clip Raster by Extent" or via GDAL.<br><br>'
            "<u>Threshold:</u> the higher the value, the fewer merges are accepted "
            "and the more rectangles are generated. "
            "For distributions with significant gaps, use &ge; 80%."
        )
