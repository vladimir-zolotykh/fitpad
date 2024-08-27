#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
from typing import List, Tuple, Any, Dict, cast
import frame2d as f2
from entry_var import EntryVar


class Frame2DSet(f2.Frame2D):
    def arrange(self):
        cols, rows = self.grid_size()
        mb = self.grid_slaves(row=rows - 1)[0]  # menu button
        entries: List[tk.Widget] = []
        Info = Dict[str, Any]
        SavedEntry = Tuple[EntryVar, Info]
        saved: List[List[SavedEntry]] = []
        for i in range(1, rows - 1):
            entries = [self[i, col] for col in range(cols)]
            item: List[SavedEntry] = []
            item = cast(List[SavedEntry],
                        [(e, e.grid_info()) for e in entries])
            saved.append(item)

        def get_set_no(row):
            e0: EntryVar = row[0][0]
            return int(e0.get())

        saved.sort(key=get_set_no)
        row: List[SavedEntry]
        row_index: int = 1
        for row in saved:
            set_no: EntryVar = row[0][0]
            saved_entry: SavedEntry
            e: EntryVar
            new_set_no: int = 1
            if int(set_no.get()) == 0:
                for saved_entry in row:
                    e = saved_entry[0]
                    e.destroy()
            else:
                for col, saved_entry in enumerate(row):
                    e = saved_entry[0]
                    if col == 0:
                        # Renumber the set. The first (index = 0)
                        # EntryVar widget holds the set number.
                        var: tk.StringVar = e.configure('textvariable')
                        var.set(str(new_set_no))
                        new_set_no += 1
                    o: Info = saved_entry[1]
                    e.grid(column=o['column'], row=row_index,
                           sticky=o['sticky'])
                row_index += 1
        mb.grid(column=0, row=row_index + 1, columnspan=cols)
