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
        # cols = 1, rows = 2
        Options = Dict[str, Any]    # .grid_info() dict
        SavedWidget = Tuple[f2.Frame2D, Options]
        sorted: List[SavedWidget] = []
        row_index: int
        for row_index in range(rows):
            w: f2.Frame2D
            w = cast(f2.Frame2D, self.grid_slaves(column=0, row=row_index)[0])
            sorted.append((w, cast(Options, w.grid_info())))

        def _key(saved_widget: SavedWidget) -> int:
            var: EntryVar = saved_widget[0][0, 0]
            return int(var.get())

        sorted.sort(key=_key)
        o: Options
        deleted_exer: List[str] = []  # deleted exercises (names)
        saved_widget: SavedWidget
        row_index = 0
        for saved_widget in sorted:
            w, o = saved_widget
            # w[tk.Frame]: EntryVar | SetFrame
            entry: EntryVar = w[0, 0]
            var = entry.configure('textvariable')
            if int(entry.get()) == 0:
                frame_set: f2s.Frame2DSet = w[0, 1]
                label: tk.Label = frame_set[0, 0][0, 0]
                exer_name: str = label.cget('text')
                deleted_exer.append(exer_name)
                w.destroy()
            else:
                w.grid(column=o['column'], row=row_index, sticky=o['sticky'])
                var.set(str(row_index + 1))
                row_index += 1
        return deleted_exer
