# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-04-17
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

import itertools

import concurrent.futures
import itertools


def concurrently(handler, inputs, *, max_concurrency=5):
    """
    Calls the function ``handler`` on the values ``inputs``.

    ``handler`` should be a function that takes a single input, which is the
    individual values in the iterable ``inputs``.

    Generates (input, output) tuples as the calls to ``handler`` complete.

    See https://alexwlchan.net/2019/10/adventures-with-concurrent-futures/ for an explanation
    of how this function works.

    """
    # Make sure we get a consistent iterator throughout, rather than
    # getting the first element repeatedly.
    handler_inputs = iter(inputs)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(handler, input): input
            for input in itertools.islice(handler_inputs, max_concurrency)
        }

        while futures:
            done, _ = concurrent.futures.wait(
                futures, return_when=concurrent.futures.FIRST_COMPLETED
            )

            for fut in done:
                original_input = futures.pop(fut)
                yield fut.result()

            for input in itertools.islice(handler_inputs, len(done)):
                fut = executor.submit(handler, input)
                futures[fut] = input
