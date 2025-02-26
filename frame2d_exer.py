#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import cast, Dict, Any, List, Tuple
import tkinter as tk
import frame2d as f2
import frame2d_set as f2s
from entry_var import EntryVar


class Frame2DExer(f2.Frame2D):
    def arrange(self) -> list[str]:
        """Arrange exercises in exercise number order.

        Return the deleletd exer names list"""

        cols, rows = self.grid_size()
        Options = Dict[str, Any]    # .grid_info() dict
        ExerFrameRow = Tuple[EntryVar, f2s.Frame2DSet, Options]
        sorted: List[ExerFrameRow] = []
        row_index: int
        for row_index in range(rows):
            e = cast(EntryVar, self.grid_slaves(column=0, row=row_index)[0])
            s = cast(f2s.Frame2DSet,
                     self.grid_slaves(column=1, row=row_index)[0])
            sorted.append((e, s, cast(Options, s.grid_info())))

        def _key(exerframerow: ExerFrameRow) -> int:
            var: EntryVar = exerframerow[0]
            return int(var.get())

        sorted.sort(key=_key)
        o: Options
        deleted_exer: List[str] = []  # deleted exercises (names)
        exerframerow: ExerFrameRow
        row_index = 0
        for exerframerow in sorted:
            e, s, o = exerframerow
            var = e.configure('textvariable')
            if int(e.get()) == 0:
                label: tk.Label = s[0, 0]
                exer_name: str = label.cget('text')
                deleted_exer.append(exer_name)
                e.destroy()
                s.destroy()
            else:
                var.set(str(row_index + 1))
                e.grid(column=0, row=row_index)
                s.grid(column=o['column'], row=row_index, sticky=o['sticky'])
                row_index += 1
        return deleted_exer
