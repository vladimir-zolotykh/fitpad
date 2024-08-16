#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
from typing import List, Optional
from entry_var import EntryVar


class NumberedSets(list):
    """Represents one set of an exercise

    """

    def __init__(self, widgets: List[tk.Widget]):
        super().__init__(widgets)

    @staticmethod
    def grid_column(widget: tk.Widget) -> int:
        """Return the column number of a widget"""

        return int(widget.grid_info()['column'])

    @classmethod
    def from_grid(cls, box: tk.Frame, row: int) -> 'NumberedSets':
        slaves = sorted(box.grid_slaves(row=row), key=NumberedSets.grid_column)
        return cls(slaves)

    @classmethod
    def from_list(cls, row: List[tk.Widget]) -> 'NumberedSets':
        return cls(sorted(row, key=NumberedSets.grid_column))

    def column(self, column: int = 0) -> Optional[tk.Widget]:
        for w in self:
            if self.grid_column(w) == column:
                return w
        return None

    def set_no(self) -> int:
        """Return the set number (integer)

        Each set [of exercise] has a set number, the 1st Entry widget
        of a grid row"""

        w: Optional[tk.Widget] = self.column(0)
        if isinstance(w, EntryVar):
            var: tk.StringVar = w.configure('textvariable')
            return int(var.get())
        else:
            raise TypeError(f'Expected Entry widget, got {type(w)}')
