#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import cast, Dict, Any, List, Tuple
import tkinter as tk
import frame2d as f2
import frame2d_set as f2s
from entry_var import EntryVar


class Frame2DExer(f2.Frame2D):
    def arrange(self):
        """Arrange exercises in exercise number order.

        Return the deleletd exer names list"""

        cols, rows = self.grid_size()
        Options = Dict[str, Any]    # .grid_info() dict
        ExerFrameRow = Tuple[EntryVar, f2.Frame2D, Options]
        sorted: List[ExerFrameRow] = []
        row_index: int
        for row_index in range(rows):
            slaves = self.grid_slaves(row=row_index)
            w: f2.Frame2D
            w = cast(f2.Frame2D, slaves[1])  # Frame2DSet
            e = cast(EntryVar, slaves[0])
            sorted.append((e, w, cast(Options, w.grid_info())))

        def _key(exerframerow: ExerFrameRow) -> int:
            var: EntryVar = exerframerow[0]
            return int(var.get())

        sorted.sort(key=_key)
        o: Options
        deleted_exer: List[str] = []  # deleted exercises (names)
        exerframerow: ExerFrameRow
        row_index = 0
        for exerframerow in sorted:
            e, w, o = exerframerow
            entry: EntryVar = e
            var = entry.configure('textvariable')
            if int(entry.get()) == 0:
                frame_set: f2s.Frame2DSet = cast(f2s.Frame2DSet, w)
                label: tk.Label = frame_set[0, 0][0, 0]
                exer_name: str = label.cget('text')
                deleted_exer.append(exer_name)
                e.destroy()
                w.destroy()
            else:
                w.grid(column=o['column'], row=row_index, sticky=o['sticky'])
                var.set(str(row_index + 1))
                row_index += 1
        return deleted_exer
