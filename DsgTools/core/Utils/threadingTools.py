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
import os


def concurrently(handler, inputs, *, max_concurrency=None, feedback=None):
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
    # Determine optimal concurrency
    if max_concurrency is None:
        max_concurrency = min(os.cpu_count() - 1 or 1, 5)

    # Convert inputs to iterator
    handler_inputs = iter(inputs)
    total_submitted = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_concurrency) as executor:
        # Initial batch of tasks
        futures = {
            executor.submit(handler, input): input
            for input in itertools.islice(handler_inputs, max_concurrency)
        }
        total_submitted += len(futures)

        while futures:
            # Wait for the first task to complete
            done, _ = concurrent.futures.wait(
                futures, return_when=concurrent.futures.FIRST_COMPLETED
            )

            for fut in done:
                try:
                    result = fut.result()
                    if result is not None:
                        yield result
                except Exception as e:
                    if feedback is not None:
                        feedback.pushWarning(f"Error processing input: {str(e)}")
                futures.pop(fut)

            # Check for cancellation
            if feedback is not None:
                if feedback.isCanceled():
                    executor.shutdown(cancel_futures=True, wait=False)
                    break
                # Update progress if possible
                if hasattr(feedback, "setProgress") and total_submitted > 0:
                    progress = (
                        (total_submitted - len(futures)) / total_submitted
                    ) * 100
                    feedback.setProgress(progress)

            # Submit new tasks to replace completed ones
            for input in itertools.islice(handler_inputs, len(done)):
                if feedback is not None and feedback.isCanceled():
                    break
                fut = executor.submit(handler, input)
                futures[fut] = input
                total_submitted += 1
